import os

from ipaddress import IPv4Address, IPv6Address, AddressValueError
from requests import HTTPError
from unittest import TestCase

from syncgandidns.gandi_api import GandiAPI


class TestGandiAPI(TestCase):

    def setUp(self) -> None:
        api_key = os.getenv("GANDI_TEST_APIKEY")
        self._gandi_api = GandiAPI(api_key)
        self._test_domain = os.getenv("GANDI_TEST_DOMAIN")

    def test_get_update(self) -> None:
        expected = '{"rrset_type": "RESOURCE", "rrset_values": ["VALUE"]}'
        update = self._gandi_api._get_update("RESOURCE", "VALUE")
        self.assertEqual(expected, update)

    def test_get_domain_record_resource_value_unknown(self) -> None:
        with self.assertRaises(HTTPError):
            self._gandi_api._get_domain_record_resource_value(self._test_domain, 'UNKNOWN')

    def test_get_ipv4_address(self) -> None:
        ipv4 = self._gandi_api.get_ipv4_address(self._test_domain)
        try:
            IPv4Address(ipv4)
        except AddressValueError:
            self.fail("{0} is not a valid IPV4 address".format(ipv4))

    def test_get_ipv6_address(self) -> None:
        ipv6 = self._gandi_api.get_ipv6_address(self._test_domain)
        try:
            IPv6Address(ipv6)
        except AddressValueError:
            self.fail("{0} is not a valid IPV6 address".format(ipv6))
