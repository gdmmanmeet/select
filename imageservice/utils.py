from django.conf import settings
import os
from PIL import Image

IMG_METADATA_SIZE = 100  # in bytes


def get_image_path(filename, user_id):
    return os.path.join(settings.STORAGE_PATH, str(user_id), filename)


def save_image(image_file, path):
    """
    save file with content_type at the end of file
    """
    with open(path, 'wb+') as f:
        for chunk in image_file:
            f.write(chunk)
        content_type = (image_file.content_type + " " * IMG_METADATA_SIZE).encode('ascii')[:IMG_METADATA_SIZE]
        f.write(content_type)


def is_valid_image(image):
    try:
       Image.open(image)
    except IOError:
        return False
    return True


def image_exists(path):
    return os.path.exists(path)


def get_image(filename, user_id):
    """
    get file content in bytes and content type stored at the end of file.
    """
    try:
        f = open(get_image_path(filename, user_id), 'rb').read()
        return f[:-IMG_METADATA_SIZE], f[-IMG_METADATA_SIZE:].strip()
    except FileNotFoundError:
        return None, None


def delete_image(filename, user_id):
    os.remove(get_image_path(filename, user_id))


def get_user_images(user_id):
    try:
        return os.listdir(os.path.join(settings.STORAGE_PATH, str(user_id)))
    except:
        return []