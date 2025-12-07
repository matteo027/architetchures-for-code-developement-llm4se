from utils.llm_client import LLMClient
from agents.planner import PlannerAgent


MODEL_ID_LARGE = "meta-llama/Llama-2-7b-hf" # big LLM
MODEL_ID_SMALL = "gpt2"                      # small LLM

LLM_LARGE_CLIENT = LLMClient(model_id=MODEL_ID_LARGE)
LLM_SMALL_CLIENT = LLMClient(model_id=MODEL_ID_SMALL)