from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpRequest


@csrf_exempt
def check_email(request):
    """ AJAX checking if email already exists (registration stage) """

    if HttpRequest.is_ajax and request.method == "POST":
        email = request.POST.get('email', False)
        if User.objects.filter(email=email).exists():
            return HttpResponse("false")
        else:
            return HttpResponse("true")
    else:
        return HttpResponse('')
