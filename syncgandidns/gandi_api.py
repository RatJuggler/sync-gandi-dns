import logging
from typing import Dict

import requests


class GandiAPI:

    def __init__(self, api_key: str, domain: str) -> None:
        self.__api_key = api_key
        self.__domain = domain
        self.__livedns = 'https://api.gandi.net/livedns/'

    def _get_domain_records_url(self) -> str:
        return self.__livedns + 'domains/' + self.__domain + '/records'

    def _get_domain_record_url(self, resource: str) -> str:
        # @ is the DNS record name (rrset_name).
        return self._get_domain_records_url() + '/@/' + resource

    def _get_headers(self) -> Dict[str, str]:
        return {'Authorization': '"Apikey ' + self.__api_key, 'Content-Type': 'application/json'}

    @staticmethod
    def _get_update(resource: str, value: str) -> str:
        return '{{"rrset_type": "{0}", "rrset_values": ["{1}"]}}'.format(resource, value)

    def _get_domain_record_resource_value(self, resource: str) -> str:
        response = requests.get(self._get_domain_record_url(resource),
                                headers=self._get_headers(),
                                timeout=4)
        logging.debug(response)
        response.raise_for_status()
        logging.debug(response.json())
        value = None
        if 'rrset_values' in response.json():
            values = response.json()['rrset_values']
            value = values[0]
        return value

    def get_domain_records(self) -> str:
        response = requests.get(self._get_domain_records_url(),
                                headers=self._get_headers(),
                                timeout=4)
        logging.debug(response)
        response.raise_for_status()
        logging.debug(response.json())
        return response.json()

    def get_ipv4_address(self) -> str:
        return self._get_domain_record_resource_value('A')

    def get_ipv6_address(self) -> str:
        return self._get_domain_record_resource_value('AAAA')

    def _update_domain_record_resource(self, resource: str, value: str) -> None:
        response = requests.put(self._get_domain_record_url(resource),
                                headers=self._get_headers(),
                                data=self._get_update(resource, value),
                                timeout=4)
        response.raise_for_status()

    def update_ipv4_address(self, new_address) -> None:
        self._update_domain_record_resource('A', new_address)

    def update_ipv6_address(self, new_address) -> None:
        self._update_domain_record_resource('AAAA', new_address)
