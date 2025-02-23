from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Director, Movie, Review
from .serializers import DirectorSerializers, MovieSerializers, ReviewSerializers, MovieReviewSerializers, \
    DirectorValidateSerializers, MovieValidateSerializers, ReviewValidateSerializers
from rest_framework import status
from django.db import transaction
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
from rest_framework.pagination import PageNumberPagination


class DirectorListCreateAPIView(ListCreateAPIView):
    serializer_class = DirectorSerializers
    queryset = Director.objects.all()
    pagination_class = PageNumberPagination

    def create(self, request, *args, **kwargs):
        serializer = DirectorValidateSerializers(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)
        name = serializer.validated_data.get('name')
        with transaction.atomic():
            director = Director.objects.create(
                name=name,
            )
        return Response(data=DirectorSerializers(director).data, status=status.HTTP_201_CREATED)

class DirectorRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = DirectorSerializers
    queryset = Director.objects.all()

    def update(self, request, *args, **kwargs):
        director = Director.objects.get(id=kwargs['pk'])
        serializer = DirectorValidateSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        director.name = serializer.validated_data.get('name')
        director.save()
        return Response(status=status.HTTP_201_CREATED)


class MovieListCreateAPIView(ListCreateAPIView):
    serializer_class = MovieSerializers
    queryset = Movie.objects.select_related('director_id').all()
    pagination_class = PageNumberPagination

    def create(self, request, *args, **kwargs):
        serializer = MovieValidateSerializers(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)
        title = serializer.validated_data.get('title')
        description = serializer.validated_data.get('description')
        duration = serializer.validated_data.get('duration')
        director_id = serializer.validated_data.get('director_id')
        with transaction.atomic():
            movie = Movie.objects.create(
                title=title,
                description=description,
                duration=duration,
                director_id=director_id,
            )
        return Response(data=MovieSerializers(movie).data, status=status.HTTP_201_CREATED)

class MovieReviewListAPIView(ListAPIView):
    serializer_class = MovieReviewSerializers
    queryset = Movie.objects.prefetch_related('reviews', 'director').all()
    pagination_class = PageNumberPagination

class MovieRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = MovieSerializers
    queryset = Movie.objects.select_related('director_id').all()

    def update(self, request, *args, **kwargs):
        movie = Movie.objects.get(id=kwargs['pk'])
        serializer = MovieValidateSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        movie.title = serializer.validated_data.get('title')
        movie.description = serializer.validated_data.get('description')
        movie.duration = serializer.validated_data.get('duration')
        movie.director_id = serializer.validated_data.get('director_id')
        movie.save()
        return Response(status=status.HTTP_201_CREATED)


class ReviewListCreateAPIView(ListCreateAPIView):
    serializer_class = ReviewSerializers
    queryset = Review.objects.select_related('movie_id').all()
    pagination_class = PageNumberPagination

    def create(self, request, *args, **kwargs):
        serializer = ReviewValidateSerializers(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)
        text = serializer.validated_data.get('text')
        stars = serializer.validated_data.get('stars')
        movie_id = serializer.validated_data.get('movie_id')
        with transaction.atomic():
            review = Review.objects.create(
                text=text,
                stars=stars,
                movie_id=movie_id,
            )
        return Response(data=ReviewSerializers(review).data, status=status.HTTP_201_CREATED)


class ReviewRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = ReviewSerializers
    queryset = Review.objects.select_related('movie_id').all()

    def update(self, request, *args, **kwargs):
        review = Review.objects.get(id=kwargs['pk'])
        serializer = ReviewValidateSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        review.text = serializer.validated_data.get('text')
        review.stars = serializer.validated_data.get('stars')
        review.movie_id = serializer.validated_data.get('movie_id')
        review.save()
        return Response(status=status.HTTP_201_CREATED)

# @api_view(http_method_names=['GET', 'POST'])
# def director_list_create_api_view(request):
#     if request.method == 'GET':
#         director = Director.objects.all()
#         data = DirectorSerializers(instance=director, many=True).data
#         return Response(data=data, status=200)
#     elif request.method == 'POST':
#         serializer = DirectorValidateSerializers(data=request.data)
#         if not serializer.is_valid():
#             return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)
#         name = serializer.validated_data.get('name')
#         with transaction.atomic():
#             director = Director.objects.create(
#                 name=name,
#             )
#         return Response(data=DirectorSerializers(director).data, status=status.HTTP_201_CREATED)

