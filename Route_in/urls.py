from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from Route_in import settings
from api.views import CustomRegisterView, CustomLoginView


urlpatterns = [
    path('admin/', admin.site.urls),

    path('accounts/', include('accounts.urls')),
    path('accounts/', include('allauth.urls')),
    path('api/accounts/login/', CustomLoginView.as_view(), name='custom-login'),
    path('api/accounts/registration/', CustomRegisterView.as_view(), name='custom-reigster'),
    path('api/accounts/', include('dj_rest_auth.urls')),

    path('api/', include('api.urls')),
    path('socialmedia/', include('socialmedia.urls')), # no use
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)