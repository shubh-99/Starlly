from django.urls import path

from . import views

urlpatterns = [
    path('starlly/', views.index, name='starlly'),
    path('login/', views.login, name='login')
]