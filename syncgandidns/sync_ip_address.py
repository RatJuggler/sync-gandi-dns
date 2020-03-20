import logging
from typing import Optional

from .gandi_api import GandiAPI


def sync_ip(ip_type: str, new_ip: Optional[str], get_ip: callable, update_ip: callable) -> None:
    current_ip = get_ip()
    logging.info("Current {0}: {1}".format(ip_type, current_ip))
    if new_ip is None:
        logging.info("New {0} not supplied so not updated.".format(ip_type))
    elif new_ip == current_ip:
        logging.info("{0} already current so not updated.".format(ip_type))
    else:
        update_ip(new_ip)
        logging.info("{0} updated to: {1}".format(ip_type, new_ip))


def sync_ip_address(domain: str, ipv4: Optional[str], ipv6: Optional[str], apikey: str) -> None:
    gandi_api = GandiAPI(apikey, domain)
    sync_ip('IPV4', ipv4, gandi_api.get_ipv4_address, gandi_api.update_ipv4_address)
    sync_ip('IPV6', ipv6, gandi_api.get_ipv6_address, gandi_api.update_ipv6_address)
