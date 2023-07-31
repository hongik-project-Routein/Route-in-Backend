from django.contrib import admin
from .models import Post, Pin, Comment, Hashtag

admin.site.register(Post)
admin.site.register(Pin)
admin.site.register(Comment)
admin.site.register(Hashtag)