# @api_view(http_method_names=['GET', 'PUT', 'DELETE'])
# def director_detail_api_view(request, id):
#     try:
#         director = Director.objects.get(id=id)
#     except Director.DoesNotExist:
#         return Response(data={'error: Director not found'}, status=status.HTTP_404_NOT_FOUND)
#     if request.method == 'GET':
#         data = DirectorSerializers(instance=director).data
#         return Response(data=data)
#     elif request.method == 'PUT':
#         serializer = DirectorValidateSerializers(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         director.name = serializer.validated_data.get('name')
#         director.save()
#         return Response(status=status.HTTP_201_CREATED)
#     elif request.method == 'DELETE':
#         director.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

# @api_view(http_method_names=['GET', 'POST'])
# def movie_list_create_api_view(request):
#     if request.method == 'GET':
#         movie = Movie.objects.filter('id, title, description, duration, director')
#         data = MovieSerializers(instance=movie, many=True).data
#         return Response(data=data, status=200)
#     elif request.method == 'POST':
#         serializer = MovieValidateSerializers(data=request.data)
#         if not serializer.is_valid():
#             return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)
#         title = serializer.validated_data.get('title')
#         description = serializer.validated_data.get('description')
#         duration = serializer.validated_data.get('duration')
#         director_id = serializer.validated_data.get('director_id')
#         with transaction.atomic():
#             movie = Movie.objects.create(
#                 title=title,
#                 description=description,
#                 duration=duration,
#                 director_id=director_id,
#             )
#         return Response(data=MovieSerializers(movie).data, status=status.HTTP_201_CREATED)
#

# @api_view(http_method_names=['GET'])
# def movie_review_list_api_view(request):
#     movie = Movie.objects.prefetch_related('reviews', 'director').all()
#     data = MovieSerializers(instance=movie, many=True).data
#     return Response(data=data, status=200)

# @api_view(http_method_names=['GET', 'PUT', 'DELETE'])
# def movie_detail_api_view(request, id):
#     try:
#         movie = Movie.objects.get(id=id)
#     except Movie.DoesNotExist:
#         return Response(data={'error: Movie not found'}, status=status.HTTP_404_NOT_FOUND)
#     if request.method == 'GET':
#         data = MovieSerializers(instance=movie).data
#         return Response(data=data)
#     elif request.method == 'PUT':
#         serializer = MovieValidateSerializers(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         movie.title = serializer.validated_data.get('title')
#         movie.description = serializer.validated_data.get('description')
#         movie.duration = serializer.validated_data.get('duration')
#         movie.director_id = serializer.validated_data.get('director_id')
#         movie.save()
#         return Response(status=status.HTTP_201_CREATED)
#     elif request.method == 'DELETE':
#         movie.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

# @api_view(http_method_names=['GET', 'POST'])
# def review_list_create_api_view(request):
#     if request.method == 'GET':
#         review = Review.objects.select_related('movie').all()
#         data = ReviewSerializers(instance=review, many=True).data
#         return Response(data=data, status=200)
#     elif request.method == 'POST':
#         serializer = ReviewValidateSerializers(data=request.data)
#         if not serializer.is_valid():
#             return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)
#         text = serializer.validated_data.get('text')
#         stars = serializer.validated_data.get('stars')
#         movie_id = serializer.validated_data.get('movie_id')
#         with transaction.atomic():
#             review = Review.objects.create(
#                 text=text,
#                 stars=stars,
#                 movie_id=movie_id,
#             )
#         return Response(data=ReviewSerializers(review).data, status=status.HTTP_201_CREATED)
#
# @api_view(http_method_names=['GET', 'PUT', 'DELETE'])
# def review_detail_api_view(request, id):
#     try:
#         review = Review.objects.get(id=id)
#     except Review.DoesNotExist:
#         return Response(data={'error: Review not found'}, status=status.HTTP_404_NOT_FOUND)
#     if request.method == 'GET':
#         data = ReviewSerializers(instance=review).data
#         return Response(data=data)
#     elif request.method == 'PUT':
#         serializer = ReviewValidateSerializers(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         review.text = serializer.validated_data.get('text')
#         review.stars = serializer.validated_data.get('stars')
#         review.movie_id = serializer.validated_data.get('movie_id')
#         review.save()
#         return Response(status=status.HTTP_201_CREATED)
#     elif request.method == 'DELETE':
#         review.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
