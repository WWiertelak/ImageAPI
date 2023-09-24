
from django.urls import path
from image import views as image_views
from django.urls import path

app_name = 'image'

urlpatterns = [
    path('load/', image_views.LoadImageView.as_view(), name='load'),
    path('images/', image_views.get_user_images, name='user-images'),
    path('create-expiring-link/', image_views.CreateExpiringLinkView.as_view(), name='create_expiring_link'),
]
