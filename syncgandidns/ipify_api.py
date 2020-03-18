import logging
import requests


IPV4_URL = 'https://api.ipify.org'
IPV6_URL = 'https://api6.ipify.org'


def _get_ip_address(api_url: str):
    response = requests.get(api_url,
                            timeout=3)
    logging.debug(response)
    response.raise_for_status()
    return response.text


def get_ipv4_address():
    return _get_ip_address(IPV4_URL)


def get_ipv6_address():
    return _get_ip_address(IPV6_URL)
