import logging

from .gandi_api import get_domain_record_resource_value, update_domain_record_resource


def sync_ip_address(domain, ipv4, ipv6, apikey):
    current_ipv4 = get_domain_record_resource_value(apikey, domain, 'A')
    current_ipv6 = get_domain_record_resource_value(apikey, domain, 'AAAA')
    logging.info("Current: IPV4 = {0}, IPV6 = {1}".format(current_ipv4, current_ipv6))
    if ipv4 != current_ipv4:
        update_domain_record_resource(apikey, domain, 'A', ipv4)
    if ipv6 != current_ipv6:
        update_domain_record_resource(apikey, domain, 'AAAA', ipv6)
