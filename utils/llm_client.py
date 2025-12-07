from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

class LLMClient:
  """
  Manages the upload and the interaction with LLM models,
  ensouring efficienc through caching and tracking token usage.
  """
  def __init__(self, model_id: str):
    self.model_id = model_id
    # tokenizer and models already loaded (caching)
    self.cache = {}
    self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

  def _load_model(self):
    """loads the model and the tokenizer only if thery're already cached"""
    if self.model_id not in self.cache:
      print(f"[llm_client] Loading model {self.model_id}...")
      
      tokenizer = AutoTokenizer.from_pretrained(self.model_id)

      model = AutoModelForCausalLM.from_pretrained(
        self.model_id, 
        torch_dtype=torch.float16, 
        device_map="auto"
      )
      model.eval() # inference

      self.cache[self.model_id] = {'model': model, 'tokenizer': tokenizer}
    
      return self.cache[self.model_id]['model'], self.cache[self.model_id]['tokenizer']
    else:
      print(f"[llm_client] Model {self.model_id} already in cache.")

  def generate_response(self, prompt: str, max_new_tokens: int = 200, temperature: float = 0.7, deterministic: bool = False) -> tuple[str, int, int]:
    """
    sends a prompt to the model, return the response and the tokens used/returned

    Returns: (response_text, input_tokens, generated_tokens)
    """
    model, tokenizer = self._load_model()
    
    # input tokenization
    inputs = tokenizer(prompt, return_tensors="pt", truncation=True)
    input_ids = inputs['input_ids'].to(self.device)
    input_tokens = input_ids.shape[1]

    # output generation
    with torch.no_grad(): # no gradient for intference
      outputs = model.generate(
        input_ids,
        max_new_tokens=max_new_tokens,
        temperature=temperature,
        # deterministic
        do_sample=(temperature > 1e-6) and (not deterministic), 
        pad_token_id=tokenizer.eos_token_id,
      )
    
    # note: outputs[0] is the complete sequence (input + output)
    generated_ids = outputs[0][input_tokens:] 
    generated_tokens = generated_ids.shape[0]

    # output decoding
    full_response = tokenizer.decode(outputs[0], skip_special_tokens=True).strip()

    response_text = full_response[len(prompt):].strip()

    return response_text, input_tokens, generated_tokens