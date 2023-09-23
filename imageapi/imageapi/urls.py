"""
URL configuration for imageapi project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from image import views as image_views
from django.urls import path, re_path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('load/', image_views.LoadImageView.as_view(), name='load'),
    path('images/', image_views.get_user_images, name='user-images'),
    re_path(r'^images/(?P<filename>[\w\-]+\.\w+)$', image_views.image_view, name='image_view'),
    re_path(r'^thumbnails/(?P<filename>[\w\-]+\.\w+)$', image_views.imagethumbnail_view, name='thumbnail_view'),
    path('create-expiring-link/', image_views.CreateExpiringLinkView.as_view(), name='create_expiring_link'),
    path('expiring/<uuid:token>/', image_views.expiring_link_view, name='expiring_link_view'),
]
