import logging
import requests


URL = "https://api.gandi.net/v5/livedns/domains/"
RECORDS = "/records/@/"


def get_rest_url(domain: str, resource: str):
    return URL + domain + RECORDS + resource


def get_headers(api_key: str):
    return {"Authorization": "Apikey " + api_key}


def get_update(resource: str, value: str):
    return '{"rrset_type": {0}, "rrset_values": ["{1}"]}'.format(resource, value)


def get_domain_record_resource_value(api_key: str, domain: str, resource: str) -> str:
    response = requests.get(get_rest_url(domain, resource),
                            headers=get_headers(api_key),
                            timeout=3)
    logging.debug(response)
    response.raise_for_status()
    logging.debug(response.json())
    value = None
    if 'rrset_values' in response.json():
        values = response.json()['rrset_values']
        value = values[0]
    return value


def update_domain_record_resource(api_key: str, domain: str, resource: str, value: str):
    response = requests.get(get_rest_url(domain, resource),
                            headers=get_headers(api_key),
                            data=get_update(resource, value),
                            timeout=3)
    response.raise_for_status()
