from django.contrib import admin
from image import models as image_models


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'level')
    readonly_fields = ('image',)


class ImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'image')


class UserLevelAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


class ImageSizeAdmin(admin.ModelAdmin):
    list_display = ('id', 'height')


class ImageThumbnailAdmin(admin.ModelAdmin):
    list_display = ('id', 'image', 'size', 'date_of_used')

class ExpiringLinkAdmin(admin.ModelAdmin):
    list_display = ('id', 'image', 'token', 'expires_at')

admin.site.register(image_models.Image, ImageAdmin)
admin.site.register(image_models.UserProfile, UserProfileAdmin)
admin.site.register(image_models.UserLevel, UserLevelAdmin)
admin.site.register(image_models.ImageSize, ImageSizeAdmin)
admin.site.register(image_models.ImageThumbnail, ImageThumbnailAdmin)
admin.site.register(image_models.ExpiringLink, ExpiringLinkAdmin)
