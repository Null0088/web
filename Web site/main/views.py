from django.shortcuts import render, redirect
from .forms import RegisterForm, PostForm, password_Change, MusicForm, VideoForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User, Group
from .models import Post, Password, File, Music, Video
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from django.contrib import messages
import os
from django.conf import settings


@login_required(login_url="/login")
def home(request):
    posts = Post.objects.all()

    if request.method == "POST":
        post_id = request.POST.get("post-id")
        user_id = request.POST.get("user-id")
        image_id = request.POST.get("image-id")
        file_id = request.POST.get("image-id")
        if post_id:
            post = Post.objects.filter(id=post_id).first()
            post.delete()
            messages.success(request, "Post Deleted Successfully")
        elif image_id:
            post = Post.objects.filter(id=file_id).first()
            post_file = str(post.file)
            os.remove(os.path.join(settings.MEDIA_ROOT, post_file))
            post.file.delete()
            messages.success(request, "Image Deleted Successfully")
    return render(request, "main/home.html", {"posts": posts})


@login_required(login_url="/login")
def create_post(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, "Post Created Successfully")
            return redirect("/home")
    else:
        form = PostForm()

    return render(request, "main/create_post.html", {"form": form})


def sign_up(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            messages.success(request, "Signed Up Successfully")
            user = form.save()
            logout(request)
            return redirect("/home")
    else:
        form = RegisterForm()

    return render(request, "registration/sign_up.html", {"form": form})


def views(request):
    posts = Post.objects.all()
    User = get_user_model()
    users = User.objects.all()
    if request.method == "POST":
        user_id = request.POST.get("user-id")
        if user_id:
            user = User.objects.filter(id=user_id).first()
            user.delete()
            messages.success(request, "User Deleted Successfully")
    return render(request, "main/view.html", {"user_list": users})


@login_required(login_url="/login")
def password_change(request):
    if request.method == "POST":
        form = password_Change(request.POST)
        if form.is_valid():
            old_password = form.cleaned_data["old_password"]
            new_password = form.cleaned_data["new_password"]
            username = request.user.username
            usr = User.objects.get(username=username)
            if check_password(old_password, usr.password):
                usr.set_password(new_password)
                usr.save()
                login(request, usr)
                messages.success(request, "Password Changed Successfully")
                return redirect("/home")
        else:
            form = password_Change()

    return render(request, "main/password_change.html", {"form": form})


@login_required(login_url="/login")
def music_upload(request):
    if request.method == "POST":
        form = MusicForm(request.POST, request.FILES)
        if form.is_valid():
            title = form.cleaned_data["title"]
            genre = form.cleaned_data["genre"]
            music = form.save(commit=False)
            music.artist = request.user
            music.save()
            print(music.music_file)
            form.save()
            messages.success(request, "Music Uploaded Successfully")
            return redirect("/home")

    else:
        form = MusicForm()
    return render(
        request,
        "main/music_upload.html",
        {
            "form": form,
        },
    )


@login_required(login_url="/login")
def music_play(request):
    musics = Music.objects.all()

    if request.method == "POST":
        music_del_id = request.POST.get("music-del-id")
        music_id = request.POST.get("music-id")
        if music_id:
            music = musics.filter(id=music_id).first()
            return render(request, "main/player.html", {"music": music})
        elif music_del_id:
            music = musics.filter(id=music_del_id).first()
            music_file = str(music.music_file)
            os.remove(os.path.join(settings.MEDIA_ROOT, music_file))
            music.delete()
            messages.success(request, "Music Deleted Successfully")
            return redirect('/')
    return render(request, "main/music_play.html", {"musics": musics})


@login_required(login_url="/login")
def video_upload(request):
    if request.method == "POST":
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            video = form.save(commit=False)
            video.creator = request.user
            video.save()
            form.save()
            messages.success(request, "Video Uploaded Successfully")
            return redirect("/home")

    else:
        form = VideoForm()
    return render(
        request,
        "main/video_upload.html",
        {
            "form": form,
        },
    )


def video_play(request):
    video = Video.objects.all()
    if request.method == "POST":
        video_del_id = request.POST.get("video-del-id")
        video_id = request.POST.get("video-id")
        if video_id:
            video = video.filter(id=video_id).first()
            return render(request, "main/player.html", {"video": video})
        elif video_del_id:
            video = video.filter(id=video_del_id).first()
            video_file = str(video.video)
            os.remove(os.path.join(settings.MEDIA_ROOT, video_file))
            video.delete()
            messages.success(request, "Video Deleted Successfully")
            return redirect('/')
    return render(request, "main/video_play.html", {"videos": video})


def search(request):
    if request.method == "POST":
        searched = request.POST["searched"]
        posts_data = Post.objects.filter(
            title__contains=searched
        ) | Post.objects.filter(description__contains=searched)
        users_data = User.objects.filter(
            username__contains=searched
        ) | User.objects.filter(email__contains=searched)
        music_data = Music.objects.filter(
            genre__contains=searched
        ) | Music.objects.filter(title__contains=searched)

        video_data = Video.objects.filter(
            title__contains=searched
        ) | Video.objects.filter(description__contains=searched)
        return render(
            request,
            "main/search.html",
            {
                "searched": searched,
                "posts": posts_data,
                "users": users_data,
                "musics": music_data,
                "videos": video_data,
            },
        )
    else:
        return redirect('/')
