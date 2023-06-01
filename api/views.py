from rest_framework import status
from rest_framework.views import APIView

from account.models import User
# from rest_framework import viewsets
# from .serializers import UserSerializer, PostSerializer
from rest_framework.generics import CreateAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView, UpdateAPIView, \
    GenericAPIView, get_object_or_404
from rest_framework.response import Response
from .serializers import PostSerializer, PostLikeSerializer, PinSerializer, CommentSerializer, StorySerializer, \
    HashtagSerializer
from socialmedia.models import Post, Pin, Comment, Story, Hashtag


# class UserViewSet(viewsets.ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#
# class PostViewSet(viewsets.ModelViewSet):
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer

class PostListAPIView(ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class PostRetrieveAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

# class PostLikeAPIView(UpdateAPIView):
#     queryset = Post.objects.all()
#     serializer_class = PostLikeSerializer
#
#     # PATCH method
#     def update(self, request, *args, **kwargs):
#         partial = kwargs.pop('partial', False)
#         instance = self.get_object()
#         changed_data = {
#             'like': instance.like + 1,
#             'liked_users': request.user,
#         }
#         serializer = self.get_serializer(instance, data=changed_data, partial=partial)
#         serializer.is_valid(raise_exception=True)
#         self.perform_update(serializer)
#
#         if getattr(instance, '_prefetched_objects_cache', None):
#             # If 'prefetch_related' has been applied to a queryset, we need to
#             # forcibly invalidate the prefetch cache on the instance.
#             instance._prefetched_objects_cache = {}
#
#         return Response(serializer.data)
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
            post.like -= 1
            post.save()
            return Response('unlike', status=status.HTTP_200_OK)
        else:
            # 좋아요 추가
            post.like_users.add(user)
            post.like += 1
            post.save()
            return Response('like', status=status.HTTP_200_OK)

    queryset = Post.objects.all()
    serializer_class = PostLikeSerializer

    # # GET method
    # def get(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     instance.like += 1
    #     instance.like_users.append(request.user)
    #
    #     return Response(instance.like, instance.like_users)


class PinListAPIView(ListCreateAPIView):
    queryset = Pin.objects.all()
    serializer_class = PinSerializer

class PinRetrieveAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Pin.objects.all()
    serializer_class = PinSerializer


class CommentCreateAPIView(ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class StoryListAPIView(ListCreateAPIView):
    queryset = Story.objects.all()
    serializer_class = StorySerializer

class StoryRetrieveAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Story.objects.all()
    serializer_class = StorySerializer


class HashtagListAPIView(ListCreateAPIView):
    queryset = Hashtag.objects.all()
    serializer_class = HashtagSerializer

class HashtagRetrieveAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Hashtag.objects.all()
    serializer_class = HashtagSerializer

