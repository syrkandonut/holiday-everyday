from django.http import JsonResponse


async def index(request):
    return JsonResponse(data={"text": "Hello, from Agency!"})
