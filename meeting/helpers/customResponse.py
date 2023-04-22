from django.http.response import JsonResponse
from rest_framework import status

class Custom:
    def errorResponse(data, operationResult, statusCode, operationMessage):
        return JsonResponse({
            'type' : operationResult,
            'message' : operationMessage,
            'code' : statusCode,
            'data': [data]
        },
        status=statusCode
        )
    
    def successResponse(data, operationResult, statusCode, operationMessage):
        return JsonResponse({
            'type' : operationResult,
            'message' : operationMessage,
            'code' : statusCode,
            'data': [data]
        },
        status=statusCode
        )

    def dataResponse(data, operationResult, statusCode, operationMessage):
        return JsonResponse({
            'type' : operationResult,
            'message' : operationMessage,
            'code' : statusCode,
            'data': [data]
        },
        status=statusCode
        )