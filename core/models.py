from django.db import models


class Musician(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    instrument = models.CharField(max_length=100)

    def __str__(self) -> str:
        return f"{self.first_name}-{self.instrument}"


class Album(models.Model):
    artist = models.ForeignKey(Musician, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    release_date = models.DateField(auto_now=True)
    num_stars = models.IntegerField(default=0)

    def __str__(self) -> str :
        return f"{self.artist.first_name} {self.artist.last_name}-{self.name}"