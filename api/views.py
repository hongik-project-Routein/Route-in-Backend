import rest_framework.permissions
from rest_framework import status
from rest_framework.parsers import MultiPartParser
from rest_framework.views import APIView
from account.models import User
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, get_object_or_404, ListAPIView, \
    RetrieveAPIView, RetrieveDestroyAPIView, CreateAPIView
from rest_framework.response import Response
from .serializers import PostSerializer, PostLikeSerializer, PinDetailSerializer, CommentSerializer, StorySerializer, \
    HashtagSerializer, PostBookmarkSerializer, UserSerializer, PostRetrieveSerializer, \
    PinSerializer, PostCreateSerializer
from socialmedia.models import Post, Pin, Comment, Story, Hashtag


# User List
class UserListAPIView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


# User Retrieve
class UserRetrieveAPIView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


# Post List
class PostListAPIView(ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        data = serializer.data

        for item in data:
            post_id = item['id']
            item['pin'] = Pin.objects.filter(post_id=post_id).values('image', 'latitude', 'longitude')
            item['user'] = User.objects.filter(name=item['writer']).values('image')
            item['comment'] = Comment.objects.filter(post_id=post_id).values('id', 'updated_at', 'post', 'writer', 'content')

        return Response(data)


# Post Create
class PostCreateAPIView(CreateAPIView):
    def perform_create(self, serializer):
        serializer.save(writer=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    queryset = Post.objects.all()
    serializer_class = PostCreateSerializer



# Post Like
class PostLikeAPIView(APIView):
    permission_classes = [rest_framework.permissions.AllowAny]

    def get(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        serializer = PostLikeSerializer(post)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        user = request.user

        if user in post.like_users.all():
            # 이미 좋아요한 경우
            post.like_users.remove(user)
            post.save()
            return Response(post.like_users.all().count(), status=status.HTTP_200_OK)
        else:
            post.like_users.add(user)
            post.save()
            return Response(post.like_users.all().count(), status=status.HTTP_200_OK)

    queryset = Post.objects.all()
    serializer_class = PostLikeSerializer


# Post Bookmark
class PostBookmarkAPIView(APIView):
    def get(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        serializer = PostBookmarkSerializer(post)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        user = request.user

        if user in post.bookmark_users.all():
            # 이미 좋아요한 경우
            post.bookmark_users.remove(user)
            post.save()
            return Response(status=status.HTTP_200_OK)
        else:
            post.bookmark_users.add(user)
            post.save()
            return Response(status=status.HTTP_200_OK)

    queryset = Post.objects.all()
    serializer_class = PostBookmarkSerializer


# Post Comment List
class PostCommentListAPIView(ListCreateAPIView):

    def get(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        comments = post.comments.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def perform_create(self, serializer):
        serializer.save(writer=self.request.user)

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


# Pin List + Create
class PinListAPIView(ListCreateAPIView):
    queryset = Pin.objects.all()
    serializer_class = PinSerializer


# Pin Retrieve
class PinRetrieveAPIView(RetrieveAPIView):
    def get(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        pins = post.pins.all()
        serializer = PinSerializer(pins, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    queryset = Pin.objects.all()
    serializer_class = PinDetailSerializer


# Comment List
class CommentListAPIView(ListCreateAPIView):

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        post.comment_count += 1
        post.save()
        return Response(post.comment_count, status=status.HTTP_200_OK)

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


# Story List + Create
class StoryListAPIView(ListCreateAPIView):
    queryset = Story.objects.all()
    serializer_class = StorySerializer


# Story Retrieve + Destroy
class StoryRetrieveAPIView(RetrieveDestroyAPIView):
    queryset = Story.objects.all()
    serializer_class = StorySerializer


# Hashtag List + Create
class HashtagListAPIView(ListCreateAPIView):
    queryset = Hashtag.objects.all()
    serializer_class = HashtagSerializer


# Hashtag Retrieve + Destroy
class HashtagRetrieveAPIView(RetrieveDestroyAPIView):
    queryset = Hashtag.objects.all()
    serializer_class = HashtagSerializer


# Post Retrieve + Update + Destroy
class PostRetrieveAPIView(RetrieveUpdateDestroyAPIView):
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        pin = instance.pins.all()
        user = instance.writer
        comment = instance.comments.all()
        data = {
            'post': instance,
            'pin': pin,
            'user': user,
            'comment': comment,
        }
        serializer = self.get_serializer(instance=data)
        return Response(serializer.data)

    queryset = Post.objects.all()
    serializer_class = PostRetrieveSerializer
