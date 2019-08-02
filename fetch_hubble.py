import requests
import os
import argparse
from PIL import Image


def get_images_id_from_collections(collection):
    images_id = []
    url = 'http://hubblesite.org/api/v3/images/{}'.format(collection)
    response = requests.get(url)
    response.raise_for_status()
    images = response.json()
    for image in images:
        image_id = image['id']
        images_id.append(image_id)
    return images_id


def get_hubble_images_links(images_id):
    links = []
    for image_id in images_id:
        url = 'http://hubblesite.org/api/v3/image/{}'.format(image_id)
        response = requests.get(url)
        response.raise_for_status()
        images = response.json()['image_files']
        for image in images:
            image_link = 'https:{}'.format(image['file_url'])
        links.append(image_link)
    return links


def get_file_extensions(url):
    extensions = []
    for url in url:
        extensions.append(url.split('.')[-1])
    return extensions


def save_hubble_images(url, file_extension):
    for url_index, url_value in enumerate(url):
        response = requests.get(url_value, verify=False)
        response.raise_for_status()
        filepath = 'images/hubble{}.{}'.format(
            url_index,
            file_extension[url_index]
        )
        with open(filepath, 'wb') as file:
            file.write(response.content)
        save_resized_images()


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
        filepath = 'images/{}'.format(image)
        new_image = Image.open(filepath)
        new_image = resize_images(new_image)
        new_image.save(
            'thumbnails/{}_thubmnail.{}'.format(
                image.split('.')[0],
                image.split('.')[1]
            )
        )


if __name__ == '__main__':
    os.makedirs('images', exist_ok=True)
    os.makedirs('thumbnails', exist_ok=True)
    parser = argparse.ArgumentParser()
    parser.add_argument('collection', help='Коллекция фотографий')
    args = parser.parse_args()
    try:
        images_id = get_images_id_from_collections(args.collection)
        url_hubble = get_hubble_images_links(images_id)
        save_hubble_images(
            url_hubble,
            get_file_extensions(get_hubble_images_links(images_id))
        )
    except requests.HTTPError as error:
        exit('An error occured: {}'.format(error))
