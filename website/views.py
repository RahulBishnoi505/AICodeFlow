from django.shortcuts import render
from django.contrib import messages

# Create your views here.

language_list = ['c', 'cpp', 'csharp', 'css', 'dart', 'django', 'go', 'java', 'javascript', 'matlab', 'mongodb', 'objectivec', 'php', 'powershell', 'python', 'r', 'ruby', 'rust', 'scheme', 'sql', 'swift']

def home(request):
    if request.method == "POST":
        code = request.POST['code']
        language = request.POST['language']

        if language == "Programming Language":
            messages.success(request, 'Please select a programming language')
            return render(request, "website/index.html", {"language_list":language_list, "code":code, "language": language})
        return render(request, "website/index.html", {"language_list":language_list, "code":code, "language": language})
    return render(request, "website/index.html", {"language_list":language_list})