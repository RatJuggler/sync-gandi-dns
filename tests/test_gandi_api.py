import os

from ipaddress import IPv4Address, IPv6Address, AddressValueError
from requests import HTTPError
from unittest import TestCase

from syncgandidns.gandi_api import GandiAPI


class TestGandiAPI(TestCase):

    def setUp(self):
        API_KEY = os.getenv("GANDI_API_KEY")
        TEST_DOMAIN = os.getenv("GANDI_TEST_DOMAIN")
        self.GANDI_API = GandiAPI(API_KEY, TEST_DOMAIN)

    def test_get_domain_record_resource_value_unknown(self):
        with self.assertRaises(HTTPError):
            self.GANDI_API.get_domain_record_resource_value('UNKNOWN')

    def test_get_domain_record_resource_value_a(self):
        value = self.GANDI_API.get_domain_record_resource_value('A')
        try:
            return IPv4Address(value)
        except AddressValueError:
            self.fail("{0} is not a valid IPV4 address".format(value))

    def test_get_domain_record_resource_value_aaaa(self):
        value = self.GANDI_API.get_domain_record_resource_value('AAAA')
        try:
            return IPv6Address(value)
        except AddressValueError:
            self.fail("{0} is not a valid IPV6 address".format(value))
