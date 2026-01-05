import json
import os
import re
import gc
import torch
import shutil
import time
import csv
from dotenv import load_dotenv
from huggingface_hub import login

# --- IMPORT DEI TEST ---
from tests.tests_task01 import TestTask1
from tests.tests_task02 import TestTask2
from tests.tests_task03 import TestTask3
from tests.tests_task04 import TestTask4
from tests.tests_task05 import TestTask5
from tests.tests_task06 import TestTask6
from tests.tests_task07 import TestTask7
from tests.tests_task08 import TestTask8
from tests.tests_task09 import TestTask9
from tests.tests_task10 import TestTask10
from tests.tests_task11 import TestTask11
from tests.tests_task12 import TestTask12
from tests.tests_task13 import TestTask13
from tests.tests_task14 import TestTask14
from tests.tests_task15 import TestTask15
from tests.tests_task16 import TestTask16
from tests.tests_task17 import TestTask17
from tests.tests_task18 import TestTask18
from tests.tests_task19 import TestTask19
from tests.tests_task20 import TestTask20

# --- IMPORT AGENTI ---
from utils.llm_client import LLMClient
from agents.planner import PlannerAgent
from agents.coder import CoderAgent
from agents.tester import TesterAgent
from agents.commenter import CommenterAgent
from radon.metrics import mi_visit, ComplexityVisitor

# --- SETUP ---
load_dotenv()
token = os.getenv("HF_TOKEN")

if token:
  login(token=token)
else:
  print("Error: token not found in .env file")

TASK_NUMBER = 20
MAX_RETRIES = 10

# --- MODELLI ---
MODEL_ID_SMALL = "Qwen/Qwen2.5-Coder-1.5B-Instruct"
MODEL_ID_MISTRAL = "mistralai/Mistral-7B-Instruct-v0.3"
MODEL_ID_DISTILL_LLAMA = "deepseek-ai/DeepSeek-R1-Distill-Llama-8B"
MODEL_ID_QWEN = "Qwen/Qwen2.5-Coder-7B-Instruct"
MODEL_ID_QWEN_SA = "Qwen/Qwen2.5-Coder-14B-Instruct" 
MODEL_ID_MISTRAL_NEMO = "mistralai/Mistral-Nemo-Instruct-2407"

# --- CLIENTS ---
LLM_SMALL_CLIENT = LLMClient(model_id=MODEL_ID_SMALL)
LLM_MISTRAL_CLIENT = LLMClient(model_id=MODEL_ID_MISTRAL)
LLM_DISTILL_LLAMA_CLIENT = LLMClient(model_id=MODEL_ID_DISTILL_LLAMA)
LLM_QWEN = LLMClient(model_id=MODEL_ID_QWEN)
LLM_QWEN_SA = LLMClient(model_id=MODEL_ID_QWEN_SA)
LLM__MISTRAL_NEMO_CLIENT = LLMClient(model_id=MODEL_ID_MISTRAL_NEMO)

def clear_hf_cache():
  """ Cleans RAM and disk aggressively """
  print("\n[SYSTEM] Starting deep cleaning...")
  if torch.cuda.is_available():
    torch.cuda.empty_cache()
    torch.cuda.ipc_collect()
  gc.collect()
  
  cache_path = os.path.expanduser("~/.cache/huggingface/hub")
  if os.path.exists(cache_path):
    try:
      shutil.rmtree(cache_path)
      os.makedirs(cache_path, exist_ok=True)
      print("[SYSTEM] Disk cache Hugging Face deleted.")
    except Exception as e:
      print(f"[SYSTEM] Error in disk cleaning: {e}")
  else:
    print("[SYSTEM] No cache found on the disk.")
  print("[SYSTEM] Cleaning completed.\n")

def single_agent_arch(task_data, client):
  problem_description = task_data['prompt']
  prompt = f"""### Role: Expert Python Software Engineer.
  ### Task: Solve the following programming challenge.
  ### Problem: {problem_description}
  ### Strict Constraints:
  1. **IMPORTS**: Include necessary imports.
  2. **FORMAT**: Output ONLY the Python code inside ```python``` block.
  3. **NO TEXT**: No conversational filler.
  ### Implementation:"""
  
  try:
    response = client.generate_response(prompt)[0]
    code_match = re.search(r"```python\s*(.*?)```", response, re.DOTALL | re.IGNORECASE)
    if code_match:
      extracted_code = code_match.group(1).strip()
    else:
      extracted_code = response.strip()
    print("Single agent code generated.")
    return extracted_code
  except Exception as e:
    print(f"Error in Single Agent: {e}")
    return ""

