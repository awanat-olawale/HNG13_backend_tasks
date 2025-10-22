from django.db import IntegrityError
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import AnalyzedString
from .utils import (
    get_length,
    is_palindrome,
    unique_characters,
    word_count,
    sha256_hash,
    character_frequency_map
)


# POST /strings and GET /strings?filters...
@api_view(['GET', 'POST'])
def strings_collection(request):
    if request.method == 'POST':
        # Missing field
        if 'value' not in request.data:
            return Response({"error": "Missing 'value' field"}, status=status.HTTP_400_BAD_REQUEST)

        text = request.data['value']

        # Invalid type
        if not isinstance(text, str):
            return Response({"error": "'value' must be a string"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

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
            return Response({"error": "String already exists"}, status=status.HTTP_409_CONFLICT)

        result = {
            "id": analyzed.sha256_hash,
            "value": analyzed.value,
            "properties": {
                "length": analyzed.length,
                "is_palindrome": analyzed.is_palindrome,
                "unique_characters": analyzed.unique_characters,
                "word_count": analyzed.word_count,
                "sha256_hash": analyzed.sha256_hash,
                "character_frequency_map": analyzed.character_frequency_map,
            },
            "created_at": analyzed.created_at.isoformat() + "Z"
        }

        return Response(result, status=status.HTTP_201_CREATED)

    # GET with filters
    qs = AnalyzedString.objects.all()
    is_palindrome_q = request.GET.get('is_palindrome')
    min_length = request.GET.get('min_length')
    max_length = request.GET.get('max_length')
    word_count_q = request.GET.get('word_count')
    contains_character = request.GET.get('contains_character')

    if is_palindrome_q is not None:
        if is_palindrome_q.lower() == 'true':
            qs = qs.filter(is_palindrome=True)
        elif is_palindrome_q.lower() == 'false':
            qs = qs.filter(is_palindrome=False)

    if min_length:
        qs = qs.filter(length__gte=int(min_length))
    if max_length:
        qs = qs.filter(length__lte=int(max_length))
    if word_count_q:
        qs = qs.filter(word_count=int(word_count_q))
    if contains_character:
        qs = qs.filter(value__icontains=contains_character)

    data = [{
        "id": s.sha256_hash,
        "value": s.value,
        "properties": {
            "length": s.length,
            "is_palindrome": s.is_palindrome,
            "unique_characters": s.unique_characters,
            "word_count": s.word_count,
            "sha256_hash": s.sha256_hash,
            "character_frequency_map": s.character_frequency_map,
        },
        "created_at": s.created_at.isoformat() + "Z"
    } for s in qs]

    return Response({"data": data, "count": len(data)}, status=status.HTTP_200_OK)


# GET /strings/{value} and DELETE /strings/{value}
@api_view(['GET', 'DELETE'])
def string_detail(request, value):
    try:
        analyzed = AnalyzedString.objects.get(value=value)
    except AnalyzedString.DoesNotExist:
        return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)

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
                "character_frequency_map": analyzed.character_frequency_map,
            },
            "created_at": analyzed.created_at.isoformat() + "Z"
        }
        return Response(result, status=status.HTTP_200_OK)

    # DELETE
    analyzed.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


# GET /strings/filter-by-natural-language?q=
@api_view(['GET'])
def filter_by_natural_language(request):
    query = request.GET.get('q', '').lower()
    strings = AnalyzedString.objects.all()

    if "palindrome" in query:
        strings = strings.filter(is_palindrome=True)
    elif "even" in query:
        strings = [s for s in strings if s.length % 2 == 0]
    elif "odd" in query:
        strings = [s for s in strings if s.length % 2 != 0]
    elif "uppercase" in query:
        strings = strings.filter(value__regex=r'^[A-Z]+$')
    elif "lowercase" in query:
        strings = strings.filter(value__regex=r'^[a-z]+$')

    data = [{
        "value": s.value,
        "length": s.length,
        "is_palindrome": s.is_palindrome,
        "sha256": s.sha256_hash
    } for s in strings]

    return Response({"results": data}, status=status.HTTP_200_OK)
