from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
import json
from .models import *
from pyvi import ViTokenizer
from pathlib import Path
from transformers import AutoTokenizer, AutoModel
import torch
from datasets import Dataset,load_dataset
from django.views.decorators.csrf import csrf_exempt
from tqdm import trange
from langchain_text_splitters import RecursiveCharacterTextSplitter
from rank_bm25 import BM25Okapi
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

model_path = str(BASE_DIR)+"/models/vietnamese-bi-encoder"
tokenizer = AutoTokenizer.from_pretrained(model_path)
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = AutoModel.from_pretrained(model_path)


def import_data(data, image):
    # path= "books/dataset/history_knowledge_base.json"
    # with open(path) as file:
        # data = json.load(file)
        grade = list(data.keys())
        grade_model = Grade()
        g = grade[0]
        if Grade.objects.filter(name=g):
            return HttpResponse("Nội dung sách đã tồn tại")
        else:
            grade_model.name=g
            grade_model.image=image

            grade_model.save()

            chapter = data[g].keys()
            for ch in chapter:
                chapter_model = Chapter()
                chapter_model.name = ch
                chapter_model.grade = grade_model
                chapter_model.save()

                lession = data[g][ch].keys()
                for l in lession:
                    lession_model = Lesson()
                    lession_model.name = l
                    lession_model.chapter = chapter_model
                    lession_model.save()

                    title = data[g][ch][l].keys()
                    for t in title:
                        title_model = Title()
                        title_model.name = t
                        title_model.content = data[g][ch][l][t]
                        title_model.lesson = lession_model
                        title_model.save()
        return HttpResponse("done")
    
def retrieval(request, query):

    return HttpResponse("done")


def custom_encoder(obj):
    if isinstance(obj, uuid.UUID):
        return str(obj)
    raise TypeError(f"Object of type {type(obj)} is not JSON serializable")
def word_segmented(request):
    data = []
    text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1024,
                chunk_overlap=100,
                length_function=len,
                separators=[
                    "\n\n",
                    "\n",
                    " ",
                    ".",
                    ",",
                    "\u200b",  # Zero-width space
                    "\uff0c",  # Fullwidth comma
                    "\u3001",  # Ideographic comma
                    "\uff0e",  # Fullwidth full stop
                    "\u3002",  # Ideographic full stop
                    "",
                ],
                # Existing args
            )

    grades = Grade.objects.all()
    for grade in grades:
        chapters = Chapter.objects.filter(grade_id=grade.id).prefetch_related('lesson_set', 'lesson_set__title_set')
        for chapter in chapters:
            item = {
                "id_book": grade.id,
                "id": chapter.id,
                "type": "chapter",
                "content": ViTokenizer.tokenize(str(chapter.name).lower())
            }
            data.append(item)
            for lesson in chapter.lesson_set.all():
                lesson_sg = ViTokenizer.tokenize(str(lesson.name).lower())
                lesson_item = {
                "id_book": grade.id,
                "id": lesson.id,
                "type": "lesson",
                "content": lesson_sg
                }
                data.append(lesson_item)
                for title in lesson.title_set.all():
                    title_content = ViTokenizer.tokenize(f"{title.name}: {title.content}")
                    documents = text_splitter.split_text(title_content)
                    [data.append({
                        "id_book": grade.id,
                        "id": title.id,
                        "type": "title",
                        "content": item
                    }) for item in documents]
        
    with open(str(BASE_DIR)+"/dataset/data_segmented.json", "w") as file:
        json.dump(data, file, ensure_ascii=False, indent=2, default=custom_encoder)
    return HttpResponse("done")



# def mean_pooling(model_output, attention_mask):
#         token_embeddings = model_output[0] #First element of model_output contains all token embeddings
#         input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
#         return torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(input_mask_expanded.sum(1), min=1e-9)

def cls_pooling(model_output):
    return model_output.last_hidden_state[:, 0]

def get_embeddings(text_list):
    encoded_input = tokenizer(
        text_list, padding=True, truncation=True, return_tensors="pt"
    )
    encoded_input = {k: v.to(device) for k, v in encoded_input.items()}
    model_output = model(**encoded_input)
    return cls_pooling(model_output)


