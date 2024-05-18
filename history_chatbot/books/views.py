from django.shortcuts import render
from django.http import HttpResponse
import json
from .models import *
# Create your views here.


def import_data(request):
    path= "books/dataset/history_knowledge_base.json"
    with open(path) as file:
        data = json.load(file)
        grade = list(data.keys())
        for g in grade:
            grade_model = Grade()
            grade_model.name=g
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