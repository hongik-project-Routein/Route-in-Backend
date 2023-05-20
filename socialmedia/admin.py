from django.contrib import admin
from .models import Post, Pin, Comment, Story, Hashtag

admin.site.register(Post)
admin.site.register(Pin)
admin.site.register(Comment)
admin.site.register(Story)
admin.site.register(Hashtag)
