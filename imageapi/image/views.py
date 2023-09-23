from rest_framework import generics, status
import image.models as image_models
import image.serializers as image_serializers
from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404
from django.utils.timezone import make_aware
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import redirect
from .tasks import generate_and_store_thumbnails
from .utils import full_image_url
from datetime import datetime, timedelta



class LoadImageView(generics.CreateAPIView):
    queryset = image_models.Image.objects.all()
    serializer_class = image_serializers.ImageSerializer

    def perform_create(self, serializer):
        image_instance = serializer.save()

        user_profile = self.request.user.userprofile
        user_profile.image.add(image_instance) # Add image to user profile


class CreateExpiringLinkView(generics.CreateAPIView):
    queryset = image_models.ExpiringLink.objects.all()
    serializer_class = image_serializers.ExpiringLinkSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        user_profile = image_models.UserProfile.objects.get(user=request.user)
        if not user_profile.level.exp_link:
            return Response({"detail": "Link generation capability is reserved for higher-level accounts."}, status=status.HTTP_403_FORBIDDEN)

        response = super().create(request, *args, **kwargs)
        if response.status_code == status.HTTP_201_CREATED:
            link_token = response.data.get('token')
            base_url = request.build_absolute_uri('/')[:-1]  # get the base URL without the trailing slash
            full_link = f"{base_url}/expiring/{link_token}/"
            response.data['link'] = full_link
        return response

    def perform_create(self, serializer):
        expiration_seconds = int(self.request.data.get('expiration_seconds'))
        expires_at = datetime.now() + timedelta(seconds=expiration_seconds)
        serializer.save(expires_at=expires_at)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_images(request):
    user_profile = image_models.UserProfile.objects.get(user=request.user)
    images = user_profile.image.all()
    response_data = []

    for img in images:
        thumbnails_data = generate_and_store_thumbnails(img.id, user_profile.level.id)
        # Convert relative url to full url
        for key, value in thumbnails_data.items():
            thumbnails_data[key] = full_image_url(request, value)

        data = {
            "title": img.title,
            "thumbnails": thumbnails_data
        }
        response_data.append(data)
    
    return Response(response_data)

def image_view(request, filename):
    image = get_object_or_404(image_models.Image, image__endswith=filename)
    with open(image.image.path, 'rb') as f:
        return HttpResponse(f.read(), content_type="image/jpeg")

def imagethumbnail_view(request, filename):
    image = get_object_or_404(image_models.ImageThumbnail, thumbnail__endswith=filename)
    with open(image.thumbnail.path, 'rb') as f:
        return HttpResponse(f.read(), content_type="image/jpeg")

def expiring_link_view(request, token):
    try:
        link = image_models.ExpiringLink.objects.get(token=token)
        if make_aware(datetime.now()) > link.expires_at:
            raise Http404("Link has expired")
        return redirect(link.image.image.url)
    except image_models.ExpiringLink.DoesNotExist:
        raise Http404("Link not found")

