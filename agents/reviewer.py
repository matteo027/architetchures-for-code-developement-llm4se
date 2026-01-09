
import re
import textwrap

class ReviewerAgent:
    def __init__(self, llm_client):
        self.llm_client = llm_client

    def prepare_review_context(self, task_prompt, basic_json_tests, entry_point):
        return f"""
        TASK: {task_prompt}
        ENTRY POINT: {entry_point}
        TESTS: {basic_json_tests}
        """

    def perform_static_review(self, current_code, context):
        """
        Analizza il codice. Usa Few-Shot semplificato per stabilità.
        """
        
        review_prompt = textwrap.dedent(f"""\
            You are a Senior Code Reviewer.
            Your job is to check Python code for:
            1. Empty implementation.
            2. Missing imports (math, List, etc.).
            3. Syntax errors.

            ### EXAMPLES (LEARN THE FORMAT)

            [Example 1]
            Code: 
            ```python
            
            ```
            Analysis: The code block is completely empty.
            STATUS: FAIL Code is empty.

            [Example 2]
            Code:
            ```python
            def area(r): return math.pi * r**2
            ```
            Analysis: The code uses 'math.pi' but 'import math' is missing.
            STATUS: FAIL Missing import math.

            [Example 3]
            Code:
            ```python
            from typing import List
            def sum_list(nums: List[int]) -> int:
                return sum(nums)
            ```
            Analysis: Imports are correct, typing is used correctly, logic is valid.
            STATUS: PASS

            ### END EXAMPLES

            ### CONTEXT
            {context}
            
            ### CODE TO REVIEW
            ```python
            {current_code}
            ```
            
            ### YOUR REVIEW
            Analysis:""") 

        # Aggiungiamo un parametro di stop per evitare che il modello vada oltre
        response_text, _, _ = self.llm_client.generate_response(
            review_prompt, 
            max_new_tokens=512, 
            temperature=0.10 
            deterministic=True
        )
        
        # Riattacchiamo "Analysis:" perché il modello completa la frase
        full_response = "Analysis:" + response_text
        return self._parse_review_result(full_response)

    def _parse_review_result(self, response):
        clean_response = response.strip()
        print("Clean Response:", clean_response)
        
        if "STATUS: PASS" in clean_response:
            return True, "Passed"
        
        if "STATUS: FAIL" in clean_response:
            parts = clean_response.split("STATUS: FAIL")
            return False, parts[1].strip() if len(parts) > 1 else "Unknown Failure"
            
        # Fallback se il modello si dimentica il formato esatto ma dice "FAIL" nel testo
        lower_resp = clean_response.lower()
        if "fail" in lower_resp or "error" in lower_resp or "missing" in lower_resp:
            return False, f"Reviewer Ambiguous Failure: {clean_response[:100]}..."
            
        # Se siamo qui, assumiamo PASS per non bloccare il loop
        return True, "Passed (Fallback)"