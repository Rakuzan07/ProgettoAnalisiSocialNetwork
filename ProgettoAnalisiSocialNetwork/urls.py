"""ProgettoAnalisiSocialNetwork URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import path

from app import views

urlpatterns = [
    url(r'^/$', views.home, name="first_page"),
    url(r'^login/$', views.login, name="login"),
    url(r'^home/$', views.home, name="home"),
    url(r'^artist/$', views.artist, name="artist"),
    url(r'^authenticate/$', views.authenticate, name="authenticate"),
    url(r'^get_graph/$', views.get_graph, name="get_graph"),
    url(r'^get_user_graph/$', views.get_user_graph, name="get_user_graph"),
    url(r'^graph/$', views.graph, name="graph"),
    url(r'^users_graph/$', views.users_graph, name="users_graph"),
    url(r'^get_last_album/$', views.get_last_album, name="get_last_album"),
    url(r'^foll_rec/$', views.foll_rec, name="foll_rec"),
    url(r'^artists_recommender/$', views.artists_recommender, name="art_rec"),
    url(r'^recommendations/$', views.recommendations, name="fo_rec"),
    url(r'^art_recommender/$', views.art_rec, name="art_rec"),
]
