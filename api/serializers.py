from rest_framework import serializers
from socialmedia.models import Post, Pin, Comment, Hashtag
from accounts.models import User
from decimal import Decimal


# User ImageSerializer
class UserImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(max_length=None, allow_empty_file=True, use_url=True)

    class Meta:
        model = User
        fields = ['image']


'''
called by:
    UserFollowAPIView
'''
class UserFollowSerializer(serializers.ModelSerializer):
    follow_count = serializers.ReadOnlyField()

    class Meta:
        model = User
        fields = ['follow_count', ]

'''
called by:
    PostRetrieveSerializer
'''
class PostSerializer(serializers.ModelSerializer):
    writer = serializers.ReadOnlyField(source='writer.uname')
    like_users = serializers.StringRelatedField(many=True)
    bookmark_users = serializers.StringRelatedField(many=True)
    tagged_users = serializers.StringRelatedField(many=True)
    is_liked = serializers.SerializerMethodField()
    is_bookmarked = serializers.SerializerMethodField()
    hashtags = serializers.StringRelatedField(many=True)
    like_count = serializers.SerializerMethodField()
    pin_count = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField()

    def get_is_liked(self, obj):
        cur_user = self.context.get('request').user
        return obj.like_users.filter(id=cur_user.id).exists()

    def get_is_bookmarked(self, obj):
        cur_user = self.context.get('request').user
        return obj.bookmark_users.filter(id=cur_user.id).exists()

    def get_like_count(self, obj):
        return obj.like_users.count()

    def get_pin_count(self, obj):
        return obj.pins.count()

    def get_comment_count(self, obj):
        return obj.comments.filter(is_deleted=False).count()

    class Meta:
        model = Post
        fields = ['id', 'writer', 'content', 'is_liked', 'is_bookmarked', 'hashtags', 'pin_count', 'like_count', 'report_count', 'like_users', 'bookmark_users', 'tagged_users', 'comment_count']


'''
called by:
    UserListAPIView, UserRetrieveAPIView
'''
class UserSerializer(serializers.ModelSerializer):
    following_set = serializers.SerializerMethodField()
    follower_set = serializers.SerializerMethodField()
    image = serializers.ImageField(max_length=None, allow_empty_file=True, use_url=True)

    def get_following_set(self, obj):
        return obj.following_set.all().values_list('uname', flat=True)

    def get_follower_set(self, obj):
        return obj.follower_set.all().values_list('uname', flat=True)

    class Meta:
        model = User
        fields = ['uname', 'id', 'last_login', 'email', 'name', 'introduction', 'age', 'gender', 'image', 'following_set', 'follower_set', 'post_set']


'''
called by:
    PostLikeAPIView
'''
class PostLikeSerializer(serializers.ModelSerializer):
    like_count = serializers.ReadOnlyField()
    like_users = serializers.StringRelatedField(many=True)

    class Meta:
        model = Post
        fields = ['like_count', 'like_users']


'''
called by:
    PostBookmarkAPIView
'''
class PostBookmarkSerializer(serializers.ModelSerializer):
    bookmark_users = serializers.StringRelatedField(many=True)

    class Meta:
        model = Post
        fields = ['bookmark_users']


'''
called by:
    PostTagAPIView, PostTagListAPIView
'''
class PostTagSerializer(serializers.ModelSerializer):
    tagged_users = serializers.StringRelatedField(many=True)

    class Meta:
        model = Post
        fields = ['tagged_users']


'''
called by:
    PostRetrieveSerializer
'''
class PinDetailSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(max_length=None, allow_empty_file=True, use_url=True)

    class Meta:
        model = Pin
        fields = ['image', 'latitude', 'longitude', 'pin_hashtag', ]


'''
called by:
    PostUpdateSerializer
'''
class PinUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pin
        fields = ['id', 'image', 'latitude', 'longitude']


