import logging

from .gandi_api import GandiAPI


def sync_ip_address(domain: str, ipv4: str, ipv6: str, apikey: str) -> None:
    gandi_api = GandiAPI(apikey, domain)
    current_ipv4 = gandi_api.get_ipv4_address()
    current_ipv6 = gandi_api.get_ipv6_address()
    logging.info("Current: IPV4 = {0}, IPV6 = {1}".format(current_ipv4, current_ipv6))
    if ipv4 != current_ipv4:
        gandi_api.update_ipv4_address(ipv4)
    if ipv6 != current_ipv6:
        gandi_api.update_ipv6_address(ipv6)
