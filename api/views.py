from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView

from api.serializers import PostListSerializer, PostRetrieveSerializer, PinListSerializer, PinRetrieveSerializer, CommentSerializer, StoryListSerializer, StoryRetrieveSerializer
from socialmedia.models import Post, Pin, Comment, Story


class PostListAPIView(ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostListSerializer
class PostRetrieveAPIView(RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostRetrieveSerializer

class PinListAPIView(ListAPIView):
    queryset = Pin.objects.all()
    serializer_class = PinListSerializer
class PinRetrieveAPIView(RetrieveAPIView):
    queryset = Pin.objects.all()
    serializer_class = PinRetrieveSerializer

class CommentCreateAPIView(CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

class StoryListAPIView(ListAPIView):
    queryset = Story.objects.all()
    serializer_class = StoryListSerializer
class StoryRetrieveAPIView(RetrieveAPIView):
    queryset = Story.objects.all()
    serializer_class = StoryRetrieveSerializer