def embeddings(request):
    issues_dataset = load_dataset("json", data_files=str(BASE_DIR)+"/dataset/data_segmented.json", split="train")
    issues_dataset.set_format("pandas")
    df=issues_dataset[:]
    dataset = Dataset.from_pandas(df)

    # batch_size = 10  # Adjust the batch size as needed
    # num_batches = (len(dataset) + batch_size - 1) // batch_size

    # embeddings_list = []
    # for i in trange(num_batches):
    #     batch_start = i * batch_size
    #     batch_end = min((i + 1) * batch_size, len(dataset))
    #     batch = dataset[batch_start:batch_end]
    #     embeddings_batch = get_embeddings(batch["content"]).detach().cpu().numpy()
    #     embeddings_list.extend(embeddings_batch)

    embeddings_dataset = dataset.map(
            lambda x: {
                "embeddings": get_embeddings(x["content"]).detach().cpu().numpy()[0]
            }
        )

    # embeddings_dataset = Dataset.from_dict({"embeddings": embeddings_list})
    embeddings_dataset.add_faiss_index(column="embeddings")
    embeddings_dataset.save_faiss_index('embeddings', str(BASE_DIR)+"/dataset/his_index.faiss")

    return HttpResponse("done")


def rerank(query,samples):
    tokenized_corpus = []  # Empty list to store tokenized texts
    tokenized_corpus = [] 
    for item in samples["content"]:
        tokenized_corpus.append(item.split())
    bm25 = BM25Okapi(tokenized_corpus)
    tokenized_query = query.split()
    doc_scores = bm25.get_scores(tokenized_query)
    samples["scores"] = list(doc_scores)
    results = []
    for i in range(len(samples["scores"])):
        samples["content"][i] = samples["content"][i].replace("_", " ")
        results.append({
            "id_book": samples["id_book"][i],
            "id": samples["id"][i],
            "type": samples["type"][i],
            "content": samples["content"][i],
            "score": samples["scores"][i],
            "title": samples["content"][i],
        })
    results.sort(key=lambda x: x["score"], reverse=True)
    return results

def search(request):
    if request.method == "POST":
        query = request.POST.get('message')
        query = ViTokenizer.tokenize(query)
        issues_dataset = load_dataset("json", data_files=str(BASE_DIR)+"/dataset/data_segmented.json", split="train")
        issues_dataset.load_faiss_index('embeddings', str(BASE_DIR)+"/dataset/his_index.faiss")
        # issues_dataset.load_faiss_index('embeddings', str(BASE_DIR)+"/dataset/his_index_bge.faiss")

        question_embedding = get_embeddings([query]).cpu().detach().numpy()
        scores, samples = issues_dataset.get_nearest_examples(
            "embeddings", question_embedding, k=10
        )
        samples["scores"] = scores.tolist()
        results = rerank(query, samples)
        return JsonResponse({"data":results[:4]})

def retri():
    from tqdm import trange
    issues_dataset = load_dataset("json", data_files=str(BASE_DIR)+"/dataset/data_segmented.json", split="train")
    issues_dataset.load_faiss_index('embeddings', str(BASE_DIR)+"/dataset/his_index.faiss")
    with open("/Users/trunghuynh/History_chatbot/history_chatbot/dataset/support_data.json") as file:
        data = json.load(file)
        for i in trange(len(data)):
            query = data[i]['question'] +' '+ data[i]['answer']
            query = ViTokenizer.tokenize(query)
            question_embedding = get_embeddings([query]).cpu().detach().numpy()
            scores, samples = issues_dataset.get_nearest_examples(
                "embeddings", question_embedding, k=10
            )
            samples["scores"] = scores.tolist()
            result = rerank(query, samples)

            data[i]['score'] = result[0]['score']
            data[i]['id_book'] = result[0]['id_book']
            data[i]['id'] = result[0]['id']
            data[i]['content'] = result[0]['content']
        json.dump(data,open("/Users/trunghuynh/History_chatbot/history_chatbot/dataset/support_data_result.json" ,"w"), ensure_ascii=False, indent=4)
    print("__done__")

# retri()
    # return HttpResponse("__done__")
@csrf_exempt
def add(request):
    if request.method == 'POST':
        try:
            params = json.loads(request.body)
            data = params['data']
            image = params['image'].replace("media","image_book")
            if isinstance(data, dict) and len(data) > 0:
                result = import_data(data,image)
                return result
            else:
                return HttpResponse("Dữ liệu JSON không đúng định dạng", status=400)
        except json.JSONDecodeError:
            return HttpResponse("Tệp JSON không hợp lệ", status=400)
    return HttpResponse("Phương thức không được hỗ trợ", status=405)



