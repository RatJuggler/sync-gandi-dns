import logging
from typing import Optional, Tuple
from prometheus_client import CollectorRegistry, Gauge, push_to_gateway

from .ipv4address_param import IPV4_ADDRESS
from .ipv6address_param import IPV6_ADDRESS
from .ipify_api import get_ipv4_address, get_ipv6_address
from .gandi_api import GandiAPI


def _sync_ip(domain: str, ip_type: str, new_ip: Optional[str], get_ip: callable, update_ip: callable) -> None:
    current_ip = get_ip(domain)
    logging.info("{0} current {1} address: {2}".format(domain, ip_type, current_ip))
    if new_ip is None:
        logging.info("{0} {1} address not updated, new address not supplied!".format(domain, ip_type))
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


def _get_update_ip(ip_type: str, no_ip: bool, ip: Optional[str], get_ip: callable, ip_validate: callable):
    logging.info("Update {0} to: {1}".format(ip_type, '<disabled>' if no_ip else '<automatic lookup>' if ip is None else ip))
    if no_ip:
        return None
    if ip is None:
        return _get_ip_address(ip_type, get_ip, ip_validate)
    return ip


def do_sync(domains: Tuple[str, ...], apikey: str, no_ipv4: bool, ipv4: Optional[str], no_ipv6: bool, ipv6: Optional[str],
            metrics: Optional[str]) -> None:
    success = Gauge("do_sync_last_success", "Last time the sync-gandi-dns job ran successfully.")
    failure = Gauge("do_sync_last_failure", "Last time the sync-gandi-dns job failed.")
    duration = Gauge("do_sync_duration", "The duration of the sync-gandi-dns job.")
    processed = Gauge("do_sync_processed", "The domains processed.", ["domain"])

    registry = CollectorRegistry()
    registry.register(success)
    registry.register(duration)
    registry.register(processed)

    try:
        with duration.time():
            update_ipv4 = _get_update_ip('IPV4', no_ipv4, ipv4, get_ipv4_address, IPV4_ADDRESS.validate)
            update_ipv6 = _get_update_ip('IPV6', no_ipv6, ipv6, get_ipv6_address, IPV6_ADDRESS.validate)
            gandi_api = GandiAPI(apikey)
            for domain in domains:
                logging.info("Updating DNS for domain: {0}".format(domain))
                _sync_ip(domain, 'IPV4', update_ipv4, gandi_api.get_ipv4_address, gandi_api.update_ipv4_address)
                _sync_ip(domain, 'IPV6', update_ipv6, gandi_api.get_ipv6_address, gandi_api.update_ipv6_address)
                processed.labels(domain).inc()
        success.set_to_current_time()
    except:
        failure.set_to_current_time()
        raise
    finally:
        if metrics:
            logging.info("Pushing metrics to: {0}".format(metrics))
            push_to_gateway(metrics, job='sync-gandi-dns', registry=registry)

    logging.info("sync-gandi-dns completed normally.")
