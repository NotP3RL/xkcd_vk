import requests


class VK_API_Error(Exception):
    pass


def download_picture(url, path, params=''):
    response = requests.get(url, params)
    response.raise_for_status()
    with open(path, 'wb') as file:
        file.write(response.content)

def find_vk_api_error(response):
    if 'error' in response:
        raise VK_API_Error(response['error']['error_msg'])
