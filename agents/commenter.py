class CommenterAgent():
    def __init__(self, llm_client):
        self.llm_client = llm_client

        self.system_prompt = """You are a commenter agent in a multi-agent pipeline for code generation.
        Your role is to add professional documentation to the provided Python code.
        
        CRITICAL: Do NOT change the logic, variable names, or function signature.
        
        Your output must be the valid, executable Python code with the following additions:
        1. Docstrings: Add a Google-style docstring to the main function describing arguments and return values.
        2. Inline Comments: Add concise comments explaining complex steps.

        Guidelines:
        - Output ONLY the raw Python code.
        - Do NOT use Markdown formatting (no ```python blocks).
        - Do NOT add conversational text before or after the code.
        - Ensure the code remains valid and executable.
        """

    def comment(self, code):
        full_prompt = f"""{self.system_prompt}
                        CODE TO COMMENT:
                        {code}
                        """

        # Aumento max_new_tokens rispetto al planner perché qui
        # dobbiamo rigenerare l'intero codice sorgente + i commenti.
        response_text, _, _ = self.llm_client.generate_response(
            full_prompt, 
            max_new_tokens = 1024, 
            temperature = 0.2, 
            deterministic = True
        )

        # Pulizia base nel caso il modello inserisca comunque markdown
        if "```python" in response_text:
            response_text = response_text.replace("```python", "").replace("```", "")
        
        return response_text.strip()