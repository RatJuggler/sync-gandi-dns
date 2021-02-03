import logging
from typing import Optional, Tuple

from .ipv4address_param import IPV4_ADDRESS
from .ipv6address_param import IPV6_ADDRESS
from .ipify_api import get_ipv4_address, get_ipv6_address
from .gandi_api import GandiAPI


def _sync_ip(domain: str, ip_type: str, new_ip: Optional[str], get_ip: callable, update_ip: callable) -> None:
    current_ip = get_ip(domain)
    logging.info("{0} current {1} address: {2}".format(domain, ip_type, current_ip))
    if new_ip is None:
        logging.info("{0} not updated, new {1} address not supplied!".format(domain, ip_type))
    elif new_ip == current_ip:
        logging.info("{0} {1} address already current so not updated.".format(domain, ip_type))
    else:
        update_ip(domain, new_ip)
        logging.info("{0} {1} address updated to: {2}".format(domain, ip_type, new_ip))


def _get_ip_address(ip_type: str, get_ip: callable, ip_validate: callable) -> Optional[str]:
    try:
        ip_address = get_ip()
        logging.info("Automatic {0} lookup found: {1}".format(ip_type, ip_address))
        if ip_validate(ip_address):
            return ip_address
        logging.error("Automatic {0} lookup found invalid address '{1}', update cancelled.".format(ip_type, ip_address))
    except Exception as e:
        logging.debug(e.__str__())
        logging.error("Automatic {0} lookup call failed, {0} update cancelled!".format(ip_type))
    return None


def do_sync(domains: Tuple[str, ...], apikey: str, no_ipv4: bool, ipv4: Optional[str], no_ipv6: bool, ipv6: Optional[str]) -> None:
    logging.info("Update IPV4 to: {0}".format('<disabled>' if no_ipv4 else '<automatic lookup>' if ipv4 is None else ipv4))
    if not no_ipv4 and ipv4 is None:
        ipv4 = _get_ip_address('IPV4', get_ipv4_address, IPV4_ADDRESS.validate)
    logging.info("Update IPV6 to: {0}".format('<disabled>' if no_ipv6 else '<automatic lookup>' if ipv6 is None else ipv6))
    if not no_ipv6 and ipv6 is None:
        ipv6 = _get_ip_address('IPV6', get_ipv6_address, IPV6_ADDRESS.validate)
    gandi_api = GandiAPI(apikey)
    for domain in domains:
        logging.info("Updating DNS for domain: {0}".format(domain))
        _sync_ip(domain, 'IPV4', ipv4, gandi_api.get_ipv4_address, gandi_api.update_ipv4_address)
        _sync_ip(domain, 'IPV6', ipv6, gandi_api.get_ipv6_address, gandi_api.update_ipv6_address)
