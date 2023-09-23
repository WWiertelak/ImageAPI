from PIL import Image as PILImage
from image import models as image_models
from celery import shared_task
from django.core.files import File
import os
from io import BytesIO
from datetime import datetime, timedelta
from django.utils.timezone import make_aware



@shared_task
def generate_and_store_thumbnails(image_id, user_level_id):
    '''Generate thumbnails for the given image and store them in the database.
      Return a dictionary of links to the thumbnails.'''
    image_instance = image_models.Image.objects.get(pk=image_id)
    user_level = image_models.UserLevel.objects.get(pk=user_level_id)
    
    available_sizes = user_level.size.all()
    links = {}

    for size in available_sizes:
        thumbnail, created = image_models.ImageThumbnail.objects.get_or_create(
            image=image_instance, size=size
        )
        if created:
            # If thumbnail doesn't exist, create it
            pil_image = PILImage.open(image_instance.image.path)
            aspect = pil_image.width / pil_image.height
            new_width = int(size.height * aspect)
            pil_image.thumbnail((new_width, size.height))

            # Save thumbnail to memory
            thumb_io = BytesIO()
            file_format = image_instance.image.url.split('.')[-1].upper()
            pil_image.save(thumb_io, format=file_format)
            thumb_filename = f"thumbnail_{size.height}_{image_instance.title}.{file_format.lower()}"
            thumbnail.thumbnail = File(thumb_io, name=thumb_filename)
            thumbnail.save()

        links[str(size.height)] = thumbnail.thumbnail.url
        thumbnail.date_of_used = datetime.now() # Update date of used
        thumbnail.save(update_fields=['date_of_used'])

    # Add link to original image if user level allows it
    if user_level.org_link:
        links["Orginal"] = image_instance.image.url

    return links

@shared_task
def remove_old_thumbnails():
    '''Remove thumbnails that haven't been used for 30 days.'''
    usage_date = make_aware(datetime.now() - timedelta(days=30))
    old_images = image_models.ImageThumbnail.objects.filter(date_of_used__lt=usage_date)

    for image in old_images:
        image.thumbnail.delete()
    old_images.delete()

@shared_task
def remove_expired_links():
    '''Remove expired links from database.'''
    expiry_date = make_aware(datetime.now() - timedelta(days=30))
    expired_links = image_models.ExpiringLink.objects.filter(expires_at__lt=expiry_date)
    expired_links.delete()
