from django.db import connection


class SerializableIsolationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        with connection.cursor() as cursor:
            cursor.execute('SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;')

        response = self.get_response(request)
        return response
