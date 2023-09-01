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
    try:  # 기존에 가입된 유저의 Provider가 google이 아니면 에러 발생, 맞으면 로그인
        user = User.objects.get(email=email)


        # 다른 SNS로 가입된 유저
        social_user = SocialAccount.objects.get(user=user)
        if social_user is None:
            return JsonResponse({'err_msg': 'email exists but not social user'},
                                status=status.HTTP_400_BAD_REQUEST)
        if social_user.provider != 'google':
            return JsonResponse({'err_msg': 'no matching social type'},
                                status=status.HTTP_400_BAD_REQUEST)


        data = {'access_token': access_token}
        accept = requests.post(
            f"{BASE_URL}accounts/google/login/finish/", data=data)
        accept_status = accept.status_code
        if accept_status != 200:
            return JsonResponse({'err_msg': 'failed to signin'}, status=accept_status)
        accept_json = accept.json()

    except:  # 기존에 가입된 유저가 없으면 새로 가입
        data = {'access_token': access_token}
        accept = requests.post(
            f"{BASE_URL}accounts/google/login/finish/", data=data)
        accept_status = accept.status_code
        if accept_status != 200:
            return JsonResponse({'err_msg': 'failed to signup'}, status=accept_status)
        accept_json = accept.json()

    user = User.objects.get(email=email)
    accept_json['name'] = user.name
    accept_json['uname'] = user.uname
    # 이미지 경로를 절대 URL로 생성
    image_url = None
    if user.image:
        image_url = request.build_absolute_uri(user.image.url)
    else:
        image_url = None
    accept_json['image'] = image_url
    accept_json['email'] = user.email
    accept_json['age'] = user.age
    accept_json['gender'] = user.gender
    accept_json['follower_set'] = list(user.follower_set.values_list('uname', flat=True))
    accept_json['following_set'] = list(user.following_set.values_list('uname', flat=True))

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
    email = kakao_account.get('email', None)

    if email is None:
        return JsonResponse({'err_msg': 'failed to get email'}, status=status.HTTP_400_BAD_REQUEST)

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

        # 기존에 Kakao로 가입된 유저
        data = {'access_token': access_token}
        accept = requests.post(
            f"{BASE_URL}accounts/kakao/login/finish/", data=data)
        accept_status = accept.status_code
        if accept_status != 200:
            return JsonResponse({'err_msg': 'failed to signin'}, status=accept_status)
        accept_json = accept.json()

    except User.DoesNotExist:
        # 기존에 가입된 유저가 없으면 새로 가입
        data = {'access_token': access_token}
        accept = requests.post(
            f"{BASE_URL}accounts/kakao/login/finish/", data=data)
        accept_status = accept.status_code
        if accept_status != 200:
            return JsonResponse({'err_msg': 'failed to signup'}, status=accept_status)
        accept_json = accept.json()

    user = User.objects.get(email=email)
    accept_json['name'] = user.name
    accept_json['uname'] = user.uname
    # 이미지 경로를 절대 URL로 생성
    image_url = None
    if user.image:
        image_url = request.build_absolute_uri(user.image.url)
    else:
        image_url = None
    accept_json['image'] = image_url
    accept_json['email'] = user.email
    accept_json['age'] = user.age
    accept_json['gender'] = user.gender
    accept_json['follower_set'] = list(user.follower_set.values_list('uname', flat=True))
    accept_json['following_set'] = list(user.following_set.values_list('uname', flat=True))

    accept_json.pop('user', None)

    return JsonResponse(accept_json)


class KakaoLogin(SocialLoginView):
    adapter_class = kakao_view.KakaoOAuth2Adapter
    client_class = OAuth2Client
    callback_url = KAKAO_CALLBACK_URI