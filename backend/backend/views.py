from django.conf import settings
from django.db import connection
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view


@api_view(["GET"])
def health_check(request):
    try:
        connection.ensure_connection()

        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")

        return Response({
            "message": "connected!!!",
        }, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({
            "message": "disconnected!!!",
            "error": str(e),
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
