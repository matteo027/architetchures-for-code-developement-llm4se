import re
import textwrap

class TesterAgent:
    def __init__(self, llm_client):
        self.llm_client = llm_client

    def prepare_review_context(self, task_prompt, basic_json_tests, entry_point):
        """
        In questa modalità 'Static Review', non generiamo codice Python eseguibile.
        Invece, prepariamo il 'Contesto di Verifica' che il revisore userà.
        """
        context = f"""
        TASK DESCRIPTION:
        {task_prompt}

        ENTRY POINT FUNCTION:
        {entry_point}

        REQUIRED BEHAVIOR (JSON TESTS):
        {basic_json_tests}
        """
        return context

    def perform_static_review(self, current_code, context):
        """
        Analizza il codice staticamente usando l'LLM.
        Restituisce (True, "Passed") se il codice sembra corretto,
        altrimenti (False, Feedback).
        """
        
        # Costruiamo il prompt per il Revisore/Tester
        review_prompt = textwrap.dedent(f"""\
            You are a Senior Python QA Engineer performing a Static Code Analysis.
            
            ### GOAL
            Verify if the provided PYTHON CODE correctly solves the TASK and satisfies the REQUIRED BEHAVIOR.
            
            ### TASK CONTEXT
            {context}
            
            ### CANDIDATE CODE TO REVIEW
            ```python
            {current_code}
            ```
            
            ### INSTRUCTIONS
            1. Mentally trace the execution of the code with the provided JSON inputs.
            2. Check for syntax errors, logical bugs, or infinite loops.
            3. Check if the function signature matches the entry point exactly.
            4. Be STRICT. If there is any logical flaw, reject it.
            
            ### OUTPUT FORMAT
            You must end your response with exactly one of these two lines:
            - If code is correct: "STATUS: PASS"
            - If code is incorrect: "STATUS: FAIL" followed by a concise explanation of the bug.
            
            Start your response with your reasoning.
            """)

        # Chiamata all'LLM (Usa un numero di token sufficiente per il ragionamento)
        response_text, _, _ = self.llm_client.generate_response(
            review_prompt, 
            max_new_tokens=1024, 
            temperature=0.0, # Determinismo massimo per la review
            deterministic=True
        )

        # Parsing della risposta
        return self._parse_review_result(response_text)

    def _parse_review_result(self, response):
        """Analizza l'output testuale dell'LLM per determinare Pass/Fail."""
        
        # Pulizia generica whitespace
        clean_response = response.strip()
        
        # Strategia: Cerca l'ULTIMA occorrenza di STATUS: PASS/FAIL
        # Questo evita falsi positivi se il modello "pensa ad alta voce" prima di decidere.
        # Rfind restituisce l'indice dell'inizio della stringa trovata, o -1.
        pass_index = clean_response.rfind("STATUS: PASS")
        fail_index = clean_response.rfind("STATUS: FAIL")
        
        # Se non trova nulla
        if pass_index == -1 and fail_index == -1:
            # Fallback euristico generico
            lower_resp = clean_response.lower()
            if "incorrect" in lower_resp or "error" in lower_resp or "bug" in lower_resp or "fail" in lower_resp:
                 return False, f"Reviewer Ambiguous Failure: {clean_response}"
            return False, f"Format Error: Reviewer did not output STATUS: PASS/FAIL.\nFull Response: {clean_response}"

        # Se trova entrambi (raro, ma possibile nel ragionamento), vince l'ultimo scritto
        if pass_index > fail_index:
            return True, "Passed (Static Analysis Approved)"
        else:
            # È un FAIL. Estraiamo la spiegazione che segue lo status.
            # Prendiamo tutto il testo che viene DOPO "STATUS: FAIL"
            feedback_start = fail_index + len("STATUS: FAIL")
            feedback = clean_response[feedback_start:].strip()
            
            if not feedback:
                # Se lo status era l'ultima cosa, cerchiamo il feedback nelle righe precedenti
                # (Euristica opzionale, ma utile)
                feedback = clean_response[:fail_index].strip()[-500:] # Prendi gli ultimi 500 caratteri prima
            
            return False, feedback