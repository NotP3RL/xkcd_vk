import logging
import os
from pathlib import Path
from random import randint

import requests
from dotenv import load_dotenv

from tools import VK_API_Error, download_picture, find_vk_api_error


IMAGE_PATH = "images"


def download_random_comic():
    last_comic = requests.get('https://xkcd.com/info.0.json')
    last_comic.raise_for_status()
    random_comic_number = randint(1, last_comic.json()['num'])
    random_comic_url = f'https://xkcd.com/{random_comic_number}/info.0.json'
    random_comic = requests.get(random_comic_url)
    random_comic.raise_for_status()
    random_comic = random_comic.json()
    os.makedirs(IMAGE_PATH, exist_ok=True)
    download_picture(
        random_comic['img'],
        f'{IMAGE_PATH}/{random_comic_number}.png'
    )
    return random_comic['alt'], random_comic_number


def get_upload_url(access_token, group_id):
    params = {
        'access_token': access_token,
        'group_id': group_id,
        'v': '5.131'
    }
    url = 'https://api.vk.com/method/photos.getWallUploadServer'
    response = requests.get(url, params=params)
    response.raise_for_status()
    response = response.json()
    find_vk_api_error(response)
    return response['response']['upload_url']


def upload_file(access_token, group_id, comic_number):
    with open(f'images/{comic_number}.png', 'rb') as file:
        url = get_upload_url(access_token, group_id)
        files = {
            'photo': file
        }
        response = requests.post(url, files=files)
        response.raise_for_status()
        response = response.json()
        find_vk_api_error(response)
        return response


def save_comic_in_album(access_token, group_id, photo_file):
    params = {
        'access_token': access_token,
        'group_id': group_id,
        'server': photo_file['server'],
        'photo': photo_file['photo'],
        'hash': photo_file['hash'],
        'v': '5.131'
    }
    url = 'https://api.vk.com/method/photos.saveWallPhoto'
    response = requests.post(url, params=params)
    response.raise_for_status()
    response = response.json()
    find_vk_api_error(response)
    return response["response"][0]["id"]


def post_comic_to_wall(access_token, group_id, text, photo_file):
    params = {
        'access_token': access_token,
        'owner_id': -int(group_id),
        'from_group': 1,
        'message': text,
        'attachments': photo_id,
        'v': '5.131'
    }
    url = 'https://api.vk.com/method/wall.post'
    response = requests.post(url, params=params)
    response.raise_for_status()
    find_vk_api_error(response.json())


if __name__ == "__main__":
    load_dotenv()
    user_id = os.getenv('USER_ID')
    access_token = os.getenv('ACCESS_TOKEN')
    group_id = os.getenv('GROUP_ID')
    try:
        text, number = download_random_comic()
        photo_file = upload_file(access_token, group_id, number)
        photo_id = f'photo{user_id}' \
        f'_{save_comic_in_album(access_token, group_id, photo_file)}'
        post_comic_to_wall(access_token, group_id, text, photo_id)
    except VK_API_Error as VK_Error:
        logging.error(VK_Error)
    except requests.exceptions.HTTPError as error:
        logging.error(error)
    finally:
        files_in_dir = os.listdir(IMAGE_PATH)
        for file in files_in_dir:
            os.remove(f'{IMAGE_PATH}/{file}')
        os.rmdir(IMAGE_PATH)