def run_pipeline(task_data, planner_client, coder_client, tester_client, commenter_client, config_name):
  task_id = task_data['task_id']
  prompt = task_data['prompt']
  unit_tests = task_data['test']
  entry_point = task_data['entry_point']
  
  print(f"--- Running {config_name} on {task_id} ---")

  planner = PlannerAgent(llm_client=planner_client)
  plan = planner.plan(prompt)
  
  coder = CoderAgent(llm_client=coder_client)
  tester = TesterAgent(llm_client=tester_client)
  
  context = tester.prepare_review_context(prompt, unit_tests, entry_point)

  current_code = ""
  feedback = ""
  is_passing = False
  attempts = 0

  while attempts < MAX_RETRIES and not is_passing:
    current_code = coder.code(prompt, plan, current_code, feedback)
    print(f"  [DEBUG] Code generated:\n", current_code)
    
    success, error_msg = tester.perform_static_review(current_code, context)
    
    if success:
      is_passing = True
      print(f"  [Attempt {attempts+1}] Success!")
    else:
      feedback = f"The code failed tests. Error: {error_msg}"
      attempts += 1
      print(f"  [Attempt {attempts}] Failed.")
      print(f"  [DEBUG] error_msg: {error_msg}")

  commenter = CommenterAgent(llm_client=commenter_client)
  final_code = commenter.comment(current_code)
  return final_code

# --- METRICS AND SAVING ---

def save_intermediate_code(task_number, arch_number, code):
  """Saved the code made by every architeture in a secific file."""
  if not code: return
  
  # Creating the folder
  output_dir = "code"
  os.makedirs(output_dir, exist_ok=True)
  
  # e.g.: task01_2.py (Task 1, Architecture 2)
  filename = f"task{task_number:02}_{arch_number}.py"
  filepath = os.path.join(output_dir, filename)
  
  try:
      with open(filepath, "w") as f:
          f.write(code)
      print(f"[FILE] Saved architecture code to: {filepath}")
  except Exception as e:
      print(f"[FILE] Error saving file {filepath}: {e}")

def measure_execution_time(func, *args, iterations=100):
  start_time = time.perf_counter()
  try:
      for _ in range(iterations): func(*args)
  except: pass
  end_time = time.perf_counter()
  return (end_time - start_time) / iterations

def calculate_maintainability(code):
  try: return mi_visit(code, multi=True)
  except: return 0.0

def get_cyclomatic_complexity(code):
  try: 
    v = ComplexityVisitor.from_code(code)
    if not v.functions: return 1
    return max(f.complexity for f in v.functions) 
  except: return 1

def save_metrics_to_csv(task_number, arch_name, mi, cc, exec_time, score, passed, tests_ratio):
  filename = "metrics_results.csv"
  file_exists = os.path.exists(filename)
  
  with open(filename, 'a', newline='') as f:
    writer = csv.writer(f)
    if not file_exists:
      writer.writerow(['Task', 'Architecture', 'Passed', 'Tests_Ratio', 'MI', 'CC', 'Time', 'Score'])
    
    writer.writerow([
      task_number, 
      arch_name, 
      passed, 
      tests_ratio, 
      f"{mi:.2f}", 
      f"{cc:.2f}", 
      f"{exec_time:.6f}", 
      f"{score:.4f}"
    ])
  print(f"[METRICS] Saved for {arch_name} (Tests: {tests_ratio})")

def evaluate_and_log(code, arch_name, task_data, i):
  entry_point = task_data['entry_point']
  
  testers_map = {
    1: TestTask1, 2: TestTask2, 3: TestTask3, 4: TestTask4, 5: TestTask5,
    6: TestTask6, 7: TestTask7, 8: TestTask8, 9: TestTask9, 10: TestTask10,
    11: TestTask11, 12: TestTask12, 13: TestTask13, 14: TestTask14, 15: TestTask15,
    16: TestTask16, 17: TestTask17, 18: TestTask18, 19: TestTask19, 20: TestTask20
  }
  
  namespace = {}
  tests_ratio_str = "0/0"
  
  try:
    exec(code, namespace)
    func = namespace.get(entry_point)
    
    if func:
      tester_cls = testers_map.get(i+1)
      if tester_cls:
        tester = tester_cls(func)
        passed_tests, total_tests = tester.execute_tests()
        tests_ratio_str = f"{passed_tests}/{total_tests}"
        
        passed = (passed_tests == total_tests) and (total_tests > 0)
        
        if passed:
          try:
            params = tester.get_benchmark_input()
            exec_time = measure_execution_time(func, *params)
          except: exec_time = 0.001
          
          mi = calculate_maintainability(code)
          cc = get_cyclomatic_complexity(code)
          
          mi_norm = min(max(mi, 0), 100) / 100
          cc_norm = 1.0 if cc <= 1 else 1.0 / cc
          time_norm = 0.00001 / max(exec_time, 0.00001)
          score = (time_norm * 0.5) + (mi_norm * 0.3) + (cc_norm * 0.2)
          
          save_metrics_to_csv(i+1, arch_name, mi, cc, exec_time, score, "YES", tests_ratio_str)
          return score
        else:
          print(f"  {arch_name} failed tests: {tests_ratio_str}")
          save_metrics_to_csv(i+1, arch_name, -1, -1, -1, -1, "NO", tests_ratio_str)
          return 0.0
      else:
        print("  Tester class not found.")
        save_metrics_to_csv(i+1, arch_name, -1, -1, -1, -1, "NO_TESTER", "0/0")
        return 0.0
    else:
      print("  Function entry point not found.")
      save_metrics_to_csv(i+1, arch_name, -1, -1, -1, -1, "NO_FUNC", "0/0")
      return 0.0
          
  except Exception as e:
    print(f"  Error evaluating {arch_name}: {e}")
    save_metrics_to_csv(i+1, arch_name, -1, -1, -1, -1, "ERROR", "0/0")
    return 0.0

