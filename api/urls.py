from django.urls import path
from api import views

app_name = 'api'
urlpatterns = [
    path('user/', views.UserListAPIView.as_view(), name='user-list'),
    path('user/<int:pk>/', views.UserRetrieveAPIView.as_view(), name='user-retrieve'),

    # 전체 게시글 목록: 구현 중
    path('post/', views.PostListAPIView.as_view(), name='post-list'),
    # 새로운 게시글 생성(POST): 구현
    path('post/create/', views.PostCreateAPIView.as_view(), name='post-create'),
    # 특정 게시글 상세(GET, PUT, DELETE): 구현
    path('post/<int:pk>/', views.PostRetrieveAPIView.as_view(), name='post-retrieve'),
    # 특정 게시글 좋아요(POST, GET): 구현
    path('post/<int:pk>/like/', views.PostLikeAPIView.as_view(), name='post-like'),
    # 특정 게시글 북마크(POST, GET): 구현
    path('post/<int:pk>/bookmark/', views.PostBookmarkAPIView.as_view(), name='post-bookmark'),
    # 특정 게시글 댓글 목록(GET) 및 새로운 댓글 생성(POST): 구현
    path('post/<int:pk>/comment/', views.PostCommentListAPIView.as_view(), name='post-comment'),

    # 전체 핀 목록: 미구현
    path('pin/', views.PinListAPIView.as_view(), name='pin-list'),
    # 특정 핀 상세: 미구현
    path('pin/<int:pk>/', views.PinRetrieveAPIView.as_view(), name='pin-retrieve'),

    # 전체 댓글 목록(GET) 및 새로운 댓글 생성(POST): 구현
    path('comment/', views.CommentListAPIView.as_view(), name='comment-list'),
    # 특정 댓글 상세(GET, PUT, DELETE): 구현 중
    path('comment/<int:pk>/', views.CommentRetrieveAPIView.as_view(), name='comment-retrieve'),
    # 특정 댓글 좋아요: 구현 중
    #path('comment/<int:pk>/like', views.CommentLikeAPIView.as_view(), name='comment-like'),

    path('hashtag/', views.HashtagListAPIView.as_view(), name='hashtag-list'),
    path('hashtag/<int:pk>/', views.HashtagRetrieveAPIView.as_view(), name='hashtag-retrieve'),
]