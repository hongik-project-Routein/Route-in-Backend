import os
from uuid import uuid4
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# media 파일 업로드 함수
def upload_to_func(instance, filename):
    prefix = timezone.now().strftime("%Y/%m/%d")
    file_name = uuid4().hex
    extension = os.path.splitext(filename)[-1].lower()
    return "/".join(
        [prefix, file_name, extension, ]
    )


class BaseModel(models.Model):
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True

    def delete(self, using=None, keep_parents=False):
        self.is_deleted = True,
        self.deleted_at = timezone.now()
        self.save()


class MapInfoModel(models.Model):
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)

    class Meta:
        abstract = True


class Post(BaseModel):
    writer = models.ForeignKey(User, on_delete=models.CASCADE, )
    content = models.TextField('CONTENT', max_length=200, blank=True)
    main_image = models.ImageField('MAIN_IMAGE', upload_to=upload_to_func)
    # like_users = models.ManyToManyField('LIKE_USERS', )
    # bookmark_users = models.ManyToManyField('BOOKMARK_USERS', )
    # tagged_users = models.ManyToManyField('TAGGED_USERS', )
    pin_count = models.IntegerField('PIN_COUNT', default=0)
    report_count = models.IntegerField('REPORT_COUNT', default=0)

    @property
    def short_content(self):
        return '{}: {}'.format(self.writer, self.content[:10])

    def __str__(self):
        return self.short_content


class Pin(MapInfoModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, )
    image = models.ImageField('IMAGE', upload_to=upload_to_func)

    def __str__(self):
        return self.name


class Comment(BaseModel):
    writer = models.ForeignKey(User, on_delete=models.CASCADE, )
    post = models.ForeignKey(Post, on_delete=models.CASCADE, )
    content = models.TextField('CONTENT', max_length=200, blank=True)
    is_reply = models.BooleanField(default=False)
    # like_users = models.ManyToManyField('LIKE_USERS', )
    # tagged_users = models.ManyToManyField('TAGGED_USERS', )

    @property
    def short_content(self):
        return self.content[:10]

    def __str__(self):
        return self.short_content


class Story(BaseModel, MapInfoModel):
    writer = models.ForeignKey(User, on_delete=models.CASCADE, )
    image = models.ImageField('IMAGE', upload_to=upload_to_func)
    # like_users = models.ManyToManyField('LIKE_USERS', )
    # tagged_users = models.ManyToManyField('TAGGED_USERS', )
    report_count = models.IntegerField('REPORT_COUNT', default=0)


class Hashtag(models.Model):
    name = models.CharField('NAME', max_length=20)

    def __str__(self):
        return self.name