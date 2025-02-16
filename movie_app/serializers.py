from rest_framework import serializers
from .models import Director, Movie, Review
from rest_framework.exceptions import ValidationError


class DirectorSerializers(serializers.ModelSerializer):
    class Meta:
        model = Director
        fields = 'id name movies_count'.split()

class MovieSerializers(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = 'id title description duration director reviews rating'.split()
        depth = 1

class ReviewSerializers(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = 'id text stars movie'.split()

class DirectorValidateSerializers(serializers.Serializer):
    name = serializers.CharField(min_length=2, max_length=200)

class MovieValidateSerializers(serializers.Serializer):
    title = serializers.CharField(min_length=2, max_length=200)
    description = serializers.CharField(required=False)
    duration = serializers.FloatField(min_value=0.5, max_value=10)
    director_id = serializers.IntegerField(min_value=1)

    def validate_director_id(self, director_id):
        try:
            Director.objects.get(id=director_id)
        except Director.DoesNotExist:
            raise ValidationError("Director does not exist!")
        return director_id

class ReviewValidateSerializers(serializers.Serializer):
    text = serializers.CharField()
    stars = serializers.IntegerField(default=5, max_value=5, min_value=1)
    movie_id = serializers.IntegerField(min_value=1)

    def validate_movie_id(self, movie_id):
        try:
            Movie.objects.get(id=movie_id)
        except Movie.DoesNotExist:
            raise ValidationError("Movie does not exist!")
        return movie_id
