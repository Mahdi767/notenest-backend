from django.contrib import admin
from .models import Like, Bookmark, Comment

admin.site.register(Like)
admin.site.register(Bookmark)
admin.site.register(Comment)