key="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"
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from groq import Groq
import logging
import json
from .models import *

client = Groq(api_key=key)  # Replace 'your_api_key' with your actual API key
logger = logging.getLogger(__name__)

@login_required
@csrf_exempt  # If you want to bypass CSRF protection (usually not recommended)
def chatbot(request):
    if request.method == "POST":
        message = request.POST.get('message')
        params = json.loads(message)
        message = params["query"]
        context = params['context']
        if not message:
            return JsonResponse({'error': 'No message provided'}, status=400)
        try:
    
            if context['score'] >=9 and context['type']=='title':
                message = f"Dựa vào nội dung sau hãy trả lời ngắn gọn câu hỏi\nNội dung: {context['content']}\nCâu hỏi: {message}"
                 
            completion = client.chat.completions.create(
                model="llama3-70b-8192",
                messages=[
                    {"role": "system", "content": "Bạn là giảng viên lịch sử của Việt Nam. Hãy thực hiện yêu cầu bằng tiếng Việt."},
                    {"role": "user", "content": message}
                ],
                temperature=0.8,
                max_tokens=1024,
                top_p=1,
                stream=False,
                stop=None,
            )

            response = completion.choices[0].message.content
            if isinstance(message, str) and isinstance(response, str):
                chat_message = Chat(
                    message=message,
                    response=response,
                    user=request.user
                )
                chat_message.save()
            return JsonResponse({'message': message, 'response': response, 'id': chat_message.id})

        except Exception as e:
            logger.error(f"Error in chatbot completion: {e}")
            return JsonResponse({'error': 'An error occurred while processing your request'}, status=500)
    return render(request, 'chatbot.html')

@login_required
@csrf_exempt 
def delete(request, id):
    if request.method =="POST":
        obj = get_object_or_404(Chat, id = id)
        obj.delete()
        return JsonResponse({"message": "done"})



    