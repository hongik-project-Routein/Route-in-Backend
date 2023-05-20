from django.urls import path
from . import views

app_name = 'api'
urlpatterns = [
    path('post/', views.PostListAPIView.as_view(), name='post-list'),
    path('post/<int:pk>/', views.PostRetrieveAPIView.as_view(), name='post-detail'),

    path('pin/', views.PinListAPIView.as_view(), name='pin-list'),
    path('pin/<int:pk>/', views.PinRetrieveAPIView.as_view(), name='pin-detail'),

    path('comment/', views.CommentCreateAPIView.as_view(), name='comment-list'),

    path('story/', views.StoryListAPIView.as_view(), name='story-list'),
    path('story/<int:pk>/', views.StoryRetrieveAPIView.as_view(), name='story-detail'),
]