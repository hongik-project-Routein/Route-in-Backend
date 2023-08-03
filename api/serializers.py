from rest_framework import serializers
from socialmedia.models import Post, Pin, Comment, Story, Hashtag
from account.models import User
from decimal import Decimal


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


# Pin Detail Serializer
class PinDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Pin
        fields = ['image', 'latitude', 'longitude']


# Pin Serializer (for Post Create Serializer)
class PinSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(max_length=None, allow_empty_file=True, use_url=True)

    class Meta:
        model = Pin
        fields = ['image', 'pin_hashtag', 'content', 'latitude', 'longitude', 'mapID']


# Post Create Serializer
class PostCreateSerializer(serializers.ModelSerializer):
    pins = PinSerializer(many=True)

    class Meta:
        model = Post
        fields = ['content', 'pins']

    def create(self, validated_data):
        pins_data = validated_data.pop('pins')
        post = Post.objects.create(**validated_data)

        for pdata in pins_data:
            image_data = pdata.pop('image')
            lat_data = pdata.pop('latitude')
            lng_data = pdata.pop('longitude')

            pin = Pin.objects.create(post=post, image=image_data, latitude=Decimal(lat_data), longitude=Decimal(lng_data), **pdata)
            pin.image.save(image_data.name, image_data, save=True)

        return post


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


# Post Retrieve Serializer
class PostRetrieveSerializer(serializers.Serializer):
    post = PostSerializer()
    pin = PinDetailSerializer(many=True)
    user = UserImageSerializer()
    comment = CommentSerializer(many=True)
