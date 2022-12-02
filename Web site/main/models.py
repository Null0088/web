from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    file = models.ImageField(null=True, blank=True, upload_to="images/")

    def __str__(self):
        return self.title + "\n" + self.description


class File(models.Model):
    uploader = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    file = models.FileField(null=True, blank=True, upload_to="files/")


class Password(models.Model):
    old_password = models.CharField(max_length=100)
    new_password = models.CharField(max_length=100)


class Music(models.Model):
    GENRES = (
        ("Pop", "Pop"),
        ("Hiphop", "Hiphop"),
        ("Rap", "Rap"),
        ("Rock", "Rock"),
        ("Jazz", "Jazz"),
        ("Country", "Country"),
    )
    title = models.CharField(max_length=200)
    artist = models.ForeignKey(User, on_delete=models.CASCADE)
    genre = models.CharField(max_length=200, choices=GENRES)
    music_file = models.FileField(
        null=True,
        upload_to="musics/",
        validators=[FileExtensionValidator(allowed_extensions=["mp3", "ogg", "wav"])],
    )


class Video(models.Model):
    video = models.FileField(
        upload_to="video/",
        null=True,
        validators=[
            FileExtensionValidator(
                allowed_extensions=["MOV", "avi", "mp4", "webm", "mkv"]
            )
        ],
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
