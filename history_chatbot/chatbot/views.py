key="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"
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from groq import Groq
import logging

client = Groq(api_key=key)  # Replace 'your_api_key' with your actual API key
logger = logging.getLogger(__name__)

@login_required
@csrf_exempt  # If you want to bypass CSRF protection (usually not recommended)
def chatbot(request):
    if request.method == "POST":
        message = request.POST.get('message')
        if not message:
            return JsonResponse({'error': 'No message provided'}, status=400)

        try:
            completion = client.chat.completions.create(
                model="llama3-8b-8192",
                messages=[
                    {"role": "system", "content": "Bạn là trợ lý về lịch sử Việt Nam."},
                    {"role": "user", "content": message}
                ],
                temperature=1,
                max_tokens=1024,
                top_p=1,
                stream=False,
                stop=None,
            )

            response = completion.choices[0].message.content
            return JsonResponse({'message': message, 'response': response})

        except Exception as e:
            logger.error(f"Error in chatbot completion: {e}")
            return JsonResponse({'error': 'An error occurred while processing your request'}, status=500)

    return render(request, 'chatbot.html')
