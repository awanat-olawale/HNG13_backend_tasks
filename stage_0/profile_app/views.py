import requests
from django.http import JsonResponse
from datetime import datetime, timezone

def get_cat_fact():
    try:
        response = requests.get("https://catfact.ninja/fact", timeout=5)
        response.raise_for_status()
        fact = response.json().get("fact", "No cat fact available!")
        return fact
    except requests.RequestException:
        return "Could not fetch cat fact at the moment"


def my_profile(request):
    data = {
        "status": "success",
        "user": {
            "email": "olawaleawanat@gmail.com",
            "name": "Awanat Olawale",
            "stack": "Python/Django"
        },
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "fact": get_cat_fact()
    }
    return JsonResponse(data)
