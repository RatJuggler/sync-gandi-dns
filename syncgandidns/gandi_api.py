import logging
from typing import Dict

import requests


class GandiAPI:

    def __init__(self, api_key: str) -> None:
        self.__api_key = api_key
        self.__livedns = 'https://api.gandi.net/v5/livedns/'

    def _get_domain_records_url(self, domain: str) -> str:
        return self.__livedns + 'domains/' + domain + '/records'

    def _get_domain_record_url(self, domain: str, resource: str) -> str:
        # @ is the DNS record name (rrset_name).
        return self._get_domain_records_url(domain) + '/@/' + resource

    def _get_headers(self) -> Dict[str, str]:
        return {'Authorization': 'Apikey ' + self.__api_key, 'Content-Type': 'application/json'}

    @staticmethod
    def _get_update(resource: str, value: str) -> str:
        return '{{"rrset_type": "{0}", "rrset_values": ["{1}"]}}'.format(resource, value)

    def _get_domain_record_resource_value(self, domain: str, resource: str) -> str:
        response = requests.get(self._get_domain_record_url(domain, resource),
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

    def get_domain_records(self, domain: str) -> str:
        response = requests.get(self._get_domain_records_url(domain),
                                headers=self._get_headers(),
                                timeout=4)
        logging.debug(response)
        response.raise_for_status()
        logging.debug(response.json())
        return response.json()

    def get_ipv4_address(self, domain: str) -> str:
        return self._get_domain_record_resource_value(domain, 'A')

    def get_ipv6_address(self, domain: str) -> str:
        return self._get_domain_record_resource_value(domain, 'AAAA')

    def _update_domain_record_resource(self, domain: str, resource: str, value: str) -> None:
        response = requests.put(self._get_domain_record_url(domain, resource),
                                headers=self._get_headers(),
                                data=self._get_update(resource, value),
                                timeout=4)
        response.raise_for_status()

    def update_ipv4_address(self, domain: str, new_address: str) -> None:
        self._update_domain_record_resource(domain, 'A', new_address)

    def update_ipv6_address(self, domain: str, new_address: str) -> None:
        self._update_domain_record_resource(domain, 'AAAA', new_address)
