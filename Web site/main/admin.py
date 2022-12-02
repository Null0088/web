from django.contrib import admin
from .forms import RegisterForm
from .models import Music,Post

admin.site.register(Music)
admin.site.register(Post)