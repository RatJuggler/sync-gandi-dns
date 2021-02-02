import click
import logging

from .configure_logging import configure_logging
from .sync_ip_address import do_sync
from .ipv4address_param import IPV4_ADDRESS
from .ipv6address_param import IPV6_ADDRESS


@click.command(help='''
    Sync a dynamic IP address (V4 & V6) with a Gandi DNS domain entry.\n
    The external IP address is determined automatically by default.
    ''')
@click.version_option()
@click.option('-d', '--domain', 'domain', type=click.STRING, required=True, envvar='GANDI_DOMAIN',
              help='The domain to update the DNS for.')
@click.option('-a', '--apikey', 'apikey', type=click.STRING, required=True, envvar='GANDI_APIKEY',
              help='Your Gandi API key. Taken from environment variable GANDI_APIKEY if present.')
@click.option('-no-ipv6', '--no-ipv6-update', 'no_ipv6', is_flag=True,
              help='Don\'t update the IPV6 address, will override \'-ipv6\'.')
@click.option('-ipv4', '--ipv4-address', 'ipv4', type=IPV4_ADDRESS,
              help='Override the IPV4 address to update the domain DNS with.')
@click.option('-ipv6', '--ipv6-address', 'ipv6', type=IPV6_ADDRESS,
              help='Override the IPV6 address to update the domain DNS with.')
@click.option('-l', '--log-level', 'level', type=click.Choice(['DEBUG', 'VERBOSE', 'INFO', 'WARNING']),
              help='Show additional logging information.', default='INFO', show_default=True)
def syncgandidns(domain: str, apikey: str, no_ipv6: bool, ipv4: str, ipv6: str, level: str) -> None:
    """
    Sync local dynamic IP address with Gandi DNS.
    :param domain: To sync IP address for
    :param apikey: To access the API with
    :param no_ipv6: Don't update IPV6
    :param ipv4: To sync to the domain DNS
    :param ipv6: To sync to the domain DNS
    :param level: Set a logging level; DEBUG, VERBOSE, INFO or WARNING
    :return: No meaningful return
    """
    configure_logging(level)
    logging.debug("Using API key: {0}".format(apikey))
    do_sync(domain, apikey, no_ipv6, ipv4, ipv6)


if __name__ == '__main__':
    syncgandidns()   # pragma: no cover
