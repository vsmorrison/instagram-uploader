import os
from settings import LOGIN, PASSWORD
from instabot import Bot


def upload_image_to_instagram():
    bot = Bot()
    bot.login(username=LOGIN, password=PASSWORD)
    images = os.listdir('thumbnails')
    for image_index, filename in enumerate(images):
        bot.upload_photo(
            "thumbnails/{}".format(filename),
            caption="Space Picture - {}\n".format(image_index)
        )


if __name__ == '__main__':
    upload_image_to_instagram()
