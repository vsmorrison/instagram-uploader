import requests
import os
from PIL import Image


def create_directory():
    try:
        os.makedirs('images')
        os.makedirs('thumbnails')
    except FileExistsError:
        pass


def save_spacex_last_launch(url, file_extension):
    for url_index, url_value in enumerate(url):
        response = requests.get(url_value)
        filepath = 'images/spacex{}.{}'.format(
            url_index,
            file_extension[url_index]
        )
        with open(filepath, 'wb') as file:
            file.write(response.content)


def get_spacex_flickr_links():
    url = 'https://api.spacexdata.com/v3/launches/latest'
    response = requests.get(url)
    flickr_links = response.json()['links']['flickr_images']
    return flickr_links


def get_file_extension(url):
    extension = []
    for url in url:
        extension.append(url.split('.')[-1])
    return extension


def resize_image(image):
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


def save_resized_image():
    images = os.listdir('images')
    for image in images:
        if image.split('.')[1] != 'pdf':
            filepath = 'images/{}'.format(image)
            new_image = Image.open(filepath)
            new_image = resize_image(new_image)
            new_image.save(
                'thumbnails/{}_thubmnail.{}'.format(
                    image.split('.')[0],
                    image.split('.')[1]
                )
            )
        else:
            continue


if __name__ == '__main__':
    create_directory()
    url_spacex = get_spacex_flickr_links()
    save_spacex_last_launch(url_spacex, get_file_extension(get_spacex_flickr_links()))
    save_resized_image()
