import requests


def get_google_provider_cfg(discovery_url):
    return requests.get(discovery_url).json()
