import logging
import requests


URL = "https://api.gandi.net/v5/livedns/domains/"


def get_domain_record_resource(api_key: str, domain: str, resource: str):
    url = URL + domain + "/records/@/" + resource
    headers = {"Authorization": "Apikey " + api_key}
    logging.info("GET: " + url)
    response = requests.get(url, headers=headers, timeout=3)
    logging.debug(response.json())
