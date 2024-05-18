from transformers import AutoTokenizer, AutoModel 
from datasets import load_dataset,Dataset
import pandas as pd
import torch


model_ckpt = "/Users/trunghuynh/History_chatbot/history_chatbot/models/bge-m3"
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
tokenizer = AutoTokenizer.from_pretrained(model_ckpt)
model = AutoModel.from_pretrained(model_ckpt)

def cls_pooling(model_output):
    return model_output.last_hidden_state[:, 0]
def get_embeddings(text_list):
    encoded_input = tokenizer(
        text_list, padding=True, truncation=True, return_tensors="pt"
    )
    encoded_input = {k: v.to(device) for k, v in encoded_input.items()}
    model_output = model(**encoded_input)
    return cls_pooling(model_output)

question = "hồ chí minh sinh ngày bao nhiêu"
question_embedding = get_embeddings([question]).cpu().detach().numpy()
question_embedding.shape
issues_dataset = load_dataset("json", data_files="dataset/data.json", split="train")
issues_dataset.load_faiss_index('embeddings', 'dataset/history_index.faiss')
scores, samples = issues_dataset.get_nearest_examples(
    "embeddings", question_embedding, k=5
)

samples_df = pd.DataFrame.from_dict(samples)
samples_df["scores"] = scores
samples_df.sort_values("scores", ascending=True, inplace=True)
for _, row in samples_df.iterrows():
    print(f"TITLE: {row.title}")
    print(f"SCORE: {row.scores}")
    print(f"CONTEXT: {row.content}")
    print(f"CONTEXT: {row.type}")
    print("=" * 50)
    print()


def rerank():
    from rank_bm25 import BM25Okapi
    tokenized_corpus = []  # Empty list to store tokenized texts

    result = {}
    tokenized_corpus = [] 
    for item in samples["content"]:
        tokenized_corpus.append(item.split(" "))
    bm25 = BM25Okapi(tokenized_corpus)
    tokenized_query = question.split(" ")
    doc_scores = bm25.get_scores(tokenized_query)
    result["contents"] = samples["content"]
    result["scores"] = doc_scores
    return result
    