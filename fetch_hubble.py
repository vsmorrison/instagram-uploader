import requests
import os
import argparse
import get_extensions_and_resize_tools


def get_images_ids_from_collection(collection):
    url = 'http://hubblesite.org/api/v3/images/{}'.format(collection)
    response = requests.get(url)
    response.raise_for_status()
    images = response.json()
    images_ids = [image['id'] for image in images]
    return images_ids


def get_hubble_images_links(images_ids):
    links = []
    for image_id in images_ids:
        url = 'http://hubblesite.org/api/v3/image/{}'.format(image_id)
        response = requests.get(url)
        response.raise_for_status()
        images = response.json()['image_files']
        for image in images:
            image_link = 'https:{}'.format(image['file_url'])
        links.append(image_link)
    return links


def save_hubble_images(urls, files_extensions):
    for url_index, url_value in enumerate(urls):
        response = requests.get(url_value, verify=False)
        response.raise_for_status()
        filepath = 'images/hubble{}.{}'.format(
            url_index,
            files_extensions[url_index]
        )
        with open(filepath, 'wb') as file:
            file.write(response.content)
        get_extensions_and_resize_tools.save_resized_images()


if __name__ == '__main__':
    os.makedirs('images', exist_ok=True)
    os.makedirs('thumbnails', exist_ok=True)
    parser = argparse.ArgumentParser()
    parser.add_argument('collection', help='Коллекция фотографий')
    args = parser.parse_args()
    try:
        images_ids = get_images_ids_from_collection(args.collection)
        url_hubble = get_hubble_images_links(images_ids)
        save_hubble_images(
            url_hubble,
            get_extensions_and_resize_tools.get_files_extensions(
                get_hubble_images_links(images_ids)
            )
        )
    except requests.HTTPError as error:
        exit('An error occured: {}'.format(error))
