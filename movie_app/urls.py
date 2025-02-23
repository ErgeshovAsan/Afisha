from django.urls import path
from . import views

urlpatterns = [
    path('api/v1/directors/', views.DirectorListCreateAPIView.as_view()),
    path('api/v1/movies/', views.MovieListCreateAPIView.as_view()),
    path('api/v1/reviews/', views.ReviewListCreateAPIView.as_view()),
    path('api/v1/directors/<int:pk>/', views.DirectorRetrieveUpdateDestroyAPIView.as_view()),
    path('api/v1/movies/<int:pk>/', views.MovieRetrieveUpdateDestroyAPIView.as_view()),
    path('api/v1/reviews/<int:pk>/', views.ReviewRetrieveUpdateDestroyAPIView.as_view()),
    path('api/v1/movies/reviews/', views.MovieReviewListAPIView.as_view()),
    ]