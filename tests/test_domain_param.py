from unittest import TestCase
from click import BadParameter

from syncgandidns.domain_param import DomainParamType


class TestIPv4AddressParam(TestCase):

    def setUp(self) -> None:
        self.param_type = DomainParamType()

    def test_name(self) -> None:
        self.assertEqual(self.param_type.name, "domain")

    def test_validate_valid(self) -> None:
        self.assertIsInstance(self.param_type.validate('test.com'), str)

    def test_validate_invalid(self) -> None:
        self.assertIsNone(self.param_type.validate('test'))

    def test_convert_type_error(self) -> None:
        with self.assertRaises(BadParameter):
            self.param_type.convert(127.001, "dummy", None)

    def test_convert_value_error(self) -> None:
        with self.assertRaises(BadParameter):
            self.param_type.convert("localhost", "dummy", None)

    def test_convert_valid(self) -> None:
        convert = self.param_type.convert("python.com", "dummy", None)
        self.assertIsInstance(convert, str)

    def test_convert_invalid(self) -> None:
        with self.assertRaises(BadParameter):
            self.param_type.convert("8.8.8", "dummy", None)
