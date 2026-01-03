import json
import os
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

from utils.llm_client import LLMClient
from agents.planner import PlannerAgent
from agents.coder import CoderAgent
from agents.tester import TesterAgent
from agents.commenter import CommenterAgent
from radon.metrics import mi_visit
from radon.metrics import ComplexityVisitor
import time
from dotenv import load_dotenv
from huggingface_hub import login
import re
import gc
import torch
import shutil

# load variables from the .env file
load_dotenv()

token = os.getenv("HF_TOKEN")

if token:
  login(token=token)
else:
  print("Error: token not found in .env file")

TASK_NUMBER = 20
MAX_RETRIES = 10

MODEL_ID_SMALL = "Qwen/Qwen2.5-Coder-1.5B-Instruct" #coder LLM
MODEL_ID_MISTRAL = "mistralai/Mistral-7B-Instruct-v0.3" # planner LLM
MODEL_ID_DISTILL_LLAMA = "deepseek-ai/DeepSeek-R1-Distill-Llama-8B" # planner LLM
MODEL_ID_QWEN = "Qwen/Qwen2.5-Coder-7B-Instruct"
MODEL_ID_QWEN_SA = "Qwen/Qwen2.5-Coder-14B-Instruct"

LLM_SMALL_CLIENT = LLMClient(model_id=MODEL_ID_SMALL)
LLM_MISTRAL_CLIENT = LLMClient(model_id=MODEL_ID_MISTRAL)
LLM_DISTILL_LLAMA_CLIENT = LLMClient(model_id=MODEL_ID_DISTILL_LLAMA)
LLM_QWEN = LLMClient(model_id=MODEL_ID_QWEN)
LLM_QWEN_SA = LLMClient(model_id=MODEL_ID_QWEN_SA)

def clear_hf_cache():
  """ Cleans RAM and disk through an aggressive way """
  print("\n[SYSTEM] Starting deep cleaning...")
  
  # celans GPU's RAM
  if torch.cuda.is_available():
      torch.cuda.empty_cache()
      torch.cuda.ipc_collect()
  gc.collect()
  
  # cleans files on the disk (cacke)
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
  # The original task prompt from HumanEval
  problem_description = task_data['prompt']
    
  prompt = f"""### Role:
    You are an expert Python Software Engineer.

    ### Task:
    Solve the following programming challenge. You must ensure the code is production-ready, passes all edge cases, and includes necessary imports.

    ### Problem:
    {problem_description}

    ### Strict Constraints:
    1. **IMPORTS**: Always include necessary imports at the top (e.g., `from typing import List, Optional, Dict, Tuple`).
    2. **FORMAT**: Output ONLY the Python code. Do NOT include any conversational filler, explanations, or introductory text like "Sure, here is the code".
    3. **WRAPPING**: Wrap your code strictly within a single markdown block: ```python [code] ```.
    4. **SIGNATURE**: Do not change the function name or the provided signature format.
    5. **EDGE CASES**: Explicitly handle null inputs, empty lists, or extreme values as described.

    ### Implementation:
    """
  response = client.generate_response(prompt)[0]
  code_match = re.search(r"```python\s*(.*?)```", response, re.DOTALL | re.IGNORECASE)
  if code_match:
      extracted_code = code_match.group(1).strip()
  else:
      extracted_code = response.strip()
      
  print("Single agent code generated:", extracted_code)
  return extracted_code

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
  tests = tester.prepare_review_context(prompt, unit_tests, entry_point)

  current_code = ""
  feedback = ""
  is_passing = False
  attempts = 0

  while attempts < MAX_RETRIES and not is_passing:
    current_code = coder.code(prompt, plan, current_code, feedback)
    print(f"  Code generated: {current_code}")
    success, error_msg = tester.perform_static_review(current_code, tests)
    
    if success:
      is_passing = True
      print(f"  [Attempt {attempts+1}] Success!")
    else:
      feedback = f"The code failed tests. Error: {error_msg}"
      attempts += 1
      print(f"  [Attempt {attempts}] Failed. Retrying with feedback. Error message: {error_msg}")

  commenter = CommenterAgent(llm_client=commenter_client)
  final_code = commenter.comment(current_code)
  
  return final_code


