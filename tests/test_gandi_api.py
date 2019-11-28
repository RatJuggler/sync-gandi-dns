import os

from ipaddress import IPv4Address, IPv6Address, AddressValueError
from requests import HTTPError
from unittest import TestCase

import syncgandidns.gandi_api as gandi_api


class TestGandiAPI(TestCase):

    def setUp(self):
        self.API_KEY = os.getenv("GANDI_API_KEY")
        self.TEST_DOMAIN = os.getenv("GANDI_TEST_DOMAIN")

    def test_get_domain_record_resource_value_unknown(self):
        with self.assertRaises(HTTPError):
            gandi_api.get_domain_record_resource_value(self.API_KEY, self.TEST_DOMAIN, 'UNKNOWN')

    def test_get_domain_record_resource_value_a(self):
        value = gandi_api.get_domain_record_resource_value(self.API_KEY, self.TEST_DOMAIN, 'A')
        try:
            return IPv4Address(value)
        except AddressValueError:
            self.fail("{0} is not a valid IPV4 address".format(value))

    def test_get_domain_record_resource_value_aaaa(self):
        value = gandi_api.get_domain_record_resource_value(self.API_KEY, self.TEST_DOMAIN, 'AAAA')
        try:
            return IPv6Address(value)
        except AddressValueError:
            self.fail("{0} is not a valid IPV6 address".format(value))
