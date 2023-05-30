from django.contrib.auth.models import User
from rest_framework import serializers
from socialmedia.models import Post, Pin, Comment, Story, Hashtag

# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = '__all__'
#
# class PostSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Post
#         fields = '__all__'

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'


class PinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pin
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class StorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Story
        fields = '__all__'