def choose_code(codes, fun_name, task_number):
  best_code = None
  best_score = 0.0
  best_arch = -1
  testers = {
    1: TestTask1,
    2: TestTask2,
    3: TestTask3,
    4: TestTask4,
    5: TestTask5,
    6: TestTask6,
    7: TestTask7,
    8: TestTask8,
    9: TestTask9,
    10: TestTask10,
    11: TestTask11,
    12: TestTask12,
    13: TestTask13,
    14: TestTask14,
    15: TestTask15,
    16: TestTask16,
    17: TestTask17,
    18: TestTask18,
    19: TestTask19,
    20: TestTask20,
  }

  print(f"Task {task_number}")
  for (index, code) in enumerate(codes):
    namespace = {}
    try:
      exec(code, namespace)
      
      generated_function = namespace.get(fun_name)
      
      if generated_function:
        tester = testers[task_number](generated_function)
        passed, total = tester.execute_tests()
        print(f"\tTests for pipeline {index+1}\tpassed: {passed}, total: {total}")

        if passed == total:
          # going on with metrics
          parameters = tester.get_benchmark_input()
          execution_time = measure_execution_time(generated_function, *parameters)
          MI = calculate_maintainability(code)
          CC = get_cyclomatic_complexity(code)

          # normalization

          # [0, 100] -> [0, 1]
          mi_norm = min(max(MI, 0), 100) / 100
          # invese scale (1.9/cc)
          cc_norm = 1.0 if CC <= 1 else 1.0 / CC
          # invese scale (0.1 ms -> 1.0, then decreasing)
          ideal_time = 0.00001 
          time_norm = ideal_time / max(execution_time, ideal_time)
          print(f"\tMI: {MI}, CC: {CC}, execution_time: {execution_time}")
          # (50-30-20)
          score = (time_norm * 0.50) + (mi_norm * 0.30) + (cc_norm * 0.20)
          print(f"\nTotal score: {score}")

          # Save metrics to file
          save_metrics(task_number, index+1, MI, CC, execution_time, score)

          if best_code is None or score > best_score:
            best_code = code
            best_score = score
            best_arch = index+1
        
        else:
          save_metrics(task_number, index+1, -1, -1, -1, -1) # not passed

      else:
        print(f"\t[ERROR] Unable to retreive the generated function.")
    except Exception as e:
      print(f"\t[DEBUG]: Error during the execution of exec (the function is not executable): {e}")

  return best_code, best_arch

def measure_execution_time(func, *args, iterations=100):
  start_time = time.perf_counter() # max precision
  
  for _ in range(iterations):
    func(*args)
    
  end_time = time.perf_counter()
  # mean execution time, in seconds
  return (end_time - start_time) / iterations

def calculate_maintainability(code):
  try:
    # returns a score in range [0, 100]
    score = mi_visit(code, multi=True)
    return score
  except Exception as e:
    print(f"\t[DEBUG]: Error calculating MI: {e}")
    return 0.0

def get_cyclomatic_complexity(code):
  try:
    v = ComplexityVisitor.from_code(code)
    # average complexity among the functions in the block (just 1, in our case)
    complexities = [obj.complexity for obj in v.functions]
    
    return max(complexities) if complexities else 1
  except Exception as e:
    print(f"[DEBUG]: Error calculating CC: {e}")
    return 1

def save_metrics(task_number, architecture_index, mi, cc, execution_time, score):
  """Save metrics to a CSV file"""
  import csv
  metrics_file = "metrics_results.csv"
  file_exists = os.path.exists(metrics_file)
  
  with open(metrics_file, 'a', newline='') as f:
    writer = csv.writer(f)
    
    # Write header if file doesn't exist
    if not file_exists:
      writer.writerow(['Task', 'Architecture', 'MI', 'CC', 'Execution_Time', 'Score'])
    
    writer.writerow([task_number, architecture_index, f"{mi:.2f}", f"{cc:.2f}", f"{execution_time:.6f}", f"{score:.4f}"])
  
  print(f"\tMetrics saved to {metrics_file}")

def main():

  print("Architetures:")
  print("1.\tSingle agent")
  print("2.\tPlanner (Mistral7b) -> Coder (Qwen7B) -> Tester -> Commenter")
  print("3.\tPlanner (Mistral7b) -> Coder (MIstral7B) -> Tester -> Commenter")
  print("4.\tPlanner (DeepSeek) -> Coder (Qwen7B) -> Tester -> Commenter")
  print("5.\tPlanner (DeepSeek) -> Coder (Mistral7B) -> Tester -> Commenter")
  print("6.\tPlanner -> Coder -> Reviwer -> Refiner")

  for i in range(TASK_NUMBER):
    task_file = f"tasks/task_{i+1:02}.json"
    if not os.path.exists(task_file): continue

    with open(task_file, 'r') as f:
      task_data = json.load(f)
    
    print(f"Task {i+1}")
    results = list()

    # (pre) cleaning
    clear_hf_cache()

    result = single_agent_arch(task_data, LLM_QWEN_SA)
    results.append(result)
    result = run_pipeline(task_data, LLM_MISTRAL_CLIENT, LLM_QWEN, LLM_QWEN, LLM_SMALL_CLIENT, "Architeture 2")
    results.append(result)
    result = run_pipeline(task_data, LLM_DISTILL_LLAMA_CLIENT, LLM_QWEN, LLM_QWEN, LLM_SMALL_CLIENT, "Architeture 3")
    results.append(result)
    result = run_pipeline(task_data, LLM_DISTILL_LLAMA_CLIENT, LLM_MISTRAL_CLIENT, LLM_MISTRAL_CLIENT, LLM_SMALL_CLIENT, "Architeture 5")
    results.append(result)

    # evaluation
    best_code, best_arch = choose_code(results, task_data['entry_point'], i+1)

    if best_code:
      print(f"\nThe best code has been generated by architectre {best_arch}.")

      output_path = f"code/task{i+1:02}.py"
      os.makedirs("code", exist_ok=True)
      with open(output_path, "w") as f_out:
        f_out.write(best_code)
    else:
      print("No architecture has generated a working code.")

if __name__ == '__main__':
  main()
