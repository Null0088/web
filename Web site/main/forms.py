from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Post, Password, File, Music, Video
from django.contrib.auth.password_validation import validate_password


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    GENDERS = [
        ("Men", "Men"),
        ("Women", "Women"),
    ]
    gender = forms.CharField(
        label="Gender", widget=forms.RadioSelect(choices=GENDERS), required=True
    )

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2", "gender"]


class password_Change(forms.ModelForm):
    old_password = forms.PasswordInput()
    new_password = forms.CharField(
        widget=forms.PasswordInput, validators=[validate_password]
    )

    class Meta:
        model = Password
        fields = ["old_password", "new_password"]


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "description", "file"]


class MusicForm(forms.ModelForm):
    class Meta:
        model = Music
        fields = ["title", "genre", "music_file"]


class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ["title", "description", "video"]
