from django.db import models
from django.utils import timezone


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
    # user = models.ForeignKey()
    # content = models.TextField()
    # main_image_url = models.URLField()
    # like_users = models.ManyToManyField()
    # bookmark_users = models.ManyToManyField()
    # tagged_users = models.ManyToManyField()
    # pin_count = models.IntegerField()
    # report_count = models.IntegerField()
    pass


class Pin(models.Model):
    # post = models.ForeignKey(Post, on_delete=models.CASCADE)
    # image_url = models.URLField()
    # name = models.CharField(max_length=20)
    # location
    pass

class Comment(BaseModel):
    # user = models.ForeignKey()
    # post = models.ForeignKey(Post, on_delete=models.CASCADE)
    # is_reply = models.BooleanField(default=False)
    # like_users = models.ManyToManyField()
    # tagged_users = models.ManyToManyField()
    pass

class Story(BaseModel):
    # user = models.ForeignKey()
    # image_url = models.URLField()
    # like_users = models.ManyToManyField()
    # tagged_users = models.ManyToManyField()
    # location
    # report_count = models.IntegerField()
    pass
