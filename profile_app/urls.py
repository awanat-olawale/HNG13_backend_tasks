from django.urls import path, include
from . import views

urlpatterns = [
    path('me/', views.my_profile, name='my_profile'),
]
