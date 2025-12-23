import traceback

class TesterAgent:
    def __init__(self, llm_client):
        self.llm_client = llm_client

        self.system_prompt = """You are a tester agent in a multi-agent pipeline for code generation.
        Your role is to generate a robust Python test suite for a given problem.
        You will be given the Problem Description and some Basic Tests (assertions).
        
        Your goal is to produce a single executable Python block containing assertions.
        
        Your output must contain exactly the following sections, in this exact order and with these exact titles:

        IMPORTS:
        Include any necessary standard library imports (e.g., import math, from typing import List).
        
        TEST_SUITE:
        Write a series of 'assert' statements. 
        - Start with the provided Basic Tests.
        - Add NEW edge cases (empty inputs, large numbers, negative values).
        - Add NEW complex cases to verify logic robustness.
        - Do NOT use 'unittest.TestCase' classes. Use simple 'assert function(args) == expected' statements.
        - If the function returns a float, use 'abs(result - expected) < 1e-6'.

        Guidelines:
        - Do not implement the function itself, just call it.
        - The function to test will be available in the global scope (assume it's already defined).
        - Be concise.
        - Output strictly Python code in the sections.
        """

    def generate_tests(self, problem_prompt, basic_json_tests):
        """
        Genera i test case usando l'LLM, partendo dal problema e dai test base.
        """
        full_prompt = f"""{self.system_prompt}
                        PROBLEM:
                        {problem_prompt}

                        BASIC TESTS (from dataset):
                        {basic_json_tests}
                        """

        response_text, _, _ = self.llm_client.generate_response(
            full_prompt, 
            max_new_tokens=400,  
            temperature=0.2,    
            deterministic=True
        )

        return self._parse_and_clean_response(response_text)

    def _parse_and_clean_response(self, response_text):
        """
        Pulisce la risposta dell'LLM per estrarre solo il codice eseguibile.
        Rimuove i titoli delle sezioni (IMPORTS, TEST_SUITE) e formatta il codice.
        """

        clean_code = response_text.replace("IMPORTS:", "").replace("TEST_SUITE:", "")
        clean_code = clean_code.replace("```python", "").replace("```", "")
        return clean_code.strip()

    def test(self, code_to_test, test_suite_code):
        """
        Esegue il codice generato dal Coder contro la suite di test generata dal Tester.
        """
        namespace = {}
        try:

            exec(code_to_test, namespace)
            
            exec(test_suite_code, namespace)
            
            return True, "All generated tests passed."

        except AssertionError:
            return False, f"Assertion Failed:\n{traceback.format_exc()}"
        except SyntaxError:
            return False, f"Syntax Error in code or tests:\n{traceback.format_exc()}"
        except Exception:
            return False, f"Runtime Error:\n{traceback.format_exc()}"