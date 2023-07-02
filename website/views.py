from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import  UserCreationForm
from .forms import SignUpForm
from .models import UserData

import openai

from dotenv import load_dotenv
load_dotenv()
import os

# Create your views here.

language_list = ['c', 'css', 'django', 'java', 'javascript', 'matlab', 'php', 'powershell', 'python', 'r', 'ruby', 'rust', 'sql', 'swift']

def home(request):
    if request.method == "POST":
        code = request.POST['code']
        language = request.POST['language']

        if language == "Programming Language":
            messages.success(request, 'Please select a programming language')
            return render(request, "website/index.html", {"language_list":language_list, "code":code, "language": language})
        else:
            
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

                # Saving data to database
                user_record = UserData(question=code, answer=response, language=language, user=request.user)
                user_record.save()
                return render(request, "website/index.html", {"language_list":language_list, "response": response, "language": language})
            except Exception as e:
                return render(request, "website/index.html", {"language_list":language_list, "code": e, "language": language})


    return render(request, "website/index.html", {"language_list":language_list})




def suggest(request):
    
    if request.method == "POST":
        code = request.POST['code']
        language = request.POST['language']

        if language == "Programming Language":
            messages.success(request, 'Please select a programming language')
            return render(request, "website/suggest.html", {"language_list":language_list, "code":code, "language": language})
        else:
            
            openai.api_key = os.environ.get("API_KEY")
            #OpenAI 
            openai.Model.list()
            # Make an OpenAI Request
            try:
                response = openai.Completion.create(
                    engine = 'text-davinci-003',
                    prompt = f'Respond with code only. Nothing else than code. { code }',
                    temperature = 0,
                    max_tokens = 1000,
                    top_p = 1.0,
                    frequency_penalty = 0.0,
                    presence_penalty = 0.0
                    )
                response = response["choices"][0]["text"].strip()
                # Saving to database
                user_record = UserData(question=code, answer=response, language=language, user=request.user)
                user_record.save()
                return render(request, "website/suggest.html", {"language_list":language_list, "response": response, "language": language})
            except Exception as e:
                return render(request, "website/suggest.html", {"language_list":language_list, "code": e, "language": language})


    return render(request, "website/suggest.html", {"language_list":language_list})    


def login_user(request):    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Logged in Successfuly")
            return redirect('home')
        else:
            messages.success(request, "Error Logging In. Please Try Again.")
            return redirect('home')

    else:
        return render(request, "website/index.html", {})



def logout_user(request):
    logout(request)
    messages.success(request, "You Have Been Logged Out.")
    return redirect('home')

def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, 'You Have Registered Successfully')

            return redirect('home')
    else:
        form = SignUpForm()

    return render(request, 'website/register.html', {'form':form})


def history(request):
    return render(request, 'website/history.html', {})
