import json
import os
import re
import time
import csv
#from dotenv import load_dotenv
#from huggingface_hub import login

# --- IMPORT AGENTS ---
from utils.llm_client import LLMClient
from agents.planner import PlannerAgent
from agents.coder import CoderAgent
from agents.reviewer import ReviewerAgent
from agents.commenter import CommenterAgent
from radon.metrics import mi_visit, ComplexityVisitor


#load_dotenv()

TASK_NUMBER = 20
MAX_RETRIES = 10

# --- MODEL ---
MODEL_ID = "gemini-2.5-flash"

# --- CLIENT ---
LLM_CLIENT = LLMClient(model_id=MODEL_ID)

# Single agent architecture implementation
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
    response = client.generate_response(prompt, max_new_tokens=1024, temperature=0.3)[0]
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

# Multi agent architecture implementation
def run_pipeline(task_data, client, config_name):
  task_id = task_data['task_id']
  prompt = task_data['prompt']
  unit_tests = task_data['test']
  entry_point = task_data['entry_point']
  
  print(f"--- Running {config_name} on {task_id} ---")

  planner = PlannerAgent(llm_client=client)
  plan = planner.plan(prompt)
  
  coder = CoderAgent(llm_client=client)
  reviewer = ReviewerAgent(llm_client=client)

  context = reviewer.prepare_review_context(prompt, unit_tests, entry_point)

  current_code = ""
  feedback = ""
  is_passing = False
  attempts = 0

  # Try up to MAX_RETRIES to get passing code
  while attempts < MAX_RETRIES and not is_passing:
    current_code = coder.code(prompt, plan, current_code, feedback)
    print(f"  [DEBUG] Code generated:\n", current_code)
    
    success, error_msg = reviewer.perform_static_review(current_code, context)
    
    if success:
      is_passing = True
      print(f"  [Attempt {attempts+1}] Success!")
    else:
      feedback = f"The code failed tests. Error: {error_msg}"
      attempts += 1
      print(f"  [Attempt {attempts}] Failed.")
      print(f"  [DEBUG] error_msg: {error_msg}")

  # If not passing, return empty code
  if not is_passing:
    return ""
  
  commenter = CommenterAgent(llm_client=client)
  final_code = commenter.comment(current_code)
  return final_code

# --- METRICS AND SAVING ---
def save_intermediate_code(task_number, arch_number, code):
  """Saved the code made by every architeture in a specific file."""
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
'''
def measure_execution_time(func, *args, iterations=100):
  start_time = time.perf_counter()
  try:
      for _ in range(iterations): func(*args)
  except: pass
  end_time = time.perf_counter()
  return (end_time - start_time) / iterations
'''
def calculate_maintainability(code):
  try: return mi_visit(code, multi=True)
  except: return 0.0

def get_cyclomatic_complexity(code):
  try: 
    v = ComplexityVisitor.from_code(code)
    if not v.functions: return 1
    return max(f.complexity for f in v.functions) 
  except: return 1

def save_metrics_to_csv(task_number, arch_name, mi, cc, exec_time, score):
  filename = "metrics_results.csv"
  file_exists = os.path.exists(filename)
  
  with open(filename, 'a', newline='') as f:
    writer = csv.writer(f)
    if not file_exists:
      writer.writerow(['Task', 'Architecture', 'MI', 'CC', 'Time', 'Score'])
    
    writer.writerow([
    task_number,
    arch_name,
    f"{mi:.2f}", 
    f"{cc:.2f}", 
    f"{exec_time:.6f}", 
    f"{score:.4f}"
    ])
  print(f"[METRICS] Saved for {arch_name} of Task {task_number})")

def evaluate_and_log(code, arch_name, task_data, i):
  entry_point = task_data['entry_point']
  
  if not code:
    print(f"  No code generated for {arch_name}.")
    save_metrics_to_csv(i+1, arch_name, -1, -1, -1, -1)
    return -1
  elif entry_point not in code:
    print(f"  Function entry point '{entry_point}' not found in {arch_name}.")
    save_metrics_to_csv(i+1, arch_name, -1, -1, -1, -1)
    return -1
  else:
    mi = calculate_maintainability(code)
    cc = get_cyclomatic_complexity(code)
    
    mi_norm = min(max(mi, 0), 100) / 100
    cc_norm = 1.0 if cc <= 1 else 1.0 / cc
    #exec_time = measure_execution_time(LLM_CLIENT.execute_code, code, entry_point, task_data['test'], iterations=10)
    #exec_time_default = 0.001
    #time_norm = 0.00001 / max(exec_time_default, 0.00001)
    #score = (time_norm * 0.5) + (mi_norm * 0.3) + (cc_norm * 0.2)
    score = (mi_norm * 0.5) + (cc_norm * 0.5)
    #save_metrics_to_csv(i+1, arch_name, mi, cc, exec_time, score)
    save_metrics_to_csv(i+1, arch_name, mi, cc, 0, score)
    return score


def main():
  print("Architectures:")
  print("1. Single Agent")
  print("2. Multi Agent")

  for i in range(TASK_NUMBER):
    task_file = f"tasks/task_{i+1:02}.json"
    if not os.path.exists(task_file): continue

    with open(task_file, 'r') as f:
      task_data = json.load(f)
    
    print(f"\n===== TASK {i+1} =====")

    # --- Single Agent ---
    code1 = single_agent_arch(task_data, LLM_CLIENT)
    save_intermediate_code(i+1, 1, code1)
    evaluate_and_log(code1, "1_SingleAgent", task_data, i)

    # --- Multi Agent ---
    code2 = run_pipeline(task_data, LLM_CLIENT, "2_MultiAgent")
    save_intermediate_code(i+1, 2, code2)
    evaluate_and_log(code2, "2_MultiAgent", task_data, i) 

if __name__ == '__main__':
  main()
