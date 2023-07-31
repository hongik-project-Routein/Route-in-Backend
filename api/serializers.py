from rest_framework import serializers
from socialmedia.models import Post, Pin, Comment, Hashtag
from accounts.models import User
from decimal import Decimal


# User Serializer
class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'


# User ImageSerializer
class UserImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(max_length=None, allow_empty_file=True, use_url=True)

    class Meta:
        model = User
        fields = ['image']


# Post 목록 Serializer
# called by: PostRetrieveSerializer
class PostSerializer(serializers.ModelSerializer):
    writer = serializers.ReadOnlyField(source='writer.name')
    like_users = serializers.StringRelatedField(many=True)
    bookmark_users = serializers.StringRelatedField(many=True)
    tagged_users = serializers.StringRelatedField(many=True)
    is_liked = serializers.SerializerMethodField()
    like_count = serializers.SerializerMethodField()
    pin_count = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField()

    def get_is_liked(self, obj):
        cur_user = self.context.get('request').user
        return obj.like_users.filter(id=cur_user.id).exists()

    def get_like_count(self, obj):
        return obj.like_users.count()

    def get_pin_count(self, obj):
        return obj.pins.count()

    def get_comment_count(self, obj):
        return obj.comments.count()

    class Meta:
        model = Post
        fields = ['id', 'writer', 'content', 'is_liked', 'pin_count', 'like_count', 'report_count', 'like_users', 'bookmark_users', 'tagged_users', 'comment_count']


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
# called by: PostRetreieveSerializer
class PinDetailSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(max_length=None, allow_empty_file=True, use_url=True)

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
# called by: PostCommentListView, PostRetrieveSerializer
class CommentSerializer(serializers.ModelSerializer):
    writer_image = serializers.ImageField(source='writer.image', required=False)
    writer = serializers.ReadOnlyField(source='writer.name')
    like_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    tagged_users = serializers.StringRelatedField(many=True)

    def get_like_count(self, obj):
        return obj.like_users.count()

    def get_is_liked(self, obj):
        cur_user = self.context.get('request').user
        return obj.like_users.filter(id=cur_user.id).exists()

    class Meta:
        model = Comment
        fields = ['id', 'writer_image', 'writer', 'content', 'tagged_users', 'updated_at', 'post', 'like_count', 'is_liked']


# Hashtag Serializer
class HashtagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Hashtag
        fields = ['id', 'name']


# Post 상세 Serializer
# called by: PostRetrieveAPIView
class PostRetrieveSerializer(serializers.Serializer):
    post = PostSerializer()
    pin = PinDetailSerializer(many=True)
    user = UserImageSerializer()
    comment = CommentSerializer(many=True)


# Post 목록 Serializer
# called by: PostListAPIView
class PostListSerializer(serializers.Serializer):
    post = PostSerializer()
    pin = PinDetailSerializer(many=True)
    user = UserImageSerializer()
    comment = CommentSerializer(many=True)