import json
import os
from tests.tests_task1 import TestTask1
from tests.tests_task10 import TestTask10
from tests.tests_task2 import TestTask2
from tests.tests_task3 import TestTask3
from tests.tests_task4 import TestTask4
from tests.tests_task5 import TestTask5
from tests.tests_task6 import TestTask6
from tests.tests_task7 import TestTask7
from tests.tests_task8 import TestTask8
from tests.tests_task9 import TestTask9
from utils.llm_client import LLMClient
from agents.planner import PlannerAgent
from agents.coder import CoderAgent
from agents.tester import TesterAgent
from agents.commenter import CommenterAgent
from agents.refiner import RefinerAgent
from agents.reviewer import ReviewerAgent
from radon.metrics import mi_visit
from radon.metrics import ComplexityVisitor
import time

TASK_NUMBER = 10
MAX_RETRIES = 10

MODEL_ID_LARGE = "meta-llama/Llama-2-7b-hf" # big LLM
MODEL_ID_SMALL = "gpt2"                      # small LLM
MODEL_ID_MISTRAL = "mistralai/Mistral-7B-Instruct-v0.3" # planner LLM

LLM_LARGE_CLIENT = LLMClient(model_id=MODEL_ID_LARGE)
LLM_SMALL_CLIENT = LLMClient(model_id=MODEL_ID_SMALL)
LLM_MISTRAL_CLIENT = LLMClient(model_id=MODEL_ID_MISTRAL)

# from the paper
MODEL_ID_LLAMA = "meta-llama/Llama-3-70B-Instruct"
MODEL_ID_CLAUDE = "claude-3-5-sonnet-20240620"
MODEL_ID_O1 = "openai/o1-preview"
#MODEL_ID_MISTRAL = "mistralai/Mistral-7B-Instruct-v0.3"

LLM_LLAMA = LLMClient(model_id=MODEL_ID_LLAMA)              # planner
LLM_CLAUDE = LLMClient(model_id=MODEL_ID_CLAUDE)            # coder
LLM_O1 = LLMClient(model_id=MODEL_ID_O1)                    # reviewer
LLM_MISTRAL_CLIENT = LLMClient(model_id=MODEL_ID_MISTRAL)   # refiner

def single_agent_arch(task_data, client):
  return client.ask(task_data['prompt'])

def run_pipeline(task_data, planner_client, coder_client, config_name):
  task_id = task_data['task_id']
  prompt = task_data['prompt']
  unit_tests = task_data['test']
  
  print(f"--- Running {config_name} on {task_id} ---")

  planner = PlannerAgent(llm_client=planner_client)
  plan = planner.plan(prompt)
 
  coder = CoderAgent(llm_client=coder_client)
  tester = TesterAgent()
  
  current_code = ""
  feedback = ""
  is_passing = False
  attempts = 0

  while attempts < MAX_RETRIES and not is_passing:
    current_code = coder.code(prompt, plan, current_code, feedback)
    
    success, error_msg = tester.test(current_code, unit_tests)
    
    if success:
      is_passing = True
      print(f"  [Attempt {attempts+1}] Success!")
    else:
      feedback = f"The code failed tests. Error: {error_msg}"
      attempts += 1
      print(f"  [Attempt {attempts}] Failed. Retrying with feedback...")

  commenter = CommenterAgent(llm_client=LLM_SMALL_CLIENT)
  final_code = commenter.comment(current_code)
  
  return final_code

def run_pipeline_paper(task_data, planner_client, coder_client, reviewer_client, refiner_client):
  task_id = task_data['task_id']
  prompt = task_data['prompt']
  unit_tests = task_data['test']
  
  print(f"--- Running Paper Architecture (Reviewer-Refiner) on {task_id} ---")

  planner = PlannerAgent(llm_client=planner_client)
  plan = planner.plan(prompt)
  
  coder = CoderAgent(llm_client=coder_client)
  reviewer = ReviewerAgent(llm_client=reviewer_client)
  refiner = RefinerAgent(llm_client=refiner_client)
  tester = TesterAgent()
  
  current_code = ""
  feedback = ""
  is_passing = False
  attempts = 0

  while attempts < MAX_RETRIES and not is_passing:
    if attempts == 0:
      current_code = coder.code(prompt, plan, current_code, feedback)
    else:
      current_code = refiner.refine(current_code, feedback)
    
    review_feedback = reviewer.review(current_code, prompt)
    
    success, error_msg = tester.test(current_code, unit_tests)
    
    if success and "APPROVED" in review_feedback.upper():
      is_passing = True
      print(f"  [Attempt {attempts+1}] Success & Approved!")
    else:
      feedback = f"Test Error: {error_msg}\nReview Feedback: {review_feedback}"
      attempts += 1
      print(f"  [Attempt {attempts}] Failed or Needs Refinement. Retrying...")

  final_code = current_code
  
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
    # 11: TestTask11,
    # 12: TestTask12,
    # 13: TestTask13,
    # 14: TestTask14,
    # 15: TestTask15,
    # 16: TestTask16,
    # 17: TestTask17,
    # 18: TestTask18,
    # 19: TestTask19,
    # 20: TestTask20,
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

          # (50-30-20)
          score = (time_norm * 0.50) + (mi_norm * 0.30) + (cc_norm * 0.20)
          
          if best_code is None or score > best_score:
            best_code = code
            best_score = score
            best_arch = index+1

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

def __main__():

  print("Architetures:")
  print("1.\tSingle agent")
  print("2.\tPlanner (small) -> Coder (big) -> Tester -> Commenter")
  print("3.\tPlanner (big) -> Coder (small) -> Tester -> Commenter")
  print("4.\tPlanner -> Coder -> Reviwer -> Refiner")

  for i in range(TASK_NUMBER):
    task_file = f"tasks/task{i+1}.json"
    if not os.path.exists(task_file): continue

    with open(task_file, 'r') as f:
      task_data = json.load(f)
    
    results = list()

    result = single_agent_arch(task_data, LLM_LARGE_CLIENT)
    results.append(result)
    result = run_pipeline(task_data, LLM_MISTRAL_CLIENT, LLM_LARGE_CLIENT, "Architeture 2")
    results.append(result)
    result = run_pipeline(task_data, LLM_LARGE_CLIENT, LLM_SMALL_CLIENT, "Architeture 3")
    results.append(result)
    result = run_pipeline_paper(task_data, LLM_LLAMA, LLM_CLAUDE, LLM_O1, LLM_MISTRAL_CLIENT)
    results.append(result)

    # evaluation
    best_code, best_arch = choose_code(results, task_data['entry_point'], i+1)

    if best_code:
      print(f"\nThe best code has been generated by architectre {best_arch}.")

      output_path = f"code/task{i+1}.py"
      os.makedirs("code", exist_ok=True)
      with open(output_path, "w") as f_out:
        f_out.write(best_code)
    else:
      print("No architecture has generated a working code.")
