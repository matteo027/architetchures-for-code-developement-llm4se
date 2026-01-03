import re
from utils.llm_client import LLMClient
import textwrap

class CoderAgent:

  def __init__(self, llm_client: LLMClient):
    self.llm = llm_client

  def code(self, prompt: str, plan: str, current_code: str, feedback: str) -> str:
    """Generate or fix code based on plan and test feedback."""
    signature = self._extract_signature_from_plan(plan)

    if current_code and feedback:
        full_prompt = self._fix_prompt_template(
            prompt=prompt,
            plan=plan,
            current_code=current_code,
            feedback=feedback,
            signature=signature
        )
    else:
        full_prompt = self._generate_prompt_template(
            prompt=prompt,
            plan=plan,
            signature=signature
        )
    
    response = self.llm.generate_response(full_prompt)
    
    if isinstance(response, tuple):
        response = response[0]

            # DEBUG TEMPORANEO
    print("\n===== RAW LLM OUTPUT =====\n")
    print(response)
    print("\n==========================\n")

    return self._extract_clean_code(response)

  def _extract_signature_from_plan(self, plan: str) -> str:
    match = re.search(r"SIGNATURE:\s*(def\s+\w+\s*\(.*?\))", plan)
    if match:
        return match.group(1).strip()
    return "def function(...)"



  def _generate_prompt_template(self, *, prompt: str, plan: str, signature: str) -> str:
    return f"""You are an expert Python programmer.
    
    TASK DESCRIPTION:
    {prompt}
    
    INSTRUCTIONS:
    1. Include all necessary imports at the beginning (e.g., from typing import List).
    2. Follow the DETAILED PLAN step by step.
    3. Use exactly this FUNCTION SIGNATURE: {signature}

    DETAILED PLAN:
    {plan}
    
    Requirements:
    - Output ONLY valid Python code.
    - Do NOT include explanations, markdown, or extra text.
    - Start directly with the necessary imports.
    """


  def _fix_prompt_template(self, *, prompt: str, plan: str, current_code: str, feedback: str, signature: str) -> str:
    return f"""Fix the Python function based on test failures.

      ORIGINAL TASK:
      {prompt}

      FUNCTION SIGNATURE (MUST NOT BE CHANGED):
      {signature}

      DETAILED PLAN (follow exactly):
      {plan}

      PREVIOUS CODE (fix this):
      {current_code}

      TEST FAILURES:
      {feedback}

      Instructions:
      - Rewrite the function using EXACTLY the same signature above
      - Fix only logic or edge cases
      - Do NOT change the function name or parameters
      - Output ONLY valid Python code
      - No explanations or extra text
      """


  def _extract_clean_code(self, response: str) -> str:
    # Pulizia aggressiva iniziale dei backtick multipli
    # Rimuove tutti i blocchi markdown lasciando solo il contenuto testuale
    response = re.sub(r"```python", "", response, flags=re.IGNORECASE)
    response = re.sub(r"```", "", response)
    
    lines = response.splitlines()
    code_lines = []
    
    # Identifichiamo parole chiave che segnalano l'inizio del codice reale
    code_keywords = ("import ", "from ", "def ", "class ")
    
    in_code_block = False
    for line in lines:
        stripped = line.strip()
        
        # Inizia a raccogliere dalla prima riga di codice (import o def)
        if any(stripped.startswith(k) for k in code_keywords):
            in_code_block = True
            
        if in_code_block:
            # Continua a raccogliere finché le righe sono coerenti con il codice
            # (indentate, vuote, o nuove definizioni/import)
            if line.startswith(" ") or line.startswith("\t") or stripped == "" or any(stripped.startswith(k) for k in code_keywords):
                code_lines.append(line)
            else:
                break
            
    raw_code = "\n".join(code_lines)
    return textwrap.dedent(raw_code).strip()

  
  