# Pin Serializer (for Post Create Serializer)
class PinSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(max_length=None, allow_empty_file=True, use_url=True)

    class Meta:
        model = Pin
        fields = ['image', 'pin_hashtag', 'content', 'latitude', 'longitude', 'mapID']


'''
called by:
    PostCreateAPIView
'''
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


'''
called by:
    PostUpdateAPIView
'''
class PostUpdateSerializer(serializers.ModelSerializer):
    pins = PinUpdateSerializer(many=True)

    class Meta:
        model = Post
        fields = ['content', 'pins']

    def update(self, instance, validated_data):
        pins_data = validated_data.pop('pins')
        pins_instances = instance.pins.all()

        instance.content = validated_data.get('content', instance.content)
        instance.save()

        for pin_instance, pin_data in zip(pins_instances, pins_data):
            pin_instance.image = pin_data.get('image', pin_instance.image)
            pin_instance.latitude = pin_data.get('latitude', pin_instance.latitude)
            pin_instance.longitude = pin_data.get('longitude', pin_instance.longitude)
            pin_instance.save()

        return instance


'''
called by:
    PostCommentListView
    PostRetrieveSerializer
'''
class CommentSerializer(serializers.ModelSerializer):
    writer_image = serializers.ImageField(source='writer.image', required=False)
    writer = serializers.ReadOnlyField(source='writer.uname')
    like_users = serializers.StringRelatedField(many=True)
    like_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    tagged_users = serializers.StringRelatedField(many=True)

    def get_like_count(self, obj):
        return obj.like_users.count()

    def get_like_users(self, obj):
        return obj.like_users

    def get_is_liked(self, obj):
        cur_user = self.context.get('request').user
        return obj.like_users.exists()

    class Meta:
        model = Comment
        fields = ['id', 'writer_image', 'writer', 'content', 'tagged_users', 'updated_at', 'post', 'like_users', 'like_count', 'is_liked']


'''
called by:
    CommentLikeAPIView
'''
class CommentLikeSerializer(serializers.ModelSerializer):
    like_count = serializers.ReadOnlyField()
    like_users = serializers.StringRelatedField(many=True)

    class Meta:
        model = Comment
        fields = ['like_count', 'like_users']


'''
called by:
    CommentTagAPIView, CommentTagListAPIView
'''
class CommentTagSerializer(serializers.ModelSerializer):
    tagged_users = serializers.StringRelatedField(many=True)

    class Meta:
        model = Comment
        fields = ['tagged_users']


# Hashtag Serializer
class HashtagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Hashtag
        fields = ['id', 'name']


'''
called by:
    PostRetrieveAPIView
'''
class PostRetrieveSerializer(serializers.Serializer):
    post = PostSerializer()
    pin = PinDetailSerializer(many=True)
    user = UserImageSerializer()
    comment = CommentSerializer(many=True)


'''
called by:
    PostListAPIView
'''
class PostListSerializer(serializers.Serializer):
    post = PostSerializer()
    pin = PinDetailSerializer(many=True)
    user = UserImageSerializer()
    comment = CommentSerializer(many=True)


'''
called by:
    UserRetrieveAPIView
'''
class UserRetrieveSerializer(serializers.ModelSerializer):
    post_set = serializers.SerializerMethodField()

    def get_post_set(self, obj):
        posts = obj.post_set.filter(is_deleted=False)
        post_data = []
        for post in posts:
            post_data.append({
                'post': PostSerializer(post, context=self.context).data,
                'pin': PinDetailSerializer(post.pins.all(), many=True, context=self.context).data,
                'user': UserImageSerializer(post.writer, context=self.context).data,
                'comment': CommentSerializer(post.comments.filter(is_deleted=False), many=True, context=self.context).data,
            })
        return post_data

    class Meta:
        model = User
        fields = ['uname', 'id', 'last_login', 'email', 'name', 'introduction', 'age', 'gender', 'image', 'following_set', 'follower_set', 'post_set']


'''
called by:
    InitialSettingAPIView
'''
class InitialSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['uname', 'name', 'age', 'gender']