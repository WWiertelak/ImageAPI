from django.conf import settings



def full_image_url(request, image_path):
    return f"{request.scheme}://{request.get_host()}{image_path}"
