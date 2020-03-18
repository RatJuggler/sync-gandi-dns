from ipaddress import IPv4Address, IPv6Address, AddressValueError
from unittest import TestCase

from syncgandidns.ipify_api import get_ipv4_address, get_ipv6_address


class TestIpifyAPI(TestCase):

    def test_get_ipv4_address(self):
        value = get_ipv4_address()
        try:
            return IPv4Address(value)
        except AddressValueError:
            self.fail("{0} is not a valid IPV4 address".format(value))

    def test_get_ipv6_address(self):
        value = get_ipv6_address()
        try:
            return IPv6Address(value)
        except AddressValueError:
            self.fail("{0} is not a valid IPV6 address".format(value))
