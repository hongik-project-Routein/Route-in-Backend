from django.contrib.auth.models import User
from rest_framework import serializers

from socialmedia.models import Post, Pin, Comment, Story, Hashtag


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class PostListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'
class PostRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'

class PinListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pin
        fields = '__all__'
class PinRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pin
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

class StoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Story
        fields = '__all__'
class StoryRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Story
        fields = '__all__'