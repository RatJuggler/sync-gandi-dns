import logging
from typing import Dict

import requests


class GandiAPI:

    def __init__(self, api_key: str, domain: str) -> None:
        self.__api_key = api_key
        self.__domain = domain
        root_url = 'https://api.gandi.net/'
        self.__livedns = root_url + 'livedns/'
        self.__organization = root_url + 'organization/'

    def get_domain_record_url(self, resource: str) -> str:
        # @ is the DNS record name (rrset_name).
        return self.__livedns + 'domains/' + self.__domain + '/records/@/' + resource

    def get_headers(self) -> Dict[str, str]:
        return {'Authorization': '"Apikey ' + self.__api_key, 'Content-Type': 'application/json'}

    @staticmethod
    def get_update(resource: str, value: str) -> str:
        return '{{"rrset_type": "{0}", "rrset_values": ["{1}"]}}'.format(resource, value)

    def _get_domain_record_resource_value(self, resource: str) -> str:
        response = requests.get(self.get_domain_record_url(resource),
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
        return self._get_domain_record_resource_value('A')

    def get_ipv6_address(self) -> str:
        return self._get_domain_record_resource_value('AAAA')

    def _update_domain_record_resource(self, resource: str, value: str) -> None:
        response = requests.put(self.get_domain_record_url(resource),
                                headers=self.get_headers(),
                                data=self.get_update(resource, value),
                                timeout=3)
        response.raise_for_status()

    def update_ipv4_address(self, new_address) -> None:
        self._update_domain_record_resource('A', new_address)

    def update_ipv6_address(self, new_address) -> None:
        self._update_domain_record_resource('AAAA', new_address)
