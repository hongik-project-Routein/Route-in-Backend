from django.urls import path, include
from rest_framework import routers
# from .views import UserViewSet, PostViewSet
from api import views

#
# router = routers.DefaultRouter()
# router.register(r'user', UserViewSet)
# router.register(r'post', PostViewSet)

app_name = 'api'
urlpatterns = [
    # path('', include(router.urls)),

    path('post/', views.PostListAPIView.as_view(), name='post-list'),
    path('post/<int:pk>/', views.PostRetrieveAPIView.as_view(), name='post-detail'),
    path('post/<int:pk>/like', views.PostLikeAPIView.as_view(), name='post-like'),

    path('pin/', views.PinListAPIView.as_view(), name='pin-list'),
    path('pin/<int:pk>/', views.PinRetrieveAPIView.as_view(), name='pin-detail'),

    path('comment/', views.CommentCreateAPIView.as_view(), name='comment-list'),

    path('story/', views.StoryListAPIView.as_view(), name='story-list'),
    path('story/<int:pk>/', views.StoryRetrieveAPIView.as_view(), name='story-detail'),

    path('hashtag/', views.HashtagListAPIView.as_view(), name='hashtag-list'),
    path('hashtag/<int:pk>/', views.HashtagRetrieveAPIView.as_view(), name='hashtag-detail'),
]