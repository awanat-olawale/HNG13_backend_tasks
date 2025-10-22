from django.urls import path
from . import views

urlpatterns = [
    path('strings', views.strings_collection, name='strings_collection'),
    path('strings/<str:value>', views.string_detail, name='string_detail'),
    path('strings/filter-by-natural-language', views.filter_by_natural_language, name='filter_by_natural_language'),
]