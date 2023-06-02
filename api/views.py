from rest_framework import status
from rest_framework.views import APIView
from account.models import User
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, get_object_or_404
from rest_framework.response import Response
from .serializers import PostSerializer, PostLikeSerializer, PinSerializer, CommentSerializer, StorySerializer, \
    HashtagSerializer, PostDetailSerializer, PostBookmarkSerializer
from socialmedia.models import Post, Pin, Comment, Story, Hashtag


# 포스트 목록 및 생성
class PostListAPIView(ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(writer=self.request.user)


# 포스트 상세 및 수정, 삭제
class PostRetrieveAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        comment_list = instance.comment_set.all()
        data = {
            'post': instance,
            'comment_list': comment_list,
        }
        serializer = self.get_serializer(instance=data)
        return Response(serializer.data)


# 포스트 좋아요
class PostLikeAPIView(APIView):
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
            post.like_count -= 1
            post.save()
            return Response(post.like_count, status=status.HTTP_200_OK)
        else:
            post.like_users.add(user)
            post.like_count += 1
            post.save()
            return Response(post.like_count, status=status.HTTP_200_OK)

    queryset = Post.objects.all()
    serializer_class = PostLikeSerializer


# 포스트 북마크
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

# 핀 목록 및 생성
class PinListAPIView(ListCreateAPIView):
    queryset = Pin.objects.all()
    serializer_class = PinSerializer


# 핀 상세 및 수정, 삭제
class PinRetrieveAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Pin.objects.all()
    serializer_class = PinSerializer


# 댓글 목록 및 생성
class CommentCreateAPIView(ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


# 스토리 목록 및 생성
class StoryListAPIView(ListCreateAPIView):
    queryset = Story.objects.all()
    serializer_class = StorySerializer


# 스토리 상세 및 수정, 삭제
class StoryRetrieveAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Story.objects.all()
    serializer_class = StorySerializer


# 해시태그 목록 및 생성
class HashtagListAPIView(ListCreateAPIView):
    queryset = Hashtag.objects.all()
    serializer_class = HashtagSerializer


# 해시태그 상세 및 수정, 삭제
class HashtagRetrieveAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Hashtag.objects.all()
    serializer_class = HashtagSerializer

