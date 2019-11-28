import logging

from .gandi_api import GandiAPI


def sync_ip_address(domain, ipv4, ipv6, apikey):
    gandi_api = GandiAPI(apikey, domain)
    current_ipv4 = gandi_api.get_domain_record_resource_value('A')
    current_ipv6 = gandi_api.get_domain_record_resource_value('AAAA')
    logging.info("Current: IPV4 = {0}, IPV6 = {1}".format(current_ipv4, current_ipv6))
    if ipv4 != current_ipv4:
        gandi_api.update_domain_record_resource('A', ipv4)
    if ipv6 != current_ipv6:
        gandi_api.update_domain_record_resource('AAAA', ipv6)
