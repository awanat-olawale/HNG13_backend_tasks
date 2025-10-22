import re
from django.db import IntegrityError
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.views.decorators.http import require_GET
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from .models import AnalyzedString
from .utils import sha256_hash
from .utils import (
    get_length,
    is_palindrome,
    unique_characters,
    word_count,
    sha256_hash,
    character_frequency_map
)

@api_view(['POST'])
def analyze_string(request):
    text = request.data.get('value')

    if text is None:
        return Response({"error": '"value" field is required.'}, status=400)

    if not isinstance(text, str):
        return Response({"error": '"value" must be a string.'}, status=422)

    hash_value = sha256_hash(text)

    try:
        # Attempt to create a new record; will fail if duplicate
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
        # Duplicate detected
        return Response(
            {"error": "String already exists in the system."},
            status=status.HTTP_409_CONFLICT
        )

    # Build response
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

#GET endpoint by value
@api_view(['GET'])
def get_string(request):
    text = request.query_params.get('value')

    if not text:
        return Response({"error": '"value" query parameter is required.'}, status=400)

    try:
        analyzed = AnalyzedString.objects.get(value=text)
    except AnalyzedString.DoesNotExist:
        return Response({"error": "String does not exist in the system."}, status=status.HTTP_404_NOT_FOUND)

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

#GET all enpoint by filtering
@api_view(['GET'])
def get_all_strings(request):
    strings = AnalyzedString.objects.all()

    # Apply filters
    is_palindrome = request.query_params.get('is_palindrome')
    min_length = request.query_params.get('min_length')
    max_length = request.query_params.get('max_length')
    word_count = request.query_params.get('word_count')
    contains_character = request.query_params.get('contains_character')

    if is_palindrome is not None:
        if is_palindrome.lower() == 'true':
            strings = strings.filter(is_palindrome=True)
        elif is_palindrome.lower() == 'false':
            strings = strings.filter(is_palindrome=False)
        else:
            return Response({"error": "Invalid is_palindrome value"}, status=400)

    if min_length is not None:
        try:
            min_length = int(min_length)
            strings = strings.filter(length__gte=min_length)
        except ValueError:
            return Response({"error": "min_length must be an integer"}, status=400)

    if max_length is not None:
        try:
            max_length = int(max_length)
            strings = strings.filter(length__lte=max_length)
        except ValueError:
            return Response({"error": "max_length must be an integer"}, status=400)

    if word_count is not None:
        try:
            word_count = int(word_count)
            strings = strings.filter(word_count=word_count)
        except ValueError:
            return Response({"error": "word_count must be an integer"}, status=400)

    if contains_character:
        strings = strings.filter(value__icontains=contains_character)

    # Build response
    data = []
    for s in strings:
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
        "word_count": word_count,
        "contains_character": contains_character
    }

    return Response({
        "data": data,
        "count": len(data),
        "filters_applied": filters_applied
    }, status=200)

@api_view(['DELETE'])
def delete_string(request, value):
    try:
        string_hash = sha256_hash(value)
        string_obj = AnalyzedString.objects.filter(sha256_hash=string_hash).first()
        if not string_obj:
            return Response({"error": "String not found"}, status=404)

        string_obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    except Exception as e:
        return Response({"error": str(e)}, status=500)

#FILTERING BY NATURAL LANGUAGE PARSING
@csrf_exempt
@require_GET
@api_view(['GET'])
def filter_by_natural_language(request):
    query = request.GET.get("query", "").lower().strip()
    if not query:
        return Response({"error": "Query parameter is required"}, status=400)

    filters = {}

    # Simple heuristics
    if "palindrom" in query:
        filters["is_palindrome"] = True
    if "single word" in query:
        filters["word_count"] = 1
    # Extract numbers for length filters
    match = re.search(r'longer than (\d+) characters', query)
    if match:
        filters["min_length"] = int(match.group(1)) + 1
    match = re.search(r'shorter than (\d+) characters', query)
    if match:
        filters["max_length"] = int(match.group(1)) - 1
    # Contain specific letter
    match = re.search(r'letter (\w)', query)
    if match:
        filters["contains_character"] = match.group(1)
    if "first vowel" in query:
        filters["contains_character"] = "a"

    # Apply filters to queryset
    qs = AnalyzedString.objects.all()
    if "is_palindrome" in filters:
        qs = qs.filter(is_palindrome=filters["is_palindrome"])
    if "word_count" in filters:
        qs = qs.filter(word_count=filters["word_count"])
    if "min_length" in filters:
        qs = qs.filter(length__gte=filters["min_length"])
    if "max_length" in filters:
        qs = qs.filter(length__lte=filters["max_length"])
    if "contains_character" in filters:
        char = filters["contains_character"]
        qs = [s for s in qs if char in s.value]

    # Build response
    data = [
        {
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
        } for s in qs
    ]

    return Response({
        "data": data,
        "count": len(data),
        "interpreted_query": {
            "original": query,
            "parsed_filters": filters
        }
    })