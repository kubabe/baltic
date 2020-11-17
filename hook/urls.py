from django.urls import path
from hook import views

urlpatterns = [
    path('server-update/', views.update_server, name='update_server')
]