from datetime import datetime
from django.db import IntegrityError
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from .models import AnalyzedString
from .utils import (
    get_length,
    is_palindrome,
    unique_characters,
    word_count,
    sha256_hash,
    character_frequency_map
)

# POST /strings  and GET /strings?filters...
@api_view(['GET', 'POST'])
def strings_collection(request):
    # POST: create/analyze string 
    if request.method == 'POST':
        # 400 if missing
        if 'value' not in request.data:
            return Response({"error": '"value" field is required.'}, status=status.HTTP_400_BAD_REQUEST)

        text = request.data['value']

        # 422 if wrong type
        if not isinstance(text, str):
            return Response({"error": '"value" must be a string.'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        hash_value = sha256_hash(text)

        try:
            analyzed = AnalyzedString.objects.create(
                value=text,
                sha256_hash=hash_value,
                length=get_length(text),
                is_palindrome=is_palindrome(text),
                unique_characters=unique_characters(text),
                word_count=word_count(text),
                character_frequency_map=character_frequency_map(text),
            )
        except IntegrityError:
            # duplicate
            return Response({"error": "String already exists in the system."}, status=status.HTTP_409_CONFLICT)

        result = {
            "id": analyzed.sha256_hash,
            "value": analyzed.value,
            "properties": {
                "length": analyzed.length,
                "is_palindrome": analyzed.is_palindrome,
                "unique_characters": analyzed.unique_characters,
                "word_count": analyzed.word_count,
                "sha256_hash": analyzed.sha256_hash,
                "character_frequency_map": analyzed.character_frequency_map
            },
            "created_at": analyzed.created_at.isoformat() + "Z"
        }

        return Response(result, status=status.HTTP_201_CREATED)

    # GET: list with filters (query params) 
    # Query params: is_palindrome, min_length, max_length, word_count, contains_character
    qs = AnalyzedString.objects.all()

    is_palindrome = request.query_params.get('is_palindrome')
    min_length = request.query_params.get('min_length')
    max_length = request.query_params.get('max_length')
    word_count_q = request.query_params.get('word_count')
    contains_character = request.query_params.get('contains_character')

    if is_palindrome is not None:
        if is_palindrome.lower() == 'true':
            qs = qs.filter(is_palindrome=True)
        elif is_palindrome.lower() == 'false':
            qs = qs.filter(is_palindrome=False)
        else:
            return Response({"error": "Invalid is_palindrome value"}, status=status.HTTP_400_BAD_REQUEST)

    if min_length is not None:
        try:
            min_length_i = int(min_length)
            qs = qs.filter(length__gte=min_length_i)
        except ValueError:
            return Response({"error": "min_length must be an integer"}, status=status.HTTP_400_BAD_REQUEST)

    if max_length is not None:
        try:
            max_length_i = int(max_length)
            qs = qs.filter(length__lte=max_length_i)
        except ValueError:
            return Response({"error": "max_length must be an integer"}, status=status.HTTP_400_BAD_REQUEST)

    if word_count_q is not None:
        try:
            word_count_i = int(word_count_q)
            qs = qs.filter(word_count=word_count_i)
        except ValueError:
            return Response({"error": "word_count must be an integer"}, status=status.HTTP_400_BAD_REQUEST)

    if contains_character:
        qs = qs.filter(value__icontains=contains_character)

    data = []
    for s in qs:
        data.append({
            "id": s.sha256_hash,
            "value": s.value,
            "properties": {
                "length": s.length,
                "is_palindrome": s.is_palindrome,
                "unique_characters": s.unique_characters,
                "word_count": s.word_count,
                "sha256_hash": s.sha256_hash,
                "character_frequency_map": s.character_frequency_map
            },
            "created_at": s.created_at.isoformat() + "Z"
        })

    filters_applied = {
        "is_palindrome": is_palindrome,
        "min_length": min_length,
        "max_length": max_length,
        "word_count": word_count_q,
        "contains_character": contains_character
    }

    return Response({
        "data": data,
        "count": len(data),
        "filters_applied": filters_applied
    }, status=status.HTTP_200_OK)


# GET /strings/{value} and DELETE /strings/{value}
@api_view(['GET', 'DELETE'])
def string_detail(request, value):
    # value arrives URL-decoded by Django
    try:
        analyzed = AnalyzedString.objects.get(value=value)
    except AnalyzedString.DoesNotExist:
        return Response({"error": "String does not exist in the system."}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        result = {
            "id": analyzed.sha256_hash,
            "value": analyzed.value,
            "properties": {
                "length": analyzed.length,
                "is_palindrome": analyzed.is_palindrome,
                "unique_characters": analyzed.unique_characters,
                "word_count": analyzed.word_count,
                "sha256_hash": analyzed.sha256_hash,
                "character_frequency_map": analyzed.character_frequency_map
            },
            "created_at": analyzed.created_at.isoformat() + "Z"
        }
        return Response(result, status=status.HTTP_200_OK)

    # method == DELETE
    analyzed.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

# Filtering by natural language
def filter_by_natural_language(request):
    query = request.GET.get('q', '').lower()

    if "palindrome" in query:
        filter_type = "palindrome"
    elif "even" in query or "odd" in query:
        filter_type = "length"
    elif "uppercase" in query:
        filter_type = "uppercase"
    elif "lowercase" in query:
        filter_type = "lowercase"
    else:
        filter_type = "unknown"

    return JsonResponse({
        "message": "Natural language filter parsed successfully",
        "filter_type": filter_type
    }, status=200)