class FedCMMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        # Agregar headers específicos para FedCM
        if request.path == '/api/v1/users/auth/social-login/':
            response['Access-Control-Allow-Origin'] = 'https://accounts.google.com'
            response['Access-Control-Allow-Credentials'] = 'true'
            response['Access-Control-Allow-Headers'] = 'Content-Type, Authorization, Sec-Fetch-Mode, Sec-Fetch-Site, Sec-Fetch-Dest'
            response['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
            response['Supports-Loading-Mode'] = 'fedcm'
            
        return response