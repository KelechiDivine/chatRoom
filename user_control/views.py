import jwt
from .models import Jwt
from .models import CustomUser
from datetime import datetime, timedelta
from django.conf import settings
import random
import string
from rest_framework.views import APIViews
from .serializers import LoginSerializer
from .serializers import RegisterSerializer
from .serializers import RefreshSerializer
from django.contrib.auth import authenticate
from rest_framework.response import Response
from .authentication import Authentication
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import render

# Create your views here.


def get_random(length):
    return ''.join(random.choice(
        string.ascii_uppercase + string.digits, k= length)
    )


def get_access_token(payload):
    return jwt.encode(
        {
            'exp': datetime.now() + timedelta(minutes= 5), **payload
        },
        settings.SECRET_KEY,
        algorithm= 'HS256'
    )

def get_refresh_token():
    return jwt.encode(
        
        {
            'exp': datetime.now() + timedelta(minutes= 365),
            'data': get_random(10)
        },
        
        settings.SECRET_KEY,
        algorithm= 'HS256'
    )