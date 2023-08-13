from accounts.models import User
from allauth.socialaccount.models import SocialAccount
from django.conf import settings
from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.google import views as google_view
from allauth.socialaccount.providers.kakao import views as kakao_view
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from django.http import JsonResponse
import requests
from rest_framework import status
from json.decoder import JSONDecodeError


state = getattr(settings, 'STATE')
BASE_URL = 'http://localhost:8000/'
GOOGLE_CALLBACK_URI = BASE_URL + 'accounts/google/callback/'


def google_callback(request):
    """
    Get Access Token From Frontend
    """
    # 'Bearer: ' 슬라이싱
    access_token = request.headers.get('Authorization')[7:]

    """
    Email Request
    """
    email_req = requests.get(
        f"https://www.googleapis.com/oauth2/v1/tokeninfo?access_token={access_token}")
    email_req_status = email_req.status_code
    if email_req_status != 200:
        return JsonResponse({'err_msg': 'failed to get email'}, status=status.HTTP_400_BAD_REQUEST)
    email_req_json = email_req.json()
    email = email_req_json.get('email')

    """
    Signup or Signin Request
    """
    try: # 기존에 가입된 유저의 Provider가 google이 아니면 에러 발생, 맞으면 로그인
        user = User.objects.get(email=email)
        # # 다른 SNS로 가입된 유저
        # social_user = SocialAccount.objects.get(user=user)
        # if social_user is None:
        #     return JsonResponse({'err_msg': 'email exists but not social user'},
        #                         status=status.HTTP_400_BAD_REQUEST)
        # if social_user.provider != 'google':
        #     return JsonResponse({'err_msg': 'no matching social type'},
        #                         status=status.HTTP_400_BAD_REQUEST)

        # 기존에 Google로 가입된 유저
        data = {'access_token': access_token}
        accept = requests.post(
            f"{BASE_URL}accounts/google/login/finish/", data=data)
        accept_status = accept.status_code
        if accept_status != 200:
            return JsonResponse({'err_msg': 'failed to signin'}, status=accept_status)
        accept_json = accept.json()

        # name, uname, image, email, age, gender, follower_set, following_set 포함
        user = User.objects.get(email=email)

        user_info = {
            'name': user.name,
            'uname': user.uname,
            'image': user.image if user.image else None,
            'email': user.email,
            'age': user.age,
            'gender': user.gender,
            'follower_set': user.follower_set,
            'following_set': user.following_set,
        }
        accept_json['user_info'] = user_info
        accept_json.pop('user', None)

        return JsonResponse(accept_json)

    except:  # 기존에 가입된 유저가 없으면 새로 가입
        data = {'access_token': access_token}
        accept = requests.post(
            f"{BASE_URL}accounts/google/login/finish/", data=data)

        accept_status = accept.status_code
        if accept_status != 200:
            return JsonResponse({'err_msg': 'failed to signup'}, status=accept_status)
        accept_json = accept.json()

        # name, uname, image, email, age, gender, follower_set, following_set 포함
        user = User.objects.get(email=email)

        user_info = {
            'name': user.name,
            'uname': user.uname,
            'image': user.image if user.image else None,
            'email': user.email,
            'age': user.age,
            'gender': user.gender,
            'follower_set': user.follower_set,
            'following_set': user.following_set,
        }
        accept_json['user_info'] = user_info
        accept_json.pop('user', None)

        return JsonResponse(accept_json)


class GoogleLogin(SocialLoginView):
    adapter_class = google_view.GoogleOAuth2Adapter
    callback_url = GOOGLE_CALLBACK_URI
    client_class = OAuth2Client


KAKAO_CALLBACK_URI = getattr(settings, 'KAKAO_REDIRECT_URI')


def kakao_callback(request):
    """
       Get Access Token From Frontend
    """
    access_token = request.headers.get('Authorization')[7:]

    """
    Email Request
    """
    profile_request = requests.get(
        "https://kapi.kakao.com/v2/user/me", headers={"Authorization": f"Bearer {access_token}"})
    profile_json = profile_request.json()
    kakao_account = profile_json.get('kakao_account')
    """
    kakao_account에서 이메일 외에 카카오톡 프로필 이미지, 배경 이미지 url 가져올 수 있음
    """
    email = kakao_account.get('email')

    """
    Signup or Signin Request
    """
    try:
        user = User.objects.get(email=email)
        # 기존에 가입된 유저의 Provider가 kakao가 아니면 에러 발생, 맞으면 로그인
        # 다른 SNS로 가입된 유저
        social_user = SocialAccount.objects.get(user=user)
        if social_user is None:
            return JsonResponse({'err_msg': 'email exists but not social user'}, status=status.HTTP_400_BAD_REQUEST)
        if social_user.provider != 'kakao':
            return JsonResponse({'err_msg': 'no matching social type'}, status=status.HTTP_400_BAD_REQUEST)
        # 기존에 Google로 가입된 유저
        data = {'access_token': access_token}
        accept = requests.post(
            f"{BASE_URL}accounts/kakao/login/finish/", data=data)
        accept_status = accept.status_code
        if accept_status != 200:
            return JsonResponse({'err_msg': 'failed to signin'}, status=accept_status)
        accept_json = accept.json()

        # name, uname, image, email, age, gender, follower_set, following_set 포함
        user = User.objects.get(email=email)

        user_info = {
            'name': user.name,
            'uname': user.uname,
            'image': user.image if user.image else None,
            'email': user.email,
            'age': user.age,
            'gender': user.gender,
            'follower_set': user.follower_set,
            'following_set': user.following_set,
        }
        accept_json['user_info'] = user_info
        accept_json.pop('user', None)

        return JsonResponse(accept_json)

    except User.DoesNotExist:
        # 기존에 가입된 유저가 없으면 새로 가입
        data = {'access_token': access_token}
        accept = requests.post(
            f"{BASE_URL}accounts/kakao/login/finish/", data=data)
        accept_status = accept.status_code
        if accept_status != 200:
            return JsonResponse({'err_msg': 'failed to signup'}, status=accept_status)
        # user의 pk, email, first name, last name과 Access Token, Refresh token 가져옴
        accept_json = accept.json()

        # name, uname, image, email, age, gender, follower_set, following_set 포함
        user = User.objects.get(email=email)

        user_info = {
            'name': user.name,
            'uname': user.uname,
            'image': user.image if user.image else None,
            'email': user.email,
            'age': user.age,
            'gender': user.gender,
            'follower_set': user.follower_set,
            'following_set': user.following_set,
        }
        accept_json['user_info'] = user_info
        accept_json.pop('user', None)

        return JsonResponse(accept_json)


class KakaoLogin(SocialLoginView):
    adapter_class = kakao_view.KakaoOAuth2Adapter
    client_class = OAuth2Client
    callback_url = KAKAO_CALLBACK_URI