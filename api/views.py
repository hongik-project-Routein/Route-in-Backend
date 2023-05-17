from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView

from api.serializers import PostListSerializer, PostRetrieveSerializer, CommentSerializer
from socialmedia.models import Post, Comment


class PostListAPIView(ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostListSerializer

class PostRetrieveAPIView(RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostRetrieveSerializer

class CommentCreateAPIView(CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

