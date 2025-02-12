from django.db import models

class Director(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    def movies_count(self):
        return self.movies.count()

class Movie(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    duration = models.FloatField()
    director = models.ForeignKey(Director, related_name='movies', on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def rating(self):
        ratings = self.reviews.all().values_list('stars', flat=True)
        return sum(ratings) / len(ratings) if ratings else 0

STARS = (
    (1, '*'),
    (2, '* *'),
    (3, '* * *'),
    (4, '* * * *'),
    (5, '* * * * *'),
)

class Review(models.Model):
    text = models.TextField()
    stars = models.IntegerField(default=5, choices=STARS, null=True)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='reviews')

    def __str__(self):
        return self.text