def main():
  print("Architectures:")
  print("1. Single Agent")
  print("2. Mistral -> Qwen")
  print("3. Mistral -> Mistral Nemo")
  print("4. DeepSeek -> Qwen")
  print("5. DeepSeek -> Mistral Nemo")

  for i in range(TASK_NUMBER):
    task_file = f"tasks/task_{i+1:02}.json"
    if not os.path.exists(task_file): continue

    with open(task_file, 'r') as f:
      task_data = json.load(f)
    
    print(f"\n===== TASK {i+1} =====")
    
    best_score = -1
    best_code = None
    best_arch = "None"

    # --- PIPELINE 1 ---
    clear_hf_cache()
    code1 = single_agent_arch(task_data, LLM_QWEN_SA)
    save_intermediate_code(i+1, 1, code1)
    score1 = evaluate_and_log(code1, "1_SingleAgent", task_data, i)
    if score1 > best_score: best_score, best_code, best_arch = score1, code1, "1"

    # --- PIPELINE 2 ---
    clear_hf_cache()
    code2 = run_pipeline(task_data, LLM_MISTRAL_CLIENT, LLM_QWEN_SA, LLM_QWEN, LLM_SMALL_CLIENT, "Arch 2")
    save_intermediate_code(i+1, 2, code2)
    score2 = evaluate_and_log(code2, "2_Mistral_Qwen", task_data, i)
    if score2 > best_score: best_score, best_code, best_arch = score2, code2, "2"

    # --- PIPELINE 3 ---
    clear_hf_cache()
    code3 = run_pipeline(task_data, LLM_MISTRAL_CLIENT, LLM__MISTRAL_NEMO_CLIENT, LLM_QWEN, LLM_SMALL_CLIENT, "Arch 3")
    save_intermediate_code(i+1, 3, code3)
    score3 = evaluate_and_log(code3, "3_Mistral_Nemo", task_data, i)
    if score3 > best_score: best_score, best_code, best_arch = score3, code3, "3"

    # --- PIPELINE 4 ---
    clear_hf_cache()
    code4 = run_pipeline(task_data, LLM_DISTILL_LLAMA_CLIENT, LLM_QWEN_SA, LLM_QWEN, LLM_SMALL_CLIENT, "Arch 4")
    save_intermediate_code(i+1, 4, code4)
    score4 = evaluate_and_log(code4, "4_DeepSeek_Qwen", task_data, i)
    if score4 > best_score: best_score, best_code, best_arch = score4, code4, "4"

    # --- PIPELINE 5 ---
    clear_hf_cache()
    code5 = run_pipeline(task_data, LLM_DISTILL_LLAMA_CLIENT, LLM__MISTRAL_NEMO_CLIENT, LLM_QWEN, LLM_SMALL_CLIENT, "Arch 5")
    save_intermediate_code(i+1, 5, code5)
    score5 = evaluate_and_log(code5, "5_DeepSeek_Nemo", task_data, i)
    if score5 > best_score: best_score, best_code, best_arch = score5, code5, "5"

    # --- SAVE BEST CODE ---
    if best_code:
      print(f"\nWINNER: Architecture {best_arch} with score {best_score:.4f}")
      output_path = f"code/task{i+1:02}.py" # overrides
      with open(output_path, "w") as f_out:
        f_out.write(best_code)
    else:
      print("No fully working code generated among all architectures.")

if __name__ == '__main__':
  main()