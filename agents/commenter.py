import textwrap
import re

class CommenterAgent:
    def __init__(self, llm_client):
        self.llm_client = llm_client

        # PROMPT OTTIMIZZATO: Seniority alta, focus su intenti algoritmici
        self.system_prompt = textwrap.dedent("""\
            You are a Senior Python Software Engineer specializing in code maintainability.
            Your role is to refine the documentation of existing code without altering its behavior.
            
            STRICT GUIDELINES:
            1. **NO TRIVIAL COMMENTS**: Do NOT explain basic Python syntax or obvious operations (e.g., do NOT comment "increment i" or "import list").
            2. **FOCUS ON ALGORITHMIC INTENT**: Inline comments must appear ONLY for complex logic, non-obvious mathematical formulas, or specific edge-case handling. Explain the "WHY", not the "WHAT".
            3. **COMPACT DOCSTRINGS**: Use Google-style docstrings. Prioritize a clear, single-line summary. Avoid verbose descriptions for obvious arguments.
            4. **PRESERVE LOGIC**: Do NOT change variable names, function signatures, or executable code.
            
            ### EXAMPLES
            
            [BAD - Do NOT do this]
            def add(a, b):
                # Returns the sum
                return a + b # Adds a and b

            [GOOD - Do this]
            def calculate_moving_average(data, window):
                #Computes simple moving average using a sliding window.
                cumsum = [0]
                # Efficiently calculate sum using prefix array to avoid O(N*W) complexity
                for i, x in enumerate(data, 1):
                    cumsum.append(cumsum[i-1] + x)
            """)

    def comment(self, code):
        full_prompt = textwrap.dedent(f"""\
            {self.system_prompt}
            
            CODE TO DOCUMENT:
            ```python
            {code}
            ```
            
            INSTRUCTIONS:
            Return the code with:
            - A concise docstring for the main function/class.
            - 1-2 essential inline comments ONLY if logic is complex.
            - Output must be strictly valid Python code inside a markdown block.
            """)

        response_text, _, _ = self.llm_client.generate_response(
            full_prompt, 
            max_new_tokens=1024, 
            temperature=0.2, 
            deterministic=True
        )

        return self._clean_response(response_text, original_code=code)

    def _clean_response(self, response_text, original_code):
        # Cerca il blocco di codice
        match = re.search(r"```python\s*(.*?)```", response_text, re.DOTALL | re.IGNORECASE)
        if match:
            code = match.group(1)
        else:
            match = re.search(r"```\s*(.*?)```", response_text, re.DOTALL)
            code = match.group(1) if match else response_text
            
        code = code.strip()
        
        # Se il commenter ha fallito o restituito vuoto, restituiamo il codice originale
        if not code:
            return original_code
            
        return code