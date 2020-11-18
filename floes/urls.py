from django.urls import path
from floes import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about-me/', views.about_me, name='about-me'),
    path('post/', views.post, name='post')
]