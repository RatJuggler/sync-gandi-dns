import click
import logging

from .configure_logging import configure_logging
from .ipv4address_param import IPv4AddressParamType
from .ipv6address_param import IPv6AddressParamType

IPV4_ADDRESS = IPv4AddressParamType()
IPV6_ADDRESS = IPv6AddressParamType()


@click.command(help="""
    Sync local dynamic IP address with Gandi DNS.
    """)
@click.version_option()
@click.argument('domain', nargs=1, type=click.STRING, required=True)
@click.option('-ipv4', 'ipv4', type=IPV4_ADDRESS, show_default=True,
              help="The IPV4 address to update the domain DNS with.")
@click.option('-ipv6', 'ipv6', type=IPV6_ADDRESS, show_default=True,
              help="The IPV6 address to update the domain DNS with.")
@click.option('-l', '--log-level', 'level', type=click.Choice(["DEBUG", "VERBOSE", "INFO", "WARNING"]),
              help="Show additional logging information.", default="INFO", show_default=True)
def syncgandidns(domain: str, ipv4: str, ipv6: str, level: str):
    """
    Sync local dynamic IP address with Gandi DNS.
    :param domain: To sync IP address for.
    :param ipv4: To sync to the domain DNS.
    :param ipv6: To sync to the domain DNS.
    :param level: Set a logging level; DEBUG, VERBOSE, INFO or WARNING
    :return: No meaningful return
    """
    configure_logging(level)
    logging.info("Update DNS for '{0}' with IPV4 '{1}' and IV6 '{2}'.".format(domain, ipv4, ipv6))


if __name__ == '__main__':
    syncgandidns()   # pragma: no cover
