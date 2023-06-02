from rest_framework import serializers
from socialmedia.models import Post, Pin, Comment, Story, Hashtag
from account.models import User


# class UserSerializer1(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['image']
#
# class LatLngSerializer(serializers.Serializer):
#     lat = serializers.DecimalField()
#     lng = serializers.DecimalField()
#
#     # class Meta:
#     #     model = Pin
#     #     fields = ['latitude', 'longitude']
#
#
# class PinSerializer1(serializers.ModelSerializer):
#     latLng = LatLngSerializer(many=True)
#
#     class Meta:
#         model = Pin
#         fields = ['image', 'latLng']
#
#
# class PostSerializer1(serializers.ModelSerializer):
#     user = UserSerializer1()
#     pin = PinSerializer1()
#     post = serializers.SerializerMethodField()
#
#     class Meta:
#         model = Post
#         fields = ['post', 'user', 'pin']
#
#     def get_post(self, obj):
#         return {
#             'id': 'obj.id',
#             'writer': 'obj.writer',
#             'content': 'obj.content',
#             'pinCount': 'obj.pinCount',
#             'like_users': 'obj.like_users',
#             'bookmark_users': 'obj.bookmark_users',
#             'tagged_users': 'obj.tagged_users',
#             'comment_count': 'obj.comment_count',
#         }


# User 시리얼라이저
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


# Post 시리얼라이저
class PostSerializer(serializers.ModelSerializer):
    writer = serializers.ReadOnlyField(source='writer.name')
    like_users = serializers.StringRelatedField(many=True)
    bookmark_users = serializers.StringRelatedField(many=True)
    class Meta:
        model = Post
        fields = ['id', 'is_deleted', 'created_at', 'updated_at', 'deleted_at', \
                  'content', 'like_count', 'pin_count', 'report_count', 'writer', \
                  'like_users', 'bookmark_users']


# Post 좋아요 시리얼라이저
class PostLikeSerializer(serializers.ModelSerializer):
    like_count = serializers.ReadOnlyField()

    class Meta:
        model = Post
        fields = ['like_count', 'like_users']


# Post 북마크 시리얼라이저
class PostBookmarkSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ['bookmark_users']


# Comment Sub 시리얼라이저 (for PostDetailSerializer)
class CommentSubSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'content', 'updated_at']


# Post Detail 시리얼라이저
class PostDetailSerializer(serializers.Serializer):
    post = PostSerializer()
    comment_list = CommentSubSerializer(many=True)


# Pin 시리얼라이저
class PinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pin
        fields = '__all__'


# Comment 시리얼라이저
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


# Story 시리얼라이저
class StorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Story
        fields = '__all__'


# Hashtag 시리얼라이저
class HashtagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hashtag
        fields = ['name']
