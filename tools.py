import requests


def download_picture(url, path, params=''):
    response = requests.get(url, params)
    response.raise_for_status()
    with open(path, 'wb') as file:
        file.write(response.content)
