from django.urls import path
from core import views

urlpatterns = [
    path('', views.home, name='home'),
    path('history',views.history, name='history'),
]
