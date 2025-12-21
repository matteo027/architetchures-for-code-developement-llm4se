
class ReviewerAgent:
  def __init__(self, llm_client):
    self.client = llm_client

  def review(self, code, prompt):
    system_instruction = "Verify code logic and efficiency. Identify bugs without executing. Give a verdict: APPROVED or NEEDS_REVISION."
    return self.client.ask(f"{system_instruction}\n\nCode:\n{code}\n\nOriginal Task:\n{prompt}")
