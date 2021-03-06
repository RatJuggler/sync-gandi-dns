from unittest import TestCase
from click import BadParameter
from ipaddress import IPv4Address

from syncgandidns.ipv4address_param import IPv4AddressParamType


class TestIPv4AddressParam(TestCase):

    def setUp(self) -> None:
        self.param_type = IPv4AddressParamType()

    def test_name(self) -> None:
        self.assertEqual(self.param_type.name, "ipv4_address")

    def test_validate_valid(self) -> None:
        self.assertIsInstance(self.param_type.validate('127.0.0.1'), IPv4Address)

    def test_validate_invalid(self) -> None:
        self.assertIsNone(self.param_type.validate('127.0.0'))

    def test_convert_type_error(self) -> None:
        with self.assertRaises(BadParameter):
            self.param_type.convert(127.001, "dummy", None)

    def test_convert_value_error(self) -> None:
        with self.assertRaises(BadParameter):
            self.param_type.convert("localhost", "dummy", None)

    def test_convert_valid(self) -> None:
        convert = self.param_type.convert("8.8.8.8", "dummy", None)
        self.assertIsInstance(convert, IPv4Address)

    def test_convert_invalid(self) -> None:
        with self.assertRaises(BadParameter):
            self.param_type.convert("8.8.8", "dummy", None)
