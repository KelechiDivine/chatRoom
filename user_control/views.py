import jwt
from .models import Jwt
from .models import CustomUser
from datetime import datetime
from datetime import timedelta
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

class LoginView(APIViews):
    serializer_class= LoginSerializer
    
    def post(self, request):
        serializer= self.serializer_class(data= request.data)
        serializer.is_valid(raise_exception= True)
        
        user= authenticate(
            username= serializer.validated_data['username'],
            password= serializer.validated_data['password'])
        
        if not user:
            return Response(
                {
                    'error': 'Invalid username or password'
                },
                
                status= '400'
            )
        
        Jwt.objects.filter(user_id= user.id).delete()
        access= get_access_token(
            {
                'user_id': user.id
            }
        )
        
        refresh= get_refresh_token()
        
        Jwt.objects.create(
            user_id= user.id, access= access.decode(), refresh= refresh.decode()
        )
        
        return Response(
            {
                'access': access,
                'refresh': refresh
            }
        )
    
class RegisterView(APIViews):
    serializer_class= RegisterSerializer
    
    def post(self, request):
        serializer= self.serializer_class(data= request.data)
        serializer.is_valid(raise_exception= True)
        
        CustomUser.objects._create_user(**serializer.validated_data)
        return Response(
            {
                'success': 'User Created.'
            }, status= 201
        )
    
class RefreshView(APIViews):
    serializer_class = RefreshSerializer
    
    def post(self, request):
        serializer= self.serializer_class(data= request.data)
        serializer.is_valid(raise_exception= True)
        
        try:
            active_jwt= Jwt.objects.get(
                refresh= serializer.validated_data['refresh']
            )
            
        except Jwt.DoesNotExist:
            return Response(
                {
                    'error': 'refresh token not found'
                }, status= '400'
            )
        
        if not Authentication.verify_token(serializer.validated_data['refresh']):
            return Response(
                {
                    'error': 'Token is invalid or has expire'
                }
            )
        
        access= get_access_token(
            {
                'user_id': active_jwt.user_id
            }
        )
        
        refresh= get_refresh_token()
        
        active_jwt.access= access.decode()
        active_jwt.refresh= refresh.decode()
        active_jwt.save()
        
        return Response(
            {
                'access': access,
                'refresh': refresh
            }
        )
    
#
# class GetSecuredInfo(APIViews):
#     permission_classes= [IsAuthenticated]
#
#     def get(self, request):
#         print(request.user)
#         return Response(
#             {
#                 'data': 'This is a secured info.'
#             }
#         )