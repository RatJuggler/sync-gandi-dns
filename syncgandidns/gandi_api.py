import logging
from typing import Dict

import requests


URL = "https://api.gandi.net/v5/livedns/domains/"
RECORDS = "/records/@/"
A_RECORD = 'A'
AAAA_RECORD = 'AAAA'


class GandiAPI:

    def __init__(self, api_key: str, domain: str) -> None:
        self.api_key = api_key
        self.domain = domain

    def get_rest_url(self, resource: str) -> str:
        return URL + self.domain + RECORDS + resource

    def get_headers(self) -> Dict[str, str]:
        return {"Authorization": "Apikey " + self.api_key}

    @staticmethod
    def get_update(resource: str, value: str) -> str:
        return '{"rrset_type": {0}, "rrset_values": ["{1}"]}'.format(resource, value)

    def _get_domain_record_resource_value(self, resource: str) -> str:
        response = requests.get(self.get_rest_url(resource),
                                headers=self.get_headers(),
                                timeout=4)
        logging.debug(response)
        response.raise_for_status()
        logging.debug(response.json())
        value = None
        if 'rrset_values' in response.json():
            values = response.json()['rrset_values']
            value = values[0]
        return value

    def get_ipv4_address(self) -> str:
        return self._get_domain_record_resource_value(A_RECORD)

    def get_ipv6_address(self) -> str:
        return self._get_domain_record_resource_value(AAAA_RECORD)

    def update_domain_record_resource(self, resource: str, value: str) -> None:
        response = requests.get(self.get_rest_url(resource),
                                headers=self.get_headers(),
                                data=self.get_update(resource, value),
                                timeout=3)
        response.raise_for_status()

    def update_ipv4_address(self, new_address) -> None:
        self.update_domain_record_resource(A_RECORD, new_address)

    def update_ipv6_address(self, new_address) -> None:
        self.update_domain_record_resource(AAAA_RECORD, new_address)
