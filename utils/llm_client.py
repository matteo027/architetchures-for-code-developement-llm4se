import os
import time
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
from dotenv import load_dotenv

load_dotenv()

class LLMClient:
  """
  Manages the upload and the interaction with LLM models,
  ensouring efficienc through caching and tracking token usage.
  """
  def __init__(self, model_id: str):
    self.model_id = model_id
        
    self.api_keys = self._load_api_keys()
    if not self.api_keys:
      raise ValueError("Nessuna chiave GEMINI_API_KEY trovata nel file .env")
    
    self.current_key_index = 0
    self._configure_current_key()
    
    self.model = genai.GenerativeModel(self.model_id)
  
  def _load_api_keys(self) -> list[str]:
    keys = []
    if os.getenv("GEMINI_API_KEY"):
      keys.append(os.getenv("GEMINI_API_KEY"))
    
    # other keys
    for key, value in os.environ.items():
      if key.startswith("GEMINI_API_KEY") and value not in keys:
        keys.append(value)
    return keys

  def _configure_current_key(self):
    current_key = self.api_keys[self.current_key_index]
    genai.configure(api_key=current_key)
    print(f"[DEBUG] Switched to API Key index: {self.current_key_index}")

  def _rotate_key(self):
    self.current_key_index = (self.current_key_index + 1) % len(self.api_keys)
    self._configure_current_key()

  def generate_response(self, prompt: str, max_new_tokens: int = 500, temperature: float = 0.7, deterministic: bool = False, **kwargs) -> tuple[str, int, int]:
    """
    sends a prompt to the model, return the response and the tokens used/returned

    Returns: (response_text, input_tokens, generated_tokens)
    """
    final_temp = 0.0 if deterministic else temperature
    
    generation_config = genai.types.GenerationConfig(
      max_output_tokens=max_new_tokens,
      temperature=final_temp,
    )

    safety_settings = {
      HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
      HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
      HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
      HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
    }

    try:
      # API call
      response = self.model.generate_content(
        prompt,
        generation_config=generation_config,
        safety_settings=safety_settings
      )
        
      try:
        response_text = response.text
      except ValueError:
        print(f"[GEMINI] Response blocked. Safety ratings: {response.prompt_feedback}")
        return "", 0, 0

      # 5. Estrazione Metriche Token (Usage Metadata)
      input_tokens = 0
      generated_tokens = 0
      
      if response.usage_metadata:
          input_tokens = response.usage_metadata.prompt_token_count
          generated_tokens = response.usage_metadata.candidates_token_count
      
      # rate limit for Gemini's constraints
      time.sleep(1)

      return response_text, input_tokens, generated_tokens

    except Exception as e:
      print(f"[GEMINI] Error generating response: {e}")
      return "", 0, 0
    
