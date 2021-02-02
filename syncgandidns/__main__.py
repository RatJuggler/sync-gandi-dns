import click
import logging

from .ipv4address_param import IPV4_ADDRESS
from .ipv6address_param import IPV6_ADDRESS
from .configure_logging import configure_logging
from .gandi_api import GandiAPI
from .sync_ip_address import do_sync


def test_access(domain: str, apikey: str) -> None:
    logging.info("Testing access to DNS records for domain: {0}".format(domain))
    gandi_api = GandiAPI(apikey)
    dns_records = gandi_api.get_domain_records(domain)
    logging.info("DNS Records retrieved:")
    logging.info(dns_records)


@click.command(help='''
    Sync a dynamic IP address (V4 & V6) with a Gandi DNS domain entry.\n
    The external IP address is determined automatically by default.
    ''')
@click.version_option()
@click.option('-d', '--domain', 'domain', type=click.STRING, required=True, envvar='GANDI_DOMAIN',
              help='The domain to update the DNS for. Taken from environment variable GANDI_DOMAIN if not supplied.')
@click.option('-a', '--apikey', 'apikey', type=click.STRING, required=True, envvar='GANDI_APIKEY',
              help='Your Gandi API key. Taken from environment variable GANDI_APIKEY if not supplied.')
@click.option('-ipv4', '--ipv4-address', 'ipv4', type=IPV4_ADDRESS,
              help='Override the IPV4 address to update the domain DNS with.')
@click.option('-no-ipv4', '--no-ipv4-update', 'no_ipv4', is_flag=True,
              help='Don\'t update the IPV4 address, will override \'-ipv4\'.')
@click.option('-ipv6', '--ipv6-address', 'ipv6', type=IPV6_ADDRESS,
              help='Override the IPV6 address to update the domain DNS with.')
@click.option('-no-ipv6', '--no-ipv6-update', 'no_ipv6', is_flag=True,
              help='Don\'t update the IPV6 address, will override \'-ipv6\'.')
@click.option('-l', '--log-level', 'level', type=click.Choice(['DEBUG', 'VERBOSE', 'INFO', 'WARNING']),
              help='Show additional logging information.', default='INFO', show_default=True)
@click.option('-t', '--test', 'test', default=False, is_flag=True,
              help="Test the Gandi API key and exit.", show_default=True)
def syncgandidns(domain: str, apikey: str, ipv4: str, no_ipv4: bool, ipv6: str, no_ipv6: bool, level: str, test: bool) -> None:
    """
    Sync local dynamic IP address with Gandi DNS.
    :param domain: To sync IP address for
    :param apikey: To access the API with
    :param ipv4: To sync to the domain DNS
    :param no_ipv4: Don't update IPV4
    :param ipv6: To sync to the domain DNS
    :param no_ipv6: Don't update IPV6
    :param level: Set a logging level; DEBUG, VERBOSE, INFO or WARNING
    :param test: Test access to a domains records
    :return: No meaningful return
    """
    configure_logging(level)
    logging.debug("Using API key: {0}".format(apikey))
    if test:
        test_access(domain, apikey)
    else:
        do_sync(domain, apikey, no_ipv4, ipv4, no_ipv6, ipv6)


if __name__ == '__main__':
    syncgandidns()   # pragma: no cover
