from django.http import HttpResponse
from django.shortcuts import render

from ProgettoAnalisiSocialNetwork import settings
from app.crawler import crawler


# Create your views here.

def login(request):
    try:
        code = request.COOKIES['code']
        return render(request, 'home.html')
    except KeyError:
        return render(request, 'login.html')


def home(request):
    return render(request, 'home.html')


def artist(request):
    # crawler.get_artist_followed()
    return render(request, 'artisti.html')


def authenticate(request):
    try:
        code = request.COOKIES['code']
        print("TROVATO NEI COOKIES")
    except KeyError:
        code = request.GET.get('code')
        print("TROVATO NELL URL")

    if code is None:
        print("Il cookie non è settato!")
    else:
        data = crawler.get_token(code)
        token = data['access_token']
        refresh_token = data['refresh_token']
        crawler.store_user(refresh_token)

        request.__setattr__('refresh', refresh_token)
    return render(request, 'home.html')
