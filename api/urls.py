from django.urls import path
from api import views

app_name = 'api'
urlpatterns = [
    # 자신의 프로필: 미구현
    # path('profile/', views.ProfileAPIView.as_view(), name='profile'),

    # 전체 유저 목록: 구현
    path('user/', views.UserListAPIView.as_view(), name='user-list'),
    # 최초 가입 시 정보 입력(POST): 구현
    path('user/initial_setting/', views.InitialSettingAPIView.as_view(), name='initial-setting'),
    # 특정 유저 상세: 구현
    path('user/<str:uname>/', views.UserRetrieveAPIView.as_view(), name='user-retrieve'),
    # 특정 사용자 팔로우(POST, GET): 구현
    path('user/<str:uname>/follow/', views.UserFollowAPIView.as_view(), name='user-follow'),
    # uname 중복 확인(POST): 구현
    path('user/uname_check/<str:uname>/', views.UnameUniqueCheck.as_view(), name='uname-unique-check'),


    # 전체 게시글 목록(GET): 구현
    path('post/', views.PostListAPIView.as_view(), name='post-list'),
    # 특정 게시글 상세(GET, PUT, DELETE): 구현 및 연결
    path('post/<int:pk>/', views.PostRetrieveAPIView.as_view(), name='post-retrieve'),
    # 특정 게시글 좋아요(POST, GET): 구현 및 연결
    path('post/<int:pk>/like/', views.PostLikeAPIView.as_view(), name='post-like'),
    # 특정 게시글 북마크(POST, GET): 구현
    path('post/<int:pk>/bookmark/', views.PostBookmarkAPIView.as_view(), name='post-bookmark'),
    # 특정 게시글 댓글 목록(GET) 및 새로운 댓글 생성(POST): 구현
    path('post/<int:pk>/comment/', views.PostCommentListAPIView.as_view(), name='post-comment'),
    # 특정 게시글 태그된 사용자 목록(GET): 구현
    path('post/<int:pk>/tag/', views.PostTagListAPIView.as_view(), name='post-tag-list'),
    # 특정 게시글 사용자 태그(POST): 구현
    path('post/<int:pk>/tag/<int:user_id>/', views.PostTagAPIView.as_view(), name='post-tag'),
    # 새로운 게시글 생성(POST): 구현 및 연결
    path('post/create/', views.PostCreateAPIView.as_view(), name='post-create'),
    # 특정 게시글 수정(PUT): 미구현
    path('post/update/', views.PostUpdateAPIView.as_view(), name='post-update'),

    # 전체 핀 목록: 미구현
    path('pin/', views.PinListAPIView.as_view(), name='pin-list'),
    # 특정 핀 상세: 미구현
    path('pin/<int:pk>/', views.PinRetrieveAPIView.as_view(), name='pin-retrieve'),

    # 전체 댓글 목록(GET) 및 새로운 댓글 생성(POST): 구현
    path('comment/', views.CommentListAPIView.as_view(), name='comment-list'),
    # 특정 댓글 상세(GET, PUT, DELETE): 구현
    path('comment/<int:pk>/', views.CommentRetrieveAPIView.as_view(), name='comment-retrieve'),
    # 특정 댓글 좋아요(POST, GET): 구현
    path('comment/<int:pk>/like/', views.CommentLikeAPIView.as_view(), name='comment-like'),
    # 특정 댓글 태그된 사용자 목록(GET): 구현 중
    path('comment/<int:pk>/tag/', views.CommentTagListAPIView.as_view(), name='comment-tag-list'),
    # 특정 댓글 사용자 태그(POST): 구현 중
    path('comment/<int:pk>/tag/<int:user_id>/', views.CommentTagAPIView.as_view(), name='comment-tag'),

    # 전체 해시태그 목록: 미구현
    path('hashtag/', views.HashtagListAPIView.as_view(), name='hashtag-list'),
    # 특정 해시태그 상세: 미구현
    path('hashtag/<int:pk>/', views.HashtagRetrieveAPIView.as_view(), name='hashtag-retrieve'),


]
