from ipaddress import IPv4Address, IPv6Address, AddressValueError
from unittest import TestCase

from syncgandidns.ipify_api import get_ipv4_address, get_ipv6_address


class TestIpifyAPI(TestCase):

    def test_get_ipv4_address(self) -> None:
        ipv4 = get_ipv4_address()
        try:
            IPv4Address(ipv4)
        except AddressValueError:
            self.fail("{0} is not a valid IPV4 address".format(ipv4))

    def test_get_ipv6_address(self) -> None:
        ipv6 = get_ipv6_address()
        try:
            IPv6Address(ipv6)
        except AddressValueError:
            self.fail("{0} is not a valid IPV6 address".format(ipv6))
