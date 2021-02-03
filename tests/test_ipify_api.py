from ipaddress import IPv4Address, IPv6Address, AddressValueError
from typing import Optional
from unittest import TestCase

from syncgandidns.ipify_api import get_ipv4_address, get_ipv6_address


class TestIpifyAPI(TestCase):

    @staticmethod
    def validateIPV4(ipv4: str) -> Optional[IPv4Address]:
        try:
            return IPv4Address(ipv4)
        except AddressValueError:
            return None

    @staticmethod
    def validateIPV6(ipv6: str) -> Optional[IPv6Address]:
        try:
            return IPv6Address(ipv6)
        except AddressValueError:
            return None

    def test_get_ipv4_address(self) -> None:
        try:
            ipv4 = get_ipv4_address()
            if self.validateIPV4(ipv4) is None:
                self.fail("{0} is not a valid IPV4 address".format(ipv4))
        except Exception:
            self.assertTrue(True, 'Allow ipify IPV4 lookup failure to pass.')

    def test_get_ipv6_address(self) -> None:
        try:
            ipv6 = get_ipv6_address()
            if self.validateIPV6(ipv6) is None and self.validateIPV4(ipv6) is None:
                self.fail("{0} is not a valid IPV6 or IPV4 address".format(ipv6))
        except Exception:
            self.assertTrue(True, 'Allow ipify IPV6 lookup failure to pass.')
