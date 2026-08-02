from django.shortcuts import redirect

class RoleMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            path = request.path

            if path.startswith('/patient/'):
                if not hasattr(request.user, 'patient'):
                    return redirect('login')
                
            if path.startswith('/doctor/'):
                if not hasattr(request.user, 'doctor'):
                    return redirect('login')
                
        response = self.get_response(request)
        return response