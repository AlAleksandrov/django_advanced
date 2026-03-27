from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.http import Http404
from rest_framework import status
from rest_framework.response import Response


def custom_exception_handler(exc, context):
    if isinstance(exc, Http404):
        return Response({'detail': exc.args[0]}, status=status.HTTP_404_NOT_FOUND)

    if isinstance(exc, PermissionDenied):
        return Response({'detail': f'Access denied'}, status=status.HTTP_403_FORBIDDEN)

    return custom_exception_handler(exc, context)
