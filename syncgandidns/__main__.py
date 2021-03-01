import click
import logging

from environs import Env
from typing import Optional, Tuple

from .domain_param import DOMAIN
from .ipv4address_param import IPV4_ADDRESS
from .ipv6address_param import IPV6_ADDRESS
from .url_param import URL
from .configure_logging import configure_logging
from .gandi_api import GandiAPI
from .sync_ip_address import do_sync


# Check for an environment variable file before setting up Click.
env = Env()
env.read_env('sync-gandi-dns.env')
ENVVAR_GANDI_DOMAINS = 'GANDI_DOMAINS'
ENVVAR_GANDI_APIKEY = 'GANDI_APIKEY'


def test_access(domains: Tuple[str, ...], apikey: str) -> None:
    gandi_api = GandiAPI(apikey)
    for domain in domains:
        logging.info("Testing access to DNS records for domain: {0}".format(domain))
        dns_records = gandi_api.get_domain_records(domain)
        logging.info("{0} DNS Records retrieved!".format(len(dns_records)))


@click.command(help='''
    Sync a dynamic IP address (V4 & V6) with a Gandi DNS domain entry.\n
    The external IP address is determined automatically by default.\n
    Domains can be set using the GANDI_DOMAINS environment variable. For multiple domains separate with a ';'.\n
    The Gandi API key can be set using the GANDI_APIKEY environment variable.
    ''')
@click.version_option()
@click.option('-d', '--domain', 'domains', type=DOMAIN, required=True, multiple=True, envvar=ENVVAR_GANDI_DOMAINS,
              help='A domain to update the DNS for. Repeat the option to update multiple domains.',
              default=lambda: env(ENVVAR_GANDI_DOMAINS, None))
@click.option('-a', '--apikey', 'apikey', type=click.STRING, required=True, envvar=ENVVAR_GANDI_APIKEY,
              help='Your Gandi API key.', default=lambda: env(ENVVAR_GANDI_APIKEY, None))
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
@click.option('-m', '--metrics', 'metrics', type=URL,
              help="Push metrics to this URL.")
@click.option('-t', '--test', 'test', default=False, is_flag=True,
              help="Test the Gandi API key and exit.", show_default=True)
def syncgandidns(domains: Tuple[str, ...], apikey: str, ipv4: Optional[str], no_ipv4: bool, ipv6: Optional[str], no_ipv6: bool,
                 level: Optional[str], metrics: Optional[str], test: bool) -> None:
    """
    Sync local dynamic IP address with Gandi DNS.
    :param domains: To sync the IP address for
    :param apikey: To access the API with
    :param ipv4: To sync to the domain DNS
    :param no_ipv4: Don't update IPV4
    :param ipv6: To sync to the domain DNS
    :param no_ipv6: Don't update IPV6
    :param level: Set a logging level; DEBUG, VERBOSE, INFO or WARNING
    :param metrics: Push metrics to the given URL
    :param test: Test access to a domains records
    :return: No meaningful return
    """
    configure_logging(level)
    logging.debug("Using API key: {0}".format(apikey))
    if test:
        test_access(domains, apikey)
    else:
        do_sync(domains, apikey, no_ipv4, ipv4, no_ipv6, ipv6, metrics)


if __name__ == '__main__':
    syncgandidns()   # pragma: no cover
