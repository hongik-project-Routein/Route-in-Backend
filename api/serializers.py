from rest_framework import serializers
from socialmedia.models import Post, Pin, Comment, Story, Hashtag
from account.models import User


# User Serializer
class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'


# User ImageSerializer
class UserImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['image']

# Post Serializer
class PostSerializer(serializers.ModelSerializer):
    writer = serializers.ReadOnlyField(source='writer.name')
    like_users = serializers.StringRelatedField(many=True)
    bookmark_users = serializers.StringRelatedField(many=True)
    like_count = serializers.SerializerMethodField()
    pin_count = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField()

    def get_like_count(self, obj):
        return obj.like_users.count()

    def get_pin_count(self, obj):
        return obj.pins.count()

    def get_comment_count(self, obj):
        return obj.comments.count()

    class Meta:
        model = Post
        fields = ['id', 'writer', 'content', 'pin_count', 'like_count', 'report_count', 'like_users', 'bookmark_users', 'comment_count']


# Post Like Serializer
class PostLikeSerializer(serializers.ModelSerializer):
    like_count = serializers.ReadOnlyField()
    like_users = serializers.StringRelatedField(many=True)

    class Meta:
        model = Post
        fields = ['like_count', 'like_users']


# Post Bookmark Serializer
class PostBookmarkSerializer(serializers.ModelSerializer):
    bookmark_users = serializers.StringRelatedField(many=True)

    class Meta:
        model = Post
        fields = ['bookmark_users']


# Comment Sub Serializer (for PostDetailSerializer)
class CommentSubSerializer(serializers.ModelSerializer):
    writer = serializers.ReadOnlyField(source='writer.name')

    class Meta:
        model = Comment
        fields = ['id', 'writer', 'content', 'updated_at']


# Post Detail Serializer
class PostDetailSerializer(serializers.Serializer):
    post = PostSerializer()
    comment_list = CommentSubSerializer(many=True)


# Pin Serializer
class PinDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Pin
        fields = ['image', 'latitude', 'longitude']


# Pin Serializer
class PinSerializer(serializers.ModelSerializer):

    class Meta:
        model = Pin
        fields = '__all__'


# Comment Serializer
class CommentSerializer(serializers.ModelSerializer):
    writer = serializers.ReadOnlyField(source='writer.name')
    like_count = serializers.SerializerMethodField()

    def get_like_count(self, obj):
        return obj.like_users.count()

    class Meta:
        model = Comment
        fields = ['id', 'updated_at', 'post', 'writer', 'content', 'like_count']


# Story Serializer
class StorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Story
        fields = '__all__'


# Hashtag Serializer
class HashtagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Hashtag
        fields = ['id', 'name']


#############
# 프론트 요청 #
############


# Post Retrieve Serializer
class PostRetrieveSerializer(serializers.Serializer):
    post = PostSerializer()
    pin = PinDetailSerializer(many=True)
    user = UserImageSerializer()
    comment = CommentSerializer(many=True)
