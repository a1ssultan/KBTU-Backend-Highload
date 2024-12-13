from django.http import JsonResponse

ALLOWED_IPS = ["127.0.0.1"]


class IPWhitelistMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip = request.META.get("REMOTE_ADDR")
        if ip not in ALLOWED_IPS:
            return JsonResponse({"error": "Forbidden"}, status=403)
        return self.get_response(request)
