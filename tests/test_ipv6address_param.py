from unittest import TestCase
from click import BadParameter
from ipaddress import IPv6Address

from syncgandidns.ipv6address_param import IPv6AddressParamType


class TestIPv6AddressParam(TestCase):

    def setUp(self) -> None:
        self.param_type = IPv6AddressParamType()

    def test_name(self) -> None:
        self.assertEqual(self.param_type.name, "ipv6_address")

    def test_validate_valid(self) -> None:
        self.assertIsInstance(self.param_type.validate('2a00:23c6:2915:1a00:f003:ebc4:a042:3526'), IPv6Address)

    def test_validate_invalid(self) -> None:
        self.assertIsNone(self.param_type.validate('2a00:23c6:2915:1a00:f003:ebc4'))

    def test_convert_type_error(self) -> None:
        with self.assertRaises(BadParameter):
            self.param_type.convert(1450.4009, "dummy", None)

    def test_convert_value_error(self) -> None:
        with self.assertRaises(BadParameter):
            self.param_type.convert("localhost", "dummy", None)

    def test_convert_valid(self) -> None:
        convert = self.param_type.convert("2a00:1450:4009:80f::2003", "dummy", None)
        self.assertIsInstance(convert, IPv6Address)

    def test_convert_invalid(self) -> None:
        with self.assertRaises(BadParameter):
            self.param_type.convert("2a00:1450:4009:80f", "dummy", None)
