# Permssions Policy (Feature Policy) Middleware
from django.utils.deprecation import MiddlewareMixin


class PermissionsPolicyMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        response['Permissions-Policy'] = (
            'camera=(), microphone=(), geolocation=()')
        return response
