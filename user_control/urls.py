from django.urls import path
from django.urls import include
from .views import LoginView
from .views import RegisterView
from .views import RefreshView


urlpatterns= [
    
    path('login', LoginView.as_view()),
    path('register', RegisterView.as_view()),
    path('refresh', RefreshView.as_view()),
    # path('secured-info', Gt)
]