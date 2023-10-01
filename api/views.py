from rest_framework import status
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, get_object_or_404, ListAPIView, \
    RetrieveAPIView, RetrieveDestroyAPIView, CreateAPIView, UpdateAPIView, RetrieveUpdateAPIView
from rest_framework.response import Response
from .serializers import *
from socialmedia.models import Post, Pin, Comment, Hashtag
from sentiment_analysis.analysis import get_score
from sentiment_analysis.save_to_bq import save_sa
from sentiment_analysis.find_similar_user_pd import *
from recommend_system.recommend import get_place
from django.http import HttpResponse
from dj_rest_auth.registration.views import RegisterView
from dj_rest_auth.views import LoginView
from dj_rest_auth.app_settings import api_settings
from django.utils import timezone
from django.http import JsonResponse

# User List
class UserListAPIView(ListAPIView):
    queryset = User.objects.all().order_by('joined_at')
    serializer_class = UserSerializer
    pagination_class = PageNumberPagination
    filter_backends = [SearchFilter]
    search_fields = ['uname']


'''
특정 유저 상세(GET)
api/user/<str:uname>/
'''
class UserRetrieveAPIView(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all().order_by('joined_at')
    serializer_class = UserRetrieveSerializer
    lookup_field = 'uname'

    def retrieve(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(instance=user, context={'request': request})
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(instance=user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def get_object(self):
        uname = self.kwargs['uname']
        return get_object_or_404(User, uname=uname)


'''
특정 사용자 팔로우(POST)
api/user/<str:uname>/follow/
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
uname 중복확인(POST)
api/user/uname_unique_check/<str:uname>/
'''
class UnameUniqueCheck(APIView):
    def post(self, request, uname):
        uname = uname
        if User.objects.filter(uname=uname).exists():
            return Response(False, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(True, status=status.HTTP_200_OK)


'''
전체 게시글 목록(GET)
api/post/
'''
class PostListAPIView(ListAPIView):
    queryset = Post.objects.filter(is_deleted=False).order_by('-created_at')
    serializer_class = PostListSerializer
    pagination_class = PageNumberPagination
    filter_backends = [SearchFilter]
    search_fields = ['content']

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)

        data = []
        for post in page:
            post_data = {}
            serializer = PostSerializer(post, context={'request': request})
            post_data['post'] = serializer.data
            post_data['pin'] = PinDetailSerializer(post.pins.filter(is_deleted=False), many=True, context={'request': request}).data
            post_data['user'] = UserImageSerializer(post.writer, context={'request': request}).data
            post_data['comment'] = CommentSerializer(post.comments.filter(is_deleted=False), many=True,
                                                     context={'request': request}).data
            data.append(post_data)

        return self.get_paginated_response(data)


'''
새로운 게시글 생성(POST)
api/post/create/
'''
class PostCreateAPIView(CreateAPIView):
    def perform_create(self, serializer, user):
        writer = self.request.user
        serializer.save(writer=writer)

        # [[uname, mapID, score], ...] 2차원 리스트 sentiList
        sentiList = []
        for pin in serializer.data['pins']:
            uname = writer.uname
            mapID = pin['mapID']
            content = pin['content']
            # 본문 감정 분석
            score = get_score(content)
            sentiList.append([uname, mapID, score])

        # 장소에 대한 긍/부정 점수 저장
        save_sa(sentiList)

        # 유사한 사용자 찾기
        for sim_user in find_sim_users(user.uname, pi_pd_df):
            new_user = get_object_or_404(User, uname=sim_user)
            user.sim_users.add(new_user)
            user.save()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user
        self.perform_create(serializer, user)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


    queryset = Post.objects.filter(is_deleted=False)
    serializer_class = PostCreateSerializer


'''
특정 게시글 상세(GET, DELETE)
api/post/<int:pk>/
'''
class PostRetrieveAPIView(RetrieveDestroyAPIView):
    queryset = Post.objects.filter(is_deleted=False)
    serializer_class = PostRetrieveSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        pin = instance.pins.filter(is_deleted=False)
        user = instance.writer
        comment = instance.comments.filter(is_deleted=False)
        data = {
            'post': instance,
            'pin': pin,
            'user': user,
            'comment': comment,
        }
        serializer = self.get_serializer(instance=data)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_deleted = True
        instance.save()

        return Response('삭제 성공', status=status.HTTP_204_NO_CONTENT)


'''
특정 포스트 수정(PUT, GET)
api/post/<int:pk>/update/
'''
class PostUpdateAPIView(RetrieveUpdateAPIView):
    queryset = Post.objects.filter(is_deleted=False)
    serializer_class = PostUpdateSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        post_serializer = PostContentSerializer(instance, context={'request': request})
        pins_serializer = PinDetailSerializer(instance.pins.filter(is_deleted=False), many=True, context={'request': request})
        data = {
            **post_serializer.data,
            'pins': pins_serializer.data
        }
        return Response(data)


'''
특정 게시글 좋아요(POST, GET)
api/post/<int:pk>/like/
'''
class PostLikeAPIView(APIView):
    def get(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        likes = post.like_users.all().order_by('id')  # id 기준 정렬, 수정 가능

        paginator = PageNumberPagination()
        paginated_likes = paginator.paginate_queryset(likes, request)

        serializer = UserSerializer(paginated_likes, context={'request': request}, many=True)
        return paginator.get_paginated_response(serializer.data)

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

    queryset = Post.objects.filter(is_deleted=False)
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

    queryset = Post.objects.filter(is_deleted=False)
    serializer_class = PostBookmarkSerializer


'''
특정 게시글 댓글 목록(GET) 및 새로운 댓글 생성(POST)
api/post/<int:pk>/comment/
'''
class PostCommentListAPIView(ListCreateAPIView):
    queryset = Comment.objects.filter(is_deleted=False)
    serializer_class = CommentSerializer
    pagination_class = PageNumberPagination

    def get(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        comments = post.comments.filter(is_deleted=False).order_by('-created_at')
        page = self.paginate_queryset(comments)

        serializer = CommentSerializer(page, many=True, context={'request': request})
        return self.get_paginated_response(serializer.data)

    def perform_create(self, serializer):
        post = get_object_or_404(Post, pk=self.kwargs['pk'])
        serializer.save(writer=self.request.user, post=post)


'''
특정 게시글 태그된 사용자 목록(GET)
api/post/<int:pk>/tag/
'''
class PostTagListAPIView(APIView):
    def get(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        serializer = PostTagSerializer(post)
        return Response(serializer.data, status=status.HTTP_200_OK)

    queryset = Post.objects.filter(is_deleted=False)
    serializer_class = PostTagSerializer


'''
특정 게시글 사용자 태그(POST)
api/post/<int:pk>/tag/<str:uname>
'''
class PostTagAPIView(APIView):
    def post(self, request, pk, uname):
        post = get_object_or_404(Post, pk=pk)
        try:
            user = User.objects.get(uname=uname)
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

    queryset = Post.objects.filter(is_deleted=False)
    serializer_class = PostTagSerializer


# Pin List + Create
class PinListAPIView(ListCreateAPIView):
    queryset = Pin.objects.filter(is_deleted=False)
    # serializer_class = PinSerializer
    serializer_class = PinSearchSerializer
    pagination_class = PageNumberPagination
    filter_backends = [SearchFilter]
    search_fields = ['pin_hashtag']


# Pin Retrieve
class PinRetrieveAPIView(RetrieveDestroyAPIView):
    def get(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        pins = post.pins.filter(is_deleted=False)
        serializer = PinSerializer(pins, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        pin = self.get_object()
        pin.delete()
        return Response("삭제 성공", status=status.HTTP_204_NO_CONTENT)

    queryset = Pin.objects.filter(is_deleted=False)
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

    queryset = Comment.objects.filter(is_deleted=False)
    serializer_class = CommentSerializer


'''
특정 댓글 상세 (GET, PUT, DELETE)
api/comment/<int:pk>/
'''
class CommentRetrieveAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.filter(is_deleted=False)
    serializer_class = CommentSerializer


'''
특정 댓글 좋아요 (POST, GET)
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
            return Response('좋아요 취소', status=status.HTTP_200_OK)
        else:
            comment.like_users.add(user)
            return Response('좋아요 성공', status=status.HTTP_200_OK)

    queryset = Comment.objects.filter(is_deleted=False)
    serializer_class = CommentLikeSerializer


'''
특정 댓글 태그된 사용자 목록 (GET)
api/comment/<int:pk>/tag/
'''
class CommentTagListAPIView(APIView):
    def get(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        serializer = CommentTagSerializer(comment)
        return Response(serializer.data, status=status.HTTP_200_OK)

    queryset = Comment.objects.filter(is_deleted=False)
    serializer_class = CommentTagSerializer


'''
특정 댓글 사용자 태그 (POST)
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

    queryset = Comment.objects.filter(is_deleted=False)
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
최초 가입 시 정보 입력 (POST)
api/user/initial_setting/
'''
class InitialSettingAPIView(APIView):
    def post(self, request):
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


'''
특정 사용자 북마크한 게시글 목록 (GET)
api/user/<str:uname>/bookmark/
'''
class UserBookmarkListAPIView(PostListAPIView):
    def get_queryset(self):
        uname = self.kwargs['uname']
        user = User.objects.get(uname=uname)
        bookmarked_posts = user.bookmark_posts.filter(is_deleted=False)

        return bookmarked_posts

    serializer_class = UserSerializer


'''
게시글 추천 (GET)
api/recommend/post/
'''
class PostRecommendListAPIView(ListAPIView):
    def get_queryset(self):
        # user = self.request.user
        user = get_object_or_404(User, uname='kshkakao')
        print('target_user: ', user)
        queryset = Post.objects.none()
        sim_users = [sim_user.uname for sim_user in user.sim_users.all()]
        print('sim_users: ', sim_users)
        getp = get_place(sim_users, user)
        print('get_place: ', getp)
        if sim_users:
            for userID, mapID in getp:
                target_user = User.objects.get(uname=userID)
                user_posts = target_user.writed_posts.filter(is_deleted=False)
                post = user_posts.filter(pins__mapID=mapID)
                queryset = queryset.union(post)
        else:
            print("There is no one in sim_users.")

        return queryset

    serializer_class = PostListSerializer


'''
유사한 유저 추천 (GET)
api/recommend/user/
'''
class UserRecommendListAPIView(ListAPIView):
    def get_queryset(self):
        # user = self.request.user
        user = get_object_or_404(User, uname='kshkakao')
        recom_users = find_sim_users(user.uname, pi_pd_df)
        queryset = User.objects.filter(uname__in=recom_users)

        return queryset

    serializer_class = UserSerializer


'''
일반 사용자 가입
api/accounts/registration/
'''
class CustomRegisterView(RegisterView):
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        if response.status_code == status.HTTP_201_CREATED:
            return Response('회원가입 성공', status=status.HTTP_201_CREATED)
        else:
            return Response('회원가입 실패', status=status.HTTP_400_BAD_REQUEST)

'''
일반 사용자 로그인
api/accounts/login/
'''
class CustomLoginView(LoginView):
    def custom_response(self, user):
        response_data = {
            'name': user.name,
            'uname': user.uname,
            'email': user.email,
            'age': user.age,
            'gender': user.gender,
            'follower_set': list(user.follower_set.values_list('uname', flat=True)),
            'following_set': list(user.following_set.values_list('uname', flat=True)),
        }

        # 이미지 경로를 절대 URL로 생성
        image_url = self.request.build_absolute_uri(user.image.url) if user.image else None
        response_data['image'] = image_url
        return response_data

    def post(self, request, *args, **kwargs):
        self.request = request
        self.serializer = self.get_serializer(data=self.request.data)
        self.serializer.is_valid(raise_exception=True)

        self.login()

        if self.user:
            response_data = self.custom_response(self.user)

            if hasattr(self, 'access_token'):
                response_data['access'] = str(self.access_token)
            print(response_data)
            return Response(response_data, status=status.HTTP_200_OK)

        # return self.get_response()