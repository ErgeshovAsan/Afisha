from django.urls import path
from . import views

urlpatterns = [
    path('registration/', views.RegistAPIView.as_view()),
    path('authorization/', views.AuthAPIView.as_view()),
    path('confirm/', views.ConfirmAPIView.as_view()),
]
