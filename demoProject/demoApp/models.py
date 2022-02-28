# from os import access
from datetime import timedelta
from email.policy import default
from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models

# Create your models here.
class Genre(models.Model):
    name = models.CharField(max_length=20, null= True)

    def __str__(self):
        return self.name 

class Movie(models.Model):
    title = models.CharField(max_length=50)
    language = models.CharField(max_length=20, blank = False)
    duration = models.DurationField(default=timedelta())
    release = models.DateField()
    country = models.CharField(max_length=20)
    description = models.TextField()
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    image = models.ImageField(default = "", upload_to="image/")
    def __str__(self):
        return self.title
class Artist(models.Model):
    name = models.CharField(max_length=20)
    def __str__(self):
        return self.name

class MovieArtist(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    artist  = models.ForeignKey(Artist, on_delete=models.CASCADE)
    a_typeChoice = (
        ("actor", "actor"),
        ("director", "director"),
        ("producer", "producer"),
    )
    a_type = models.CharField(max_length=20, choices=a_typeChoice)
    def __str__(self):
        return self.a_type

class User(AbstractBaseUser):
    
    
    firstname = models.CharField(max_length=20)
    lastname = models.CharField(max_length=20)
    mobile = models.CharField(max_length=13, unique=True)
    password = models.CharField(max_length=200, null= False, blank= False)
    confirm_password = models.CharField(max_length=200, null = False, blank= False)
    username = None
    email = models.EmailField(unique=True) 
    is_superuser = models.BooleanField(default = False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    