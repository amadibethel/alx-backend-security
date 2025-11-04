from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django_ratelimit.decorators import ratelimit


@csrf_exempt
@ratelimit(key='ip', rate='5/m', block=True, method='POST')
@ratelimit(key='user_or_ip', rate='10/m', block=True, method='POST')
def login_view(request):
    """
    Example sensitive view (login) protected with rate limiting:
      - Anonymous users: 5 requests/minute
      - Authenticated users: 10 requests/minute
    """

    if request.method == 'POST':
        # Simulated login logic (can be replaced with actual auth)
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username == 'admin' and password == 'password':
            return JsonResponse({"message": "Login successful!"})
        else:
            return JsonResponse({"error": "Invalid credentials"}, status=401)

    return JsonResponse({"error": "Only POST requests are allowed"}, status=405)

