from django.urls import path
from .views import (
    strings_collection,
    string_detail,
    filter_by_natural_language
)

urlpatterns = [
    # Collection: POST to create, GET to list/filter
    path('strings/', strings_collection, name='strings_collection'),

    # Natural language filter endpoint (keep this before the <path:value> route)
    path('strings/filter-by-natural-language/', filter_by_natural_language, name='filter_by_nl'),

    # Item: GET specific string and DELETE
    # use <path:value> to allow encoded characters; ordering matters (must be after specific routes)
    path('strings/<path:value>/', string_detail, name='string_detail'),
]
