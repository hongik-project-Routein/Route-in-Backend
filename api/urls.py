from django.urls import path
from api import views

app_name = 'api'
urlpatterns = [
    # 전체 유저 목록
    path('user/', views.UserListAPIView.as_view(), name='user-list'),
    # 최초 가입 시 정보 입력(POST)
    path('user/initial_setting/', views.InitialSettingAPIView.as_view(), name='initial-setting'),
    # uname 중복 확인(POST)
    path('user/uname_check/<str:uname>/', views.UnameUniqueCheck.as_view(), name='uname-unique-check'),
    # 특정 유저 상세(GET)
    path('user/<str:uname>/', views.UserRetrieveAPIView.as_view(), name='user-retrieve'),
    # 특정 유저 게시글 목록(GET)
    path('user/<str:uname>/post/', views.UserPostListAPIView.as_view(), name='user-post-list'),
    # 특정 유저 팔로우(POST)
    path('user/<str:uname>/follow/', views.UserFollowAPIView.as_view(), name='user-follow'),
    # 특정 유저 북마크 게시글 목록(GET)
    path('user/<str:uname>/bookmark/', views.UserBookmarkListAPIView.as_view(), name='user-bookmark'),

    # 전체 게시글 목록(GET)
    path('post/', views.PostListAPIView.as_view(), name='post-list'),
    # 특정 게시글 상세(GET, PUT, DELETE)
    path('post/<int:pk>/', views.PostRetrieveAPIView.as_view(), name='post-retrieve'),
    # 특정 게시글 좋아요(POST, GET)
    path('post/<int:pk>/like/', views.PostLikeAPIView.as_view(), name='post-like'),
    # 특정 게시글 북마크(POST, GET)
    path('post/<int:pk>/bookmark/', views.PostBookmarkAPIView.as_view(), name='post-bookmark'),
    # 특정 게시글 댓글 목록(GET) 및 새로운 댓글 생성(POST)
    path('post/<int:pk>/comment/', views.PostCommentListAPIView.as_view(), name='post-comment'),
    # 특정 게시글 태그된 사용자 목록(GET)
    path('post/<int:pk>/tag/', views.PostTagListAPIView.as_view(), name='post-tag-list'),
    # 특정 게시글 사용자 태그(POST)
    path('post/<int:pk>/tag/<str:uname>/', views.PostTagAPIView.as_view(), name='post-tag'),
    # 새로운 게시글 생성(POST)
    path('post/create/', views.PostCreateAPIView.as_view(), name='post-create'),
    # 특정 게시글 수정(PUT)
    path('post/<int:pk>/update/', views.PostUpdateAPIView.as_view(), name='post-update'),

    # 전체 핀 목록
    path('pin/', views.PinListAPIView.as_view(), name='pin-list'),
    # 특정 핀 상세 및 삭제
    path('pin/<int:pk>/', views.PinRetrieveAPIView.as_view(), name='pin-retrieve'),

    # 전체 댓글 목록(GET) 및 새로운 댓글 생성(POST)
    path('comment/', views.CommentListAPIView.as_view(), name='comment-list'),
    # 특정 댓글 상세(GET, PUT, DELETE)
    path('comment/<int:pk>/', views.CommentRetrieveAPIView.as_view(), name='comment-retrieve'),
    # 특정 댓글 좋아요(POST, GET)
    path('comment/<int:pk>/like/', views.CommentLikeAPIView.as_view(), name='comment-like'),
    # 특정 댓글 태그된 사용자 목록(GET)
    path('comment/<int:pk>/tag/', views.CommentTagListAPIView.as_view(), name='comment-tag-list'),
    # 특정 댓글 사용자 태그(POST)
    path('comment/<int:pk>/tag/<int:user_id>/', views.CommentTagAPIView.as_view(), name='comment-tag'),

    # 전체 해시태그 목록
    path('hashtag/', views.HashtagListAPIView.as_view(), name='hashtag-list'),
    # 특정 해시태그 상세
    path('hashtag/<int:pk>/', views.HashtagRetrieveAPIView.as_view(), name='hashtag-retrieve'),

    # 게시글 추천(GET)
    path('recommend/post/', views.PostRecommendListAPIView.as_view(), name='post-recommend'),
    # 유사한 유저 추천(GET)
    path('recommend/user/', views.UserRecommendListAPIView.as_view(), name='user-recommend'),
]
