"""
lesson27 URL Configuration
"""
from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path, include
from django.conf import settings
from ads.views import IndexView, AddToCat, AddToAd


urlpatterns = [
    path('admin/', admin.site.urls), # +
    path('', IndexView.as_view()), # +

    path('ad/', include('ads.urls1')),
    path('cat/', include('ads.urls2')), # +
    path('users/', include('users.urls')), # +

    path('addc/', AddToCat.as_view()), # +
    path('adda/', AddToAd.as_view()),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# 404
handler404 = "lesson27.views.page_not_found_view"