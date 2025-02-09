from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Director, Movie, Review
from .serializers import DirectorSerializers, MovieSerializers, ReviewSerializers
from rest_framework import status

@api_view(http_method_names=['GET'])
def director_list_api_view(request):
    director = Director.objects.select_related('movies_count').all()
    data = DirectorSerializers(instance=director, many=True).data
    return Response(data=data, status=200)

@api_view(http_method_names=['GET'])
def director_detail_api_view(request, id):
    try:
        director = Director.objects.get(id=id)
    except Director.DoesNotExist:
        return Response(data={'error: Director not found'}, status=status.HTTP_404_NOT_FOUND)
    data = DirectorSerializers(instance=director).data
    return Response(data=data)

@api_view(http_method_names=['GET'])
def movie_list_api_view(request):
    movie = Movie.objects.filter('id, title, description, duration, director')
    data = MovieSerializers(instance=movie, many=True).data
    return Response(data=data, status=200)

@api_view(http_method_names=['GET'])
def movie_review_list_api_view(request):
    movie = Movie.objects.prefetch_related('reviews', 'director').all()
    data = MovieSerializers(instance=movie, many=True).data
    return Response(data=data, status=200)

@api_view(http_method_names=['GET'])
def movie_detail_api_view(request, id):
    try:
        movie = Movie.objects.get(id=id)
    except Movie.DoesNotExist:
        return Response(data={'error: Movie not found'}, status=status.HTTP_404_NOT_FOUND)
    data = MovieSerializers(instance=movie).data
    return Response(data=data)

@api_view(http_method_names=['GET'])
def review_list_api_view(request):
    review = Review.objects.select_related('movie').all()
    data = ReviewSerializers(instance=review, many=True).data
    return Response(data=data, status=200)

@api_view(http_method_names=['GET'])
def review_detail_api_view(request, id):
    try:
        review = Review.objects.get(id=id)
    except Review.DoesNotExist:
        return Response(data={'error: Review not found'}, status=status.HTTP_404_NOT_FOUND)
    data = ReviewSerializers(instance=review).data
    return Response(data=data)
