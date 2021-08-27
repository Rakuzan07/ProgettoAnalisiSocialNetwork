from django.shortcuts import render
from app.crawler import  crawler


# Create your views here.

def login(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        if crawler.user_exist(username,password):
           return render(request, 'presente')
        else :
            return render(request, 'assente')
    return render(request, 'login.html')

def home(request):
    return render(request, 'home.html')
