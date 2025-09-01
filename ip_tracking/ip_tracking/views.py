from django.contrib.auth import authenticate, login
from django.http import HttpResponse, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from ratelimit.decorators import ratelimit

@csrf_exempt
@ratelimit(key='ip', rate='10/m', method='POST', block=True)
def login_view(request):
    if getattr(request, 'limited', False):
        return HttpResponseForbidden('Rate limit exceeded.')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponse('Login successful!')
        else:
            return HttpResponseForbidden('Invalid credentials.')
    return HttpResponse('Login page')
