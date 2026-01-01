class RefinerAgent:
  def __init__(self, llm_client):
    self.client = llm_client

  def refine(self, current_code, feedback, original_prompt):
    """
    Refines the code based on the given feedback, keeping in "mind" the context of the original problem
    """
    system_instruction = (
        "You are an expert code refiner. Your goal is to fix the code provided below.\n"
        "1. Analyze the FEEDBACK (Test errors and Reviewer comments).\n"
        "2. Ensure the code still solves the ORIGINAL TASK.\n"
        "3. Output ONLY the fixed Python code."
    )
    
    full_prompt = (
        f"{system_instruction}\n\n"
        f"### ORIGINAL TASK:\n{original_prompt}\n\n"
        f"### CURRENT CODE:\n{current_code}\n\n"
        f"### FEEDBACK:\n{feedback}\n\n"
        f"### FIXED CODE:"
    )
    
    return self.client.generate_response(full_prompt)[0] 