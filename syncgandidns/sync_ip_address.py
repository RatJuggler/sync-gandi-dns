import logging
from typing import Optional

from .ipv4address_param import IPV4_ADDRESS
from .ipv6address_param import IPV6_ADDRESS
from .ipify_api import get_ipv4_address, get_ipv6_address
from .gandi_api import GandiAPI


def _sync_ip(ip_type: str, new_ip: Optional[str], get_ip: callable, update_ip: callable) -> None:
    current_ip = get_ip()
    logging.info("Current {0}: {1}".format(ip_type, current_ip))
    if new_ip is None:
        logging.info("New {0} not supplied so not updated.".format(ip_type))
    elif new_ip == current_ip:
        logging.info("{0} already current so not updated.".format(ip_type))
    else:
        update_ip(new_ip)
        logging.info("{0} updated to: {1}".format(ip_type, new_ip))


def _sync_ip_address(apikey: str, domain: str, ipv4: Optional[str], ipv6: Optional[str]) -> None:
    gandi_api = GandiAPI(apikey, domain)
    _sync_ip('IPV4', ipv4, gandi_api.get_ipv4_address, gandi_api.update_ipv4_address)
    _sync_ip('IPV6', ipv6, gandi_api.get_ipv6_address, gandi_api.update_ipv6_address)


def _get_ip_address(ip_type: str, get_ip: callable, ip_validate: callable) -> Optional[str]:
    ip_address = get_ip()
    logging.info("...found: {0}".format(ip_address))
    if ip_validate(ip_address) is None:
        logging.info("...not valid {0} won't update.".format(ip_type))
        ip_address = None
    return ip_address


def do_sync(domain: str, apikey: str, no_ipv4: bool, ipv4: str, no_ipv6: bool, ipv6: str) -> None:
    logging.info("Updating DNS for domain: {0}".format(domain))
    logging.info("Update IPV4 to: {0}".format('<disabled>' if no_ipv4 else '<automatic lookup>' if ipv4 is None else ipv4))
    if not no_ipv4 and ipv4 is None:
        ipv4 = _get_ip_address('IPV4', get_ipv4_address, IPV4_ADDRESS.validate)
    logging.info("Update IPV6 to: {0}".format('<disabled>' if no_ipv6 else '<automatic lookup>' if ipv6 is None else ipv6))
    if not no_ipv6 and ipv6 is None:
        ipv6 = _get_ip_address('IPV6', get_ipv6_address, IPV6_ADDRESS.validate)
    _sync_ip_address(apikey, domain, ipv4, ipv6)
