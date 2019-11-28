import logging
import requests


URL = "https://api.gandi.net/v5/livedns/domains/"
RECORDS = "/records/@/"


class GandiAPI:

    def __init__(self, api_key: str, domain: str):
        self.api_key = api_key
        self.domain = domain

    def get_rest_url(self, resource: str):
        return URL + self.domain + RECORDS + resource

    def get_headers(self):
        return {"Authorization": "Apikey " + self.api_key}

    def get_update(self, resource: str, value: str):
        return '{"rrset_type": {0}, "rrset_values": ["{1}"]}'.format(resource, value)

    def get_domain_record_resource_value(self, resource: str) -> str:
        response = requests.get(self.get_rest_url(resource),
                                headers=self.get_headers(),
                                timeout=3)
        logging.debug(response)
        response.raise_for_status()
        logging.debug(response.json())
        value = None
        if 'rrset_values' in response.json():
            values = response.json()['rrset_values']
            value = values[0]
        return value

    def update_domain_record_resource(self, resource: str, value: str):
        response = requests.get(self.get_rest_url(resource),
                                headers=self.get_headers(),
                                data=self.get_update(resource, value),
                                timeout=3)
        response.raise_for_status()
