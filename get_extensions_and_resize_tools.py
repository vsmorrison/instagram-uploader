import os
from PIL import Image


def get_files_extensions(urls):
    extensions = [url.split('.')[-1] for url in urls]
    return extensions


def resize_images(images):
    size = images.size
    width, height = size
    horizontal_ratio = 16 / 9
    vertical_ratio = 0.8
    if width == height:
        size = (width, height)
    elif width > height:
        size = (width, int(width / horizontal_ratio))
    elif width < height:
        size = (int(height * vertical_ratio), height)
    resized_image = images.resize(size)
    return resized_image


def save_resized_images():
    images = os.listdir('images')
    for image in images:
        filepath = 'images/{}'.format(image)
        new_image = Image.open(filepath)
        new_image = resize_images(new_image)
        new_image.save(
            'thumbnails/{}_thubmnail.{}'.format(
                image.split('.')[0],
                image.split('.')[1]
            )
        )
