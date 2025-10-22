from django.urls import path
from .views import analyze_string, get_string, get_all_strings, delete_string, filter_by_natural_language

urlpatterns = [
    path('strings/', analyze_string, name='analyze_string'),
    path('strings/get/', get_string, name='get_string'),
    path('strings/all/', get_all_strings, name='get_all_strings'),
    path('strings/filter-by-natural-language/', filter_by_natural_language, name='filter_by_nl'),
    path('strings/<str:value>/', delete_string, name='delete_string')
]