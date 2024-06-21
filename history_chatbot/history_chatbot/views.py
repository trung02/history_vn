from django.http import HttpResponse
from django.shortcuts import render
from books.models import *
from chatbot.models import *
from django.contrib.auth.decorators import login_required

def homepage(request):
    books = Grade.objects.all()
    return render(request, 'home.html', {'books': books})

def about(request):
    # return HttpResponse("About page")
    return render(request,'about.html')
def read_book(request, grade):
    print(grade)
    chapters = Chapter.objects.filter(grade_id=grade).prefetch_related('lesson_set', 'lesson_set__title_set')  # Prefetch optimization
    if chapters:
        context = {
            'chapters': chapters,
        }
        return render(request, 'book.html', context)
    else:
        return HttpResponse("error")
@login_required(login_url="/users/signin")
def chatbot(request):
    chats = Chat.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'chatbot.html', {"chats": chats})

    