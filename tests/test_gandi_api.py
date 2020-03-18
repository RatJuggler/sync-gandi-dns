import os

from ipaddress import IPv4Address, IPv6Address, AddressValueError
from requests import HTTPError
from unittest import TestCase

from syncgandidns.gandi_api import GandiAPI


class TestGandiAPI(TestCase):

    def setUp(self) -> None:
        api_key = os.getenv("GANDI_API_KEY")
        test_domain = os.getenv("GANDI_TEST_DOMAIN")
        self.GANDI_API = GandiAPI(api_key, test_domain)

    def test_get_domain_record_resource_value_unknown(self) -> None:
        with self.assertRaises(HTTPError):
            self.GANDI_API.get_domain_record_resource_value('UNKNOWN')

    def test_get_domain_record_resource_value_a(self) -> None:
        ipv4 = self.GANDI_API.get_domain_record_resource_value('A')
        try:
            IPv4Address(ipv4)
        except AddressValueError:
            self.fail("{0} is not a valid IPV4 address".format(ipv4))

    def test_get_domain_record_resource_value_aaaa(self) -> None:
        ipv6 = self.GANDI_API.get_domain_record_resource_value('AAAA')
        try:
            IPv6Address(ipv6)
        except AddressValueError:
            self.fail("{0} is not a valid IPV6 address".format(ipv6))
