import logging
from typing import Optional

from .gandi_api import GandiAPI


def sync_ip_address(domain: str, ipv4: Optional[str], ipv6: Optional[str], apikey: str) -> None:
    gandi_api = GandiAPI(apikey, domain)
    current_ipv4 = gandi_api.get_ipv4_address()
    current_ipv6 = gandi_api.get_ipv6_address()
    logging.info("Current: IPV4 = {0}, IPV6 = {1}".format(current_ipv4, current_ipv6))
    if ipv4 is None:
        logging.info("New IPV4 not supplied so not updated.")
    elif ipv4 == current_ipv4:
        logging.info("IPV4 already current so not updated.")
    else:
        gandi_api.update_ipv4_address(ipv4)
        logging.info("IPV4 updated to: {0}".format(ipv4))
    if ipv6 is None:
        logging.info("New IPV6 not supplied so not updated.")
    elif ipv6 == current_ipv6:
        logging.info("IPV6 already current so not updated.")
    else:
        gandi_api.update_ipv6_address(ipv6)
        logging.info("IPV6 updated to: {0}".format(ipv6))
