
class RefinerAgent:
  def __init__(self, llm_client):
    self.client = llm_client

  def refine(self, current_code, feedback):
    system_instruction = "Refactor the following code based on the feedback provided. Ensure the fix is minimal and precise."
    return self.client.ask(f"{system_instruction}\n\nCode:\n{current_code}\n\nFeedback:\n{feedback}")