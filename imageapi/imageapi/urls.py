from django.urls import include, path, re_path
from django.contrib import admin
from image import views as image_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('image/', include(('image.urls'), namespace='image')),
    re_path(r'^images/(?P<filename>[\w\-]+\.\w+)$', image_views.image_view, name='image_view'),
    re_path(r'^thumbnails/(?P<filename>[\w\-]+\.\w+)$', image_views.imagethumbnail_view, name='thumbnail_view'),
    path('expiring/<uuid:token>/', image_views.expiring_link_view, name='expiring_link_view'),
]