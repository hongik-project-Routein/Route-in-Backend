from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, get_object_or_404, ListAPIView, \
    RetrieveAPIView, RetrieveDestroyAPIView, CreateAPIView, GenericAPIView
from rest_framework.response import Response
from .serializers import *
from socialmedia.models import Post, Pin, Comment, Hashtag


# User List
class UserListAPIView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

'''
특정 유저 상세(GET): 구현
api/user/<str:uname>/
'''
class UserRetrieveAPIView(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'uname'

    def retrieve(self, request, *args, **kwargs):
        serializer = self.get_serializer(instance=self.get_object())
        return Response(serializer.data)

    def get_object(self):
        uname = self.kwargs['uname']
        return get_object_or_404(User, uname=uname)


'''
특정 사용자 팔로우(POST): 구현
api/user/<int:pk>/follow/
'''
class UserFollowAPIView(APIView):
    def post(self, request, uname):
        target_user = get_object_or_404(User, uname=uname)
        user = request.user

        # 자기 자신을 팔로우하는 경우
        if user == target_user:
            return Response('팔로우 실패: 자기 자신을 팔로우 할 수 없음', status.HTTP_200_OK)

        if user in target_user.follower_set.all():
            # 이미 팔로우한 경우
            target_user.follower_set.remove(user)
            target_user.save()
            return Response('팔로우 취소', status=status.HTTP_200_OK)
        else:
            target_user.follower_set.add(user)
            target_user.save()
            return Response('팔로우 성공', status=status.HTTP_200_OK)


    queryset = User.objects.all()
    serializer_class = UserFollowSerializer


'''
uname 중복확인(POST): 구현 중
api/user/uname_unique_check/<str:uname>/
'''
class UnameUniqueCheck(APIView):
    def post(self, request, uname):
        uname = uname
        if User.objects.filter(uname=uname).exists():
            return Response(f'{uname}: 사용 불가능한 uname', status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(f'{uname}: 사용 가능한 uname', status=status.HTTP_200_OK)


'''
전체 게시글 목록(GET): 구현 중
api/post/
'''
class PostListAPIView(ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostListSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        data = []
        for post in queryset:
            post_data = {}
            serializer = PostSerializer(post, context={'request': request})
            post_data['post'] = serializer.data
            post_data['pin'] = PinDetailSerializer(post.pins.all(), many=True, context={'request': request}).data
            post_data['user'] = UserImageSerializer(post.writer, context={'request': request}).data
            post_data['comment'] = CommentSerializer(post.comments.all(), many=True, context={'request': request}).data
            data.append(post_data)

        return Response(data)


'''
새로운 게시글 생성(POST)
api/post/create/
'''
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


'''
특정 게시글 상세(GET, PUT, DELETE)
api/post/<int:pk>/
'''
class PostRetrieveAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostRetrieveSerializer

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


'''
특정 게시글 좋아요(POST, GET)
api/post/<int:pk>/like/
'''
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
            post.save()
            return Response('좋아요 취소', status=status.HTTP_200_OK)
        else:
            post.like_users.add(user)
            post.save()
            return Response('좋아요 성공', status=status.HTTP_200_OK)

    queryset = Post.objects.all()
    serializer_class = PostLikeSerializer


'''
특정 게시글 북마크(POST, GET)
api/post/<int:pk>/bookmark/
'''
class PostBookmarkAPIView(APIView):
    def get(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        serializer = PostBookmarkSerializer(post)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        user = request.user

        if user in post.bookmark_users.all():
            # 이미 북마크한 경우
            post.bookmark_users.remove(user)
            post.save()
            return Response('북마크 취소', status=status.HTTP_200_OK)
        else:
            post.bookmark_users.add(user)
            post.save()
            return Response('북마크 성공', status=status.HTTP_200_OK)

    queryset = Post.objects.all()
    serializer_class = PostBookmarkSerializer


'''
특정 게시글 댓글 목록(GET) 및 새로운 댓글 생성(POST)
api/post/<int:pk>/comment/
'''
class PostCommentListAPIView(ListCreateAPIView):

    def get(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        comments = post.comments.all()
        serializer = CommentSerializer(comments, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def perform_create(self, serializer):
        serializer.save(writer=self.request.user)
        serializer.save(post=self.request.post)
        serializer.save(tagged_users=self.request.tagged_users)

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


'''
특정 게시글 태그된 사용자 목록(GET)
api/post/<int:pk>/tag/
'''
class PostTagListAPIView(APIView):
    def get(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        serializer = PostTagSerializer(post)
        return Response(serializer.data, status=status.HTTP_200_OK)

    queryset = Post.objects.all()
    serializer_class = PostTagSerializer


'''
특정 게시글 사용자 태그(POST)
api/post/<int:pk>/tag/<int:user_id>
'''
class PostTagAPIView(APIView):
    def post(self, request, pk, user_id):
        post = get_object_or_404(Post, pk=pk)
        try:
            user = User.objects.get(id=user_id)
        except:
            return Response('태그 실패: 해당 유저를 찾을 수 없음', status=status.HTTP_404_NOT_FOUND)

        if user in post.tagged_users.all():
            # 이미 태그한 경우
            post.tagged_users.remove(user)
            post.save()
            return Response(f'태그 취소 {user}', status=status.HTTP_200_OK)
        else:
            post.tagged_users.add(user)
            post.save()
            return Response(f'태그 성공: {user}', status=status.HTTP_200_OK)

    queryset = Post.objects.all()
    serializer_class = PostTagSerializer


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


'''
전체 댓글 목록(GET) 및 새로운 댓글 생성(POST)
api/comment/
'''
class CommentListAPIView(ListCreateAPIView):

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        post.comment_count += 1
        post.save()
        return Response(post.comment_count, status=status.HTTP_200_OK)

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


'''
특정 댓글 상세(GET, PUT, DELETE)
api/comment/<int:pk>/
'''
class CommentRetrieveAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


'''
특정 댓글 좋아요(POST, GET)
api/comment/<int:pk>/like/
'''
class CommentLikeAPIView(APIView):
    def get(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        serializer = CommentLikeSerializer(comment)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        user = request.user

        if user in comment.like_users.all():
            # 이미 좋아요한 경우
            comment.like_users.remove(user)
            comment.save()
            return Response('좋아요 취소', status=status.HTTP_200_OK)
        else:
            comment.like_users.add(user)
            comment.save()
            return Response('좋아요 성공', status=status.HTTP_200_OK)

    queryset = Comment.objects.all()
    serializer_class = CommentLikeSerializer


'''
특정 댓글 태그된 사용자 목록(GET)
api/comment/<int:pk>/tag/
'''
class CommentTagListAPIView(APIView):
    def get(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        serializer = CommentTagSerializer(comment)
        return Response(serializer.data, status=status.HTTP_200_OK)

    queryset = Comment.objects.all()
    serializer_class = CommentTagSerializer


'''
특정 댓글 사용자 태그(POST)
api/comment/<int:pk>/tag/<int:user_id>
'''
class CommentTagAPIView(APIView):
    def post(self, request, pk, user_id):
        comment = get_object_or_404(Comment, pk=pk)
        try:
            user = User.objects.get(id=user_id)
        except:
            return Response('태그 실패: 해당 유저를 찾을 수 없음', status=status.HTTP_404_NOT_FOUND)

        if user in comment.tagged_users.all():
            # 이미 태그한 경우
            comment.tagged_users.remove(user)
            comment.save()
            return Response(f'태그 취소 {user}', status=status.HTTP_200_OK)
        else:
            comment.tagged_users.add(user)
            comment.save()
            return Response(f'태그 성공: {user}', status=status.HTTP_200_OK)

    queryset = Comment.objects.all()
    serializer_class = CommentTagSerializer


# Hashtag List + Create
class HashtagListAPIView(ListCreateAPIView):
    queryset = Hashtag.objects.all()
    serializer_class = HashtagSerializer


# Hashtag Retrieve + Destroy
class HashtagRetrieveAPIView(RetrieveDestroyAPIView):
    queryset = Hashtag.objects.all()
    serializer_class = HashtagSerializer


'''
최초 가입 시 정보 입력(POST)
api/initial_setting/
'''
class InitialSettingAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = InitialSettingSerializer(data=request.data)

        if serializer.is_valid():
            user = request.user

            user.uname = serializer.validated_data.get('uname')
            user.name = serializer.validated_data.get('name')
            user.age = serializer.validated_data.get('age')
            user.gender = serializer.validated_data.get('gender')
            user.save()

            return Response("초기 설정 완료.", status=status.HTTP_200_OK)

        else:
            return Response("초기 설정 실패, 재시도 필요", status=status.HTTP_400_BAD_REQUEST)