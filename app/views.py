from pprint import pprint

from django.shortcuts import render
from app.crawler import  crawler


# Create your views here.

def login(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        if crawler.user_exist(username,password):
           return render(request, 'home.html')
        else :
            request.__setattr__('error', True)
            return render(request, 'login.html')
    return render(request, 'login.html')

def home(request):
    return render(request, 'home.html')

def artist(request):
    token=request.GET.get('token')
    crawler.get_artist_followed(token)
    return render(request, 'artisti.html')

