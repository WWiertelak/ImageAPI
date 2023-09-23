from rest_framework import serializers
import image.models as image_models
from datetime import datetime, timedelta


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = image_models.Image
        fields = ('title', 'image')


class ExpiringLinkSerializer(serializers.ModelSerializer):
    expiration_seconds = serializers.IntegerField(write_only=True, min_value=300, max_value=30000)

    class Meta:
        model = image_models.ExpiringLink
        fields = ('image', 'token', 'expiration_seconds')

    def __init__(self, *args, **kwargs):
        super(ExpiringLinkSerializer, self).__init__(*args, **kwargs)
        
        # Limit the queryset to images owned by the user
        user = self.context['request'].user
        self.fields['image'].queryset = image_models.Image.objects.filter(userprofile__user=user)

    def create(self, validated_data):
        expiration_seconds = validated_data.pop('expiration_seconds', None)
        expires_at = datetime.now() + timedelta(seconds=expiration_seconds)
        validated_data['expires_at'] = expires_at
        return super().create(validated_data)
