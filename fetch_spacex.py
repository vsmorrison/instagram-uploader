import requests
import os
import get_extensions_and_resize_tools


def save_spacex_last_launch(urls, files_extensions):
    for url_index, url_value in enumerate(urls):
        response = requests.get(url_value)
        response.raise_for_status()
        filepath = 'images/spacex{}.{}'.format(
            url_index,
            files_extensions[url_index]
        )
        with open(filepath, 'wb') as file:
            file.write(response.content)


def get_spacex_flickr_links():
    url = 'https://api.spacexdata.com/v3/launches/latest'
    response = requests.get(url)
    response.raise_for_status()
    flickr_links = response.json()['links']['flickr_images']
    return flickr_links


if __name__ == '__main__':
    os.makedirs('images', exist_ok=True)
    os.makedirs('thumbnails', exist_ok=True)
    try:
        url_spacex = get_spacex_flickr_links()
        save_spacex_last_launch(
            url_spacex,
            get_extensions_and_resize_tools.get_files_extensions(
                get_spacex_flickr_links()
            )
        )
        get_extensions_and_resize_tools.save_resized_images()
    except requests.HTTPError as error:
        exit('An error occured: {}'.format(error))

