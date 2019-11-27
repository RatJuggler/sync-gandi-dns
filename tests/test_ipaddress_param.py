from unittest import TestCase
from click import BadParameter
from ipaddress import IPv4Address

from syncgandidns.ipaddress_param import IPv4AddressParamType


class TestIPAddressParam(TestCase):

    def setUp(self):
        self.param_type = IPv4AddressParamType()

    def test_name(self):
        self.assertEqual(self.param_type.name, "ipv4_address")

    def test_convert_type_error(self):
        with self.assertRaises(BadParameter):
            self.param_type.convert(127.001, "dummy", None)

    def test_convert_value_error(self):
        with self.assertRaises(BadParameter):
            self.param_type.convert("localhost", "dummy", None)

    def test_convert_valid(self):
        convert = self.param_type.convert("8.8.8.8", "dummy", None)
        self.assertIsInstance(convert, IPv4Address)
