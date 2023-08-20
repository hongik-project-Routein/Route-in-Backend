import os
from uuid import uuid4
from django.db import models
from accounts.models import User
from django.utils import timezone


# media 파일 업로드 함수
def upload_to_func(instance, filename):
    prefix = timezone.now().strftime("%Y/%m/%d")
    file_name = uuid4().hex
    extension = os.path.splitext(filename)[-1].lower()
    return "/".join(
        [prefix, file_name, extension, ]
    )


# BaseModel (subclass models: Post, Comment)
class BaseModel(models.Model):
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True

    def delete(self, using=None, keep_parents=False):
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save()


# MapInfoModel (subclass models: Pin, Story)
class MapInfoModel(models.Model):
    mapID = models.CharField('MAPID', max_length=30, blank=True)
    latitude = models.DecimalField('LATITUDE', max_digits=18, decimal_places=15, blank=True, null=True)
    longitude = models.DecimalField('LONGITUDE', max_digits=18, decimal_places=15, blank=True, null=True)

    class Meta:
        abstract = True


# Post
class Post(BaseModel):
    writer = models.ForeignKey(User, related_name='post_set', on_delete=models.CASCADE, )
    content = models.TextField('CONTENT', max_length=200, blank=True)
    like_users = models.ManyToManyField(User, related_name='like_posts', blank=True)
    bookmark_users = models.ManyToManyField(User, related_name='bookmark_posts', blank=True)
    tagged_users = models.ManyToManyField(User, related_name='tagging_posts', blank=True)
    report_count = models.IntegerField('REPORT_COUNT', default=0)

    def __str__(self):
        return f'{self.writer}: {self.content[:10]}' or ''


# Pin
class Pin(MapInfoModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='pins')
    image = models.ImageField('IMAGE', upload_to=upload_to_func)
    pin_hashtag = models.CharField('PIN_HASHTAG', max_length=20, blank=True, null=True)
    content = models.TextField('SUB_CONTENT', max_length=200, blank=True, null=True)

    def __str__(self):
        return f'{self.post}) {self.content[:10]}' or ''


# Comment
class Comment(BaseModel):
    writer = models.ForeignKey(User, on_delete=models.CASCADE, )
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField('CONTENT', max_length=200)
    like_users = models.ManyToManyField(User, related_name='like_comments', blank=True)
    tagged_users = models.ManyToManyField(User, related_name='tagging_comments', blank=True)

    def __str__(self):
        return f'{self.post}) {self.writer}: {self.content[:10]}' or ''


# Hashtag
class Hashtag(models.Model):
    post = models.ForeignKey(Post, related_name='hashtags', on_delete=models.CASCADE, )
    name = models.CharField('NAME', max_length=20, unique=True)

    def __str__(self):
        return f'{self.post}) {self.name}' or ''
