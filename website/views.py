from django.shortcuts import render
from django.contrib import messages
import openai

from dotenv import load_dotenv
load_dotenv()
import os

# Create your views here.

language_list = ['c', 'cpp', 'csharp', 'css', 'dart', 'django', 'go', 'java', 'javascript', 'matlab', 'mongodb', 'objectivec', 'php', 'powershell', 'python', 'r', 'ruby', 'rust', 'scheme', 'sql', 'swift']

def home(request):
    if request.method == "POST":
        code = request.POST['code']
        language = request.POST['language']

        if language == "Programming Language":
            messages.success(request, 'Please select a programming language')
            return render(request, "website/index.html", {"language_list":language_list, "code":code, "language": language})
        else:
            #OpenAI Key
            openai.api_key = os.environ.get("API_KEY")
            #OpenAI 
            openai.Model.list()
            # Make an OpenAI Request
            try:
                response = openai.Completion.create(
                    engine = 'text-davinci-003',
                    prompt = f'Respond with code only. Nothing else than code. Fix this {language} code: {code} and return only the fixed code.',
                    temperature = 0,
                    max_tokens = 1000,
                    top_p = 1.0,
                    frequency_penalty = 0.0,
                    presence_penalty = 0.0
                    )
                response = response["choices"][0]["text"].strip()
                print(response)
                return render(request, "website/index.html", {"language_list":language_list, "response": response, "language": language})
            except Exception as e:
                return render(request, "website/index.html", {"language_list":language_list, "code": e, "language": language})


    return render(request, "website/index.html", {"language_list":language_list})