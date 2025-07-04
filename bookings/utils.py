from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
import logging

logger = logging.getLogger(__name__)

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    
    if response is not None:
        custom_data = {
            'error': {
                'code': response.status_code,
                'message': str(exc),
                'details': response.data
            }
        }
        response.data = custom_data
    else:
        logger.error(f"Unhandled exception: {str(exc)}")
        custom_data = {
            'error': {
                'code': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'message': 'Internal Server Error',
                'details': str(exc)
            }
        }
        response = Response(custom_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    return response