from rest_framework import serializers
from .models import Director, Movie, Review


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