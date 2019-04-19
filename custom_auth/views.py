from django.shortcuts import render
from django.http import HttpResponse
import jwt
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
import json
from custom_auth.models import *
from datetime import timedelta
from datetime import datetime
import pytz, json
# Create your views here.

@csrf_exempt
def index(request):
    email = request.POST.get("email")
    if UserSession.objects.filter(user__email=email).exists():
        user_session = UserSession.objects.get(user__email=email)
        expiry_time = user_session.jwt_token_created + timedelta(minutes=30)
        now = datetime.utcnow().replace(tzinfo=pytz.utc)
        if now <= expiry_time and request.META['HTTP_AUTHORIZATION'].split()[1] == user_session.jwt_token:
            return HttpResponse({"status":"success","message":"Hello, starlly"})
    return HttpResponse({"status":"fail"})		

@csrf_exempt
def login(request):
    if request.method == 'GET':
        return render(request, template_name="custom_auth/login.html", context={"name": "starlly"})
    elif request.method == 'POST':
        try:
            if User.objects.filter(username=request.POST.get("username")).exists():
                user = User.objects.get(username=request.POST.get("username"))
                if authenticate(username=request.POST.get("username"), password=request.POST.get("password")):
                    payload = {'id': user.id, 'email': user.email}
                    jwt_token = {'token': jwt.encode(payload, "SECRET_KEY")}
                    UserSession.objects.create(user=user, jwt_token=jwt_token.get("token"))
                    # return HttpResponse(jwt_token)
                    return HttpResponse(json.dumps({"status": "success", "token": str(jwt_token.get("token"))}))
                else:
                    return HttpResponse(json.dumps({"status": "success", "reason": "Password is incorrect"}))
            return HttpResponse(json.dumps({"status": "success", "reason": "user does not exists"}))
        except Exception:
            return HttpResponse(json.dumps({"status": "failed"}))