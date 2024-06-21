from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse,JsonResponse
from .models import *
from django.urls import reverse
import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

# Create your views here.
def view_quizs(request):
    exams = Exam.objects.all().prefetch_related("question_set")
    return render(request, 'quiz/quiz.html', {"exams":exams,"exam":exams[0]})

def view_quiz(request, exam_id):
    exams = Exam.objects.all().prefetch_related("question_set")
    if exam_id:
        exam = get_object_or_404(Exam.objects.prefetch_related("question_set"), id=exam_id)
        return render(request, 'quiz/quiz.html', {"exams":exams,"exam":exam})
    
    return render(request, 'quiz/quiz.html', {"exams":exams,"exam":exams[0]})
    
@login_required(login_url="/users/signin")
def do_exam(request, exam_id):
    if exam_id:
        exam = get_object_or_404(Exam.objects.prefetch_related("question_set"), id=exam_id)
        return render(request, 'quiz/doexam.html', {"exam":exam})
    
@csrf_exempt 
def save_exam(request):
    if request.method == "POST":
        message = request.POST.get('message')
        params = json.loads(message)
        exam_id = params['exam']
        exam = get_object_or_404(Exam, id=exam_id)
        username = params['user']
        user = get_object_or_404(User, username=username)
        questions = [item for item in list(params.keys()) if "question" in item]
        for item in questions:
            question_id = item.replace('question_','')
            question = get_object_or_404(Question,id=question_id)
            answer = params[item]

            DoExam.objects.update_or_create(
                exam=exam, 
                user=user, 
                question=question, 
                defaults={'user_answer': answer}
            )
        result_url = reverse('quiz:view_result_exam', kwargs={'username': username, 'exam_id': exam_id})
        return JsonResponse({'result_url': result_url})
        # return redirect('quiz:view_result_exam', username=username, exam_id=exam_id)
    return JsonResponse({'error': 'Invalid request method'}, status=405)
    

def view_result_exam(request, username, exam_id):
    exam = get_object_or_404(Exam, id=exam_id)
    user = get_object_or_404(User, username=username)
    # do_exam = get_object_or_404(DoExam, user=user, exam=exam)
    do_exam = DoExam.objects.filter(user=user, exam=exam)
    return render(request, 'quiz/view_result.html', {"exam":exam, 'result': do_exam})

def import_quiz(data):
    name = data['name']

    # with open("/Users/trunghuynh/History_chatbot/history_chatbot/dataset/grade11-1.json") as file:
    #     data = json.load(file)
    if Exam.objects.filter(name=name):
        return HttpResponse("đã tồn tại")
    else:
        exam = Exam()
        exam.name = name
        exam.save()
        for item in data['questions']:
            question = Question()
            question.question = item['question']
            question.answer = item['answer']
            question.choice_1 = item['choices'][0]
            question.choice_2 = item['choices'][1]
            question.choice_3 = item['choices'][2]
            question.choice_4 = item['choices'][3]
            question.exam = exam
            question.save()
        return HttpResponse("__done__")

@csrf_exempt
def add(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            if isinstance(data, dict) and len(data) > 0:
                result = import_quiz(data)
                return result
            else:
                return HttpResponse("Dữ liệu JSON không đúng định dạng", status=400)
        except json.JSONDecodeError:
            return HttpResponse("Tệp JSON không hợp lệ", status=400)
    return HttpResponse("Phương thức không được hỗ trợ", status=405)
    


