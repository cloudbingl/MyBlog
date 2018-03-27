from django.contrib.auth.models import User
from django.http import HttpResponse
from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def check_username(request):
    if request.method == "POST":
        username = request.POST.get("username")
        try:
            User.objects.get(username=username)
            return HttpResponse("false")
        except User.DoesNotExist:
            return HttpResponse("true")