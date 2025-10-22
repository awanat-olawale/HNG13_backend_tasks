from django.db import IntegrityError
from django.http import JsonResponse
from rest_framework.decorators import api_view
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
            return JsonResponse({"error": "Missing 'value' field"}, status=422)

        text = request.data['value']

        # Invalid type
        if not isinstance(text, str):
            return JsonResponse({"error": "'value' must be a string"}, status=422)

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
            return JsonResponse({"error": "String already exists"}, status=409)

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

        return JsonResponse(result, status=201)

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

    return JsonResponse({"data": data, "count": len(data)}, status=200)


# GET /strings/{value} and DELETE /strings/{value}
@api_view(['GET', 'DELETE'])
def string_detail(request, value):
    try:
        analyzed = AnalyzedString.objects.get(value=value)
    except AnalyzedString.DoesNotExist:
        return JsonResponse({"error": "Not found"}, status=404)

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
        return JsonResponse(result, status=200)

    # DELETE
    analyzed.delete()
    return JsonResponse({"message": "Deleted successfully"}, status=200)


# GET /strings/filter-by-natural-language?q=
@api_view(['GET'])
def filter_by_natural_language(request):
    query = request.GET.get('q', '').lower()
    strings = AnalyzedString.objects.all()

    if "palindrome" in query:
        strings = strings.filter(is_palindrome=True)
    elif "even" in query:
        strings = strings.filter(length__mod=2)
    elif "odd" in query:
        strings = strings.exclude(length__mod=2)
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

    return JsonResponse({"results": data}, status=200)
