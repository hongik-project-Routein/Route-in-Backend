from django.urls import path, include
# from .views import UserViewSet, PostViewSet
from api import views

app_name = 'api'
urlpatterns = [
    path('user/', views.UserListAPIView.as_view(), name='user-list'),
    path('user/<int:pk>/', views.UserRetrieveAPIView.as_view(), name='user-retrieve'),

    path('post/', views.PostListAPIView.as_view(), name='post-list'),
    path('post/<int:pk>/', views.PostRetrieveAPIView.as_view(), name='post-retrieve'),
    path('post/<int:pk>/like', views.PostLikeAPIView.as_view(), name='post-like'),
    path('post/<int:pk>/bookmark', views.PostBookmarkAPIView.as_view(), name='post-bookmark'),
    path('post/<int:pk>/comment', views.PostCommentListAPIView.as_view(), name='post-comment'),

    path('pin/', views.PinListAPIView.as_view(), name='pin-list'),
    path('pin/<int:pk>/', views.PinRetrieveAPIView.as_view(), name='pin-retrieve'),

    path('comment/', views.CommentListAPIView.as_view(), name='comment-list'),
    path('comment/<int:pk>/', views.PostCommentListAPIView.as_view(), name='post-comment'),


    path('story/', views.StoryListAPIView.as_view(), name='story-list'),
    path('story/<int:pk>/', views.StoryRetrieveAPIView.as_view(), name='story-retrieve'),

    path('hashtag/', views.HashtagListAPIView.as_view(), name='hashtag-list'),
    path('hashtag/<int:pk>/', views.HashtagRetrieveAPIView.as_view(), name='hashtag-retrieve'),
]