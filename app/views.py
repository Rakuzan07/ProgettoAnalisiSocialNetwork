from django.http import JsonResponse
from django.shortcuts import render

from app.crawler import crawler
from app.networks import artists_network
from app.recommender import recommender

from app.networks import users_network
import json

# Create your views here.

def login(request):
    try:
        code = request.COOKIES['code']
        return render(request, 'home.html')
    except KeyError:
        return render(request, 'login.html')


def home(request):
    token = json.dumps(crawler.client_credentials_manager.get_access_token())
    request.__setattr__('client', token)
    return render(request, 'home.html')


def artist(request):
    # crawler.get_artist_followed()
    return render(request, 'artisti.html')


def get_graph(request):
    if request.is_ajax():
        graph = artists_network.create_network()
        #print('value 1 '+graph['data']['nodes']+"  value2 "+graph['data']['links'])
        return JsonResponse({"nodes": graph['data']['nodes'],
                             "links": graph['data']['links']})

def get_user_graph(request):
    if request.is_ajax():
        graph = users_network.create_network()
        #print('value 1 '+graph['data']['nodes']+"  value2 "+graph['data']['links'])
        print(graph['data']['nodes'])
        return JsonResponse({"nodes": graph['data']['nodes'],
                             "links": graph['data']['links']})


def explore(request):
    token = json.dumps(crawler.client_credentials_manager.get_access_token())
    request.__setattr__('client', token)
    return render(request, 'home.html')

def graph(request):
    return render(request, 'graph.html')

def users_graph(request):
    return render(request, 'users_graph.html')


def get_last_album(request):
    if request.is_ajax():
        data = crawler.spotify.artist_albums(artist_id=request.GET.get('id'), limit=1)
        url = data['items'][0]['external_urls']['spotify']
        ins = url.find('/album')
        return JsonResponse({'url': url[:ins] + '/embed' + url[ins:]})


def authenticate(request):
    try:
        code = request.COOKIES['code']
    except KeyError:
        code = request.GET.get('code')

    if code is None:
        print("Il cookie non è settato!")
    else:
        data = crawler.get_token(code)
        token = data['access_token']
        refresh_token = data['refresh_token']
        crawler.store_user(refresh_token)

        request.__setattr__('refresh', refresh_token)
        token = json.dumps(crawler.client_credentials_manager.get_access_token())
        request.__setattr__('client', token)
    return render(request, 'auth.html')


def foll_rec(request):
    token = None
    try:
        token = request.COOKIES['refresh_token']
    except KeyError:
        print("Il cookie non è settato!")

    recommended = {}
    if token is not None:
        recommended = recommender.followship_recommendations(token)
    return JsonResponse(recommended, safe=False)


def artists_recommender(request):
    token = None
    try:
        token = request.COOKIES['refresh_token']
    except KeyError:
        print("Il cookie non è settato!")

    recommended = {}
    if token is not None:
        recommended = recommender.artist_recommender(token)
    return JsonResponse(recommended, safe=False)


def recommendations(request):
    return render(request, 'recommender.html')


def art_rec(request):
    ret_val = recommender.artist_recommender(request.COOKIES['refresh_token'])
    return JsonResponse(ret_val, safe=False)