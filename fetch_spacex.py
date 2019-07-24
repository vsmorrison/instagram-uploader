import requests
import os
from PIL import Image


def create_directories():
    os.makedirs('images', exist_ok=True)
    os.makedirs('thumbnails', exist_ok=True)


def save_spacex_last_launch(url, file_extensions):
    for url_index, url_value in enumerate(url):
        response = requests.get(url_value)
        filepath = 'images/spacex{}.{}'.format(
            url_index,
            file_extensions[url_index]
        )
        with open(filepath, 'wb') as file:
            file.write(response.content)


def get_spacex_flickr_links():
    url = 'https://api.spacexdata.com/v3/launches/latest'
    response = requests.get(url)
    flickr_links = response.json()['links']['flickr_images']
    return flickr_links


def get_file_extensions(url):
    extensions = []
    for url in url:
        extensions.append(url.split('.')[-1])
    return extensions


def resize_images(image):
    size = image.size
    width, height = size
    horizontal_ratio = 16 / 9
    vertical_ratio = 0.8
    if width == height:
        size = (width, height)
    elif width > height:
        size = (width, int(width / horizontal_ratio))
    elif width < height:
        size = (int(height * vertical_ratio), height)
    resized_image = image.resize(size)
    return resized_image


def save_resized_images():
    images = os.listdir('images')
    for image in images:
        if image.split('.')[1] != 'pdf':
            filepath = 'images/{}'.format(image)
            new_image = Image.open(filepath)
            new_image = resize_images(new_image)
            new_image.save(
                'thumbnails/{}_thubmnail.{}'.format(
                    image.split('.')[0],
                    image.split('.')[1]
                )
            )
        else:
            continue


if __name__ == '__main__':
    create_directories()
    url_spacex = get_spacex_flickr_links()
    save_spacex_last_launch(url_spacex, get_file_extensions(get_spacex_flickr_links()))
    save_resized_images()
