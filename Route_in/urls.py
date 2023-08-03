from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from Route_in import settings


urlpatterns = [
    path('admin/', admin.site.urls),

    path('accounts/', include('accounts.urls')),
    path('accounts/', include('dj_rest_auth.urls')),
    path('accounts/', include('dj_rest_auth.registration.urls')),
    path('accounts/', include('allauth.urls')),

    path('api/', include('api.urls')),
    path('socialmedia/', include('socialmedia.urls')), # no use
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)