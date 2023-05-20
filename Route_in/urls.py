from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from Route_in import settings


urlpatterns = [
    path('admin/', admin.site.urls),

    # path('account/', include('account.urls')),
    path('socialmedia/', include('socialmedia.urls')),
    path('api/', include('api.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)