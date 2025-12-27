class PlannerAgent():
    def __init__(self, llm_client):
        self.llm_client = llm_client

        self.system_prompt = """You are a planner agent in a multi-agent pipeline for code generation.
        Your role is to analyze the programming problem and produce a structured plan.
        Do NOT write full code.
        Your output must contain exactly the following sections, in this exact order and with these exact titles:

        SIGNATURE:
        Write only the Python function signature on a single line. The SIGNATURE line must start with 'def ' and contain only the function signature. 

        PLAN:
        Describe the algorithm as numbered steps (1, 2, 3, ...).

        EDGE_CASES:
        List realistic corner cases using bullet points.

        Guidelines:
        - Do not write full code.
        - Do not include imports or docstrings.
        - Be concise and precise.
        - If any section is missing or formatted differently, the output is invalid.
        - Do not include conversational phrases.
        """
      
    def plan(self, prompt):
        full_prompt = f"""{self.system_prompt}
                        PROBLEM:
                        {prompt}
                        """

        response_text, _, _ = self.llm_client.generate_response(
            full_prompt, 
            max_new_tokens = 400, 
            temperature = 0.1, 
            deterministic = True) 

        return response_text
