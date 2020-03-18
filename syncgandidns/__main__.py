import click
import logging

from .ipify_api import get_ipv4_address, get_ipv6_address
from .configure_logging import configure_logging
from .sync_ip_address import sync_ip_address
from .ipv4address_param import IPv4AddressParamType
from .ipv6address_param import IPv6AddressParamType

IPV4_ADDRESS = IPv4AddressParamType()
IPV6_ADDRESS = IPv6AddressParamType()


@click.command(help='''
    Sync a dynamic IP address (V4 & V6) with a Gandi DNS domain entry.\n
    The external IP address is determined automatically.\n 
    DOMAIN: The domain to update the DNS for.\n
    APIKEY: Your Gandi API key.
    ''')
@click.version_option()
@click.argument('domain', nargs=1, type=click.STRING, required=True)
@click.argument('apikey', nargs=1, type=click.STRING, required=True)
@click.option('-ipv4', 'ipv4', type=IPV4_ADDRESS,
              help='Override the IPV4 address to update the domain DNS with.')
@click.option('-ipv6', 'ipv6', type=IPV6_ADDRESS,
              help='Override the IPV6 address to update the domain DNS with.')
@click.option('-l', '--log-level', 'level', type=click.Choice(['DEBUG', 'VERBOSE', 'INFO', 'WARNING']),
              help='Show additional logging information.', default='INFO', show_default=True)
def syncgandidns(domain: str, apikey: str, ipv4: str, ipv6: str, level: str) -> None:
    """
    Sync local dynamic IP address with Gandi DNS.
    :param domain: To sync IP address for
    :param apikey: To access the API with
    :param ipv4: To sync to the domain DNS
    :param ipv6: To sync to the domain DNS
    :param level: Set a logging level; DEBUG, VERBOSE, INFO or WARNING
    :return: No meaningful return
    """
    configure_logging(level)
    logging.info("Updating DNS for domain: {0}".format(domain))
    logging.debug("Using API key: {0}".format(apikey))
    logging.info("Using IPV4: {0}".format('<automatic lookup>' if ipv4 is None else ipv4))
    if ipv4 is None:
        ipv4 = get_ipv4_address()
        logging.info("...found: {0}".format(ipv4))
    logging.info("Using IPV6: {0}".format('<automatic lookup>' if ipv6 is None else ipv6))
    if ipv6 is None:
        ipv6 = get_ipv6_address()
        logging.info("...found: {0}".format(ipv6))
    sync_ip_address(domain, ipv4, ipv6, apikey)


if __name__ == '__main__':
    syncgandidns()   # pragma: no cover
