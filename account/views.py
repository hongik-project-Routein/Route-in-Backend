# # from django.contrib.auth.decorators import login_required
# from django.contrib.auth.models import User
# from django.shortcuts import get_object_or_404, redirect
#
#
# # @login_required
# def user_follow(request, id):
#     follow_user = get_object_or_404(User, id=id, is_active=True)
#
#     # request를 following, 유저는 request의 follower
#     request.user.following_set.add(follow_user)
#     follow_user.follower_set.add(request.user)
#
#     redirect_url = request.META.get('HTTP_REFERER', 'root')
#     return redirect(redirect_url)
#
#
# # @login_required
# def user_unfollow(request, id):
#     unfollow_user = get_object_or_404(User, id=id, is_active=True)
#
#     # request를 following, 유저는 request의 follower
#     request.user.following_set.remove(unfollow_user)
#     unfollow_user.follower_set.remove(request.user)
#
#     redirect_url = request.META.get('HTTP_REFERER', 'root')
#     return redirect(redirect_url)
