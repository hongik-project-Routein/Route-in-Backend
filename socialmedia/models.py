import os
from uuid import uuid4

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


def upload_to_func(instance, filename):
    prefix = timezone.now().strftime("%Y/%m/%d")
    file_name = uuid4().hex
    extension = os.path.splitext(filename)[-1].lower()  # 확장자 추출
    return "/".join(
        [prefix, file_name, extension, ]
    )

class BaseModel(models.Model):
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True

    def delete(self, using=None, keep_parents=False):
        self.is_deleted = True,
        self.deleted_at = timezone.now()
        self.save()


class Post(BaseModel):
    # user = models.ForeignKey('User', on_delete=models.CASCADE, )
    content = models.TextField('CONTENT')
    main_image = models.ImageField('MAIN_IMAGE', upload_to=upload_to_func)
    # like_users = models.ManyToManyField('LIKE_USERS', )
    # bookmark_users = models.ManyToManyField('BOOKMARK_USERS', )
    # tagged_users = models.ManyToManyField('TAGGED_USERS', )
    pin_count = models.IntegerField('PIN_COUNT', default=0)
    report_count = models.IntegerField('REPORT_COUNT', default=0)


class Pin(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE, )
    image = models.ImageField('IMAGE', upload_to=upload_to_func)
    name = models.CharField('NAME', max_length=20)
    '''
    location
    '''


class Comment(BaseModel):
    # user = models.ForeignKey('User', on_delete=models.CASCADE, )
    post = models.ForeignKey('Post', on_delete=models.CASCADE, )
    is_reply = models.BooleanField(default=False)
    # like_users = models.ManyToManyField('LIKE_USERS', )
    # tagged_users = models.ManyToManyField('TAGGED_USERS', )


class Story(BaseModel):
    # user = models.ForeignKey('User', on_delete=models.CASCADE, )
    image = models.ImageField('IMAGE', upload_to=upload_to_func)
    # like_users = models.ManyToManyField('LIKE_USERS', )
    # tagged_users = models.ManyToManyField('TAGGED_USERS', )
    '''
    location
    '''
    report_count = models.IntegerField('REPORT_COUNT', default=0)


class Hashtag(models.Model):
    name = models.CharField('NAME', max_length=20)

    def __str__(self):
        return self.name