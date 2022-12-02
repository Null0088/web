from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("home/", views.home, name="home"),
    path("sign-up/", views.sign_up, name="sign_up"),
    path("create-post/", views.create_post, name="create_post"),
    path("view/", views.views, name="views"),
    path("password_change/", views.password_change, name="password_change"),
    path("music_upload/", views.music_upload, name="music_upload"),
    path("music_play/", views.music_play, name="music_play"),
    path("search/", views.search, name="search"),
    path("video_upload/", views.video_upload, name="video_upload"),
    path("video_play/", views.video_play, name="video_play"),
    path(
        "reset_password/",
        auth_views.PasswordResetView.as_view(template_name="main/password_reset.html"),
        name="reset_password",
    ),
    path(
        "reset_password_sent/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="main/password_reset_sent.html"
        ),
        name="reset_password_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "reset_password_complete/",
        auth_views.PasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
]
