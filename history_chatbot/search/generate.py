
from transformers import AutoModelForCausalLM, AutoTokenizer, AutoModel

pipeline_kwargs={
    "temperature": 0.1,
    "max_new_tokens": 4096,
    "top_k": 1
}
  
if __name__ == "__main__":
    model_path = "/Users/trunghuynh/History_chatbot/history_chatbot/models/GemSUra-2B"
    model = AutoModelForCausalLM.from_pretrained(model_path)