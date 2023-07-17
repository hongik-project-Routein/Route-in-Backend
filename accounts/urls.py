from django.urls import path, include
from . import views

app_name = 'accounts'
urlpatterns = [
    ## 팔로우 및 언팔로우
    # path('follow/<int:pk>', views.user_follow, name='user_follow'),
    # path('unfollow/<int:pk>', views.user_unfollow(), name='user_follow'),

    path('google/login/', views.google_login, name='google_login'),
    path('google/callback/', views.google_callback, name='google_callback'),
    path('google/login/finish/', views.GoogleLogin.as_view(), name='google_login_todjango'),


]