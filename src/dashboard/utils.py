import requests
from core.settings import env


def create_image(data):
    HCTI_API_ENDPOINT = "https://hcti.io/v1/image"
    HCTI_API_USER_ID = env("HCTI_API_USER_ID")
    HCTI_API_KEY = env("HCTI_API_KEY")
    data = data
    image = requests.post(url = HCTI_API_ENDPOINT, data = data, auth=(HCTI_API_USER_ID, HCTI_API_KEY))
    return image.json()["url"]
