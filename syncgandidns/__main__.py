import click
import logging

from .configure_logging import configure_logging
from .sync_ip_address import sync_ip_address
from .ipv4address_param import IPv4AddressParamType
from .ipv6address_param import IPv6AddressParamType

IPV4_ADDRESS = IPv4AddressParamType()
IPV6_ADDRESS = IPv6AddressParamType()


@click.command(help='''
    Sync a local dynamic IP address with a Gandi DNS domain entry.\n
    DOMAIN: The domain to update the DNS for.\n
    APIKEY: Your Gandi API key.
    ''')
@click.version_option()
@click.argument('domain', nargs=1, type=click.STRING, required=True)
@click.argument('apikey', nargs=1, type=click.STRING, required=True)
@click.option('-auto-ipv4', 'autov4', default=True, is_flag=True, show_default=True,
              help='Update the domain DNS with an IPV4 address obtained automatically.')
@click.option('-ipv4', 'ipv4', type=IPV4_ADDRESS,
              help='Override the IPV4 address to update the domain DNS with.')
@click.option('-auto-ipv6', 'autov6', default=True, is_flag=True, show_default=True,
              help='Update the domain DNS with an IPV6 address obtained automatically.')
@click.option('-ipv6', 'ipv6', type=IPV6_ADDRESS,
              help='Override the IPV6 address to update the domain DNS with.')
@click.option('-l', '--log-level', 'level', type=click.Choice(['DEBUG', 'VERBOSE', 'INFO', 'WARNING']),
              help='Show additional logging information.', default='INFO', show_default=True)
def syncgandidns(domain: str, apikey: str, autov4: bool, ipv4: str, autov6: bool, ipv6: str, level: str):
    """
    Sync local dynamic IP address with Gandi DNS.
    :param domain: To sync IP address for
    :param apikey: To access the API with
    :param autov4: Automatically update
    :param ipv4: To sync to the domain DNS
    :param autov6: Automatically update
    :param ipv6: To sync to the domain DNS
    :param level: Set a logging level; DEBUG, VERBOSE, INFO or WARNING
    :return: No meaningful return
    """
    configure_logging(level)
    logging.info("Updating DNS for domain '{0}'...".format(domain))
    logging.debug("Using API key '{0}'...".format(apikey))
    logging.info("Using IPV4 '{0}'...".format('<automatic lookup>' if ipv4 is None else ipv4))
    logging.info("Using IPV6 '{0}'...".format('<automatic lookup>' if ipv6 is None else ipv6))
    sync_ip_address(domain, ipv4, ipv6, apikey)


if __name__ == '__main__':
    syncgandidns()   # pragma: no cover
