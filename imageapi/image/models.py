from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import FileExtensionValidator
import uuid



class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    level = models.ForeignKey('UserLevel', on_delete=models.SET_NULL, null=True)
    image = models.ManyToManyField('Image')

    def __str__(self):
        return str(self.user.username)

class Image(models.Model):
    title = models.CharField(max_length=100, blank=True, null=True)
    image = models.ImageField(upload_to='images/', validators=[FileExtensionValidator(['jpg', 'png'])])

    def __str__(self):
        return str(self.title)

class UserLevel(models.Model):
    name = models.CharField(max_length=25)
    size = models.ManyToManyField('ImageSize')
    exp_link = models.BooleanField(default=False, verbose_name='Expiring link')
    org_link = models.BooleanField(default=False, verbose_name='Original link')

    def __str__(self):
        return str(self.name)

class ImageSize(models.Model):
    height = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.height}px'
    
class ImageThumbnail(models.Model):
    image = models.ForeignKey('Image', on_delete=models.CASCADE)
    size = models.ForeignKey('ImageSize', on_delete=models.CASCADE)
    thumbnail = models.ImageField(upload_to='thumbnails/', validators=[FileExtensionValidator(['jpg', 'png'])])
    date_of_used = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.image} - {self.size}'


class ExpiringLink(models.Model):
    image = models.ForeignKey(Image, on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    expires_at = models.DateTimeField()


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    user_level = UserLevel.objects.get(name='Basic')
    if created:
        UserProfile.objects.create(user=instance, level=user_level)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()