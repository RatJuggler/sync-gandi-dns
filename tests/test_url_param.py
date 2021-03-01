from unittest import TestCase
from click import BadParameter

from syncgandidns.url_param import UrlParamType


class TestUrlParam(TestCase):

    def setUp(self) -> None:
        self.param_type = UrlParamType()

    def test_name(self) -> None:
        self.assertEqual(self.param_type.name, "url")

    def test_validate_valid_url(self) -> None:
        self.assertIsInstance(self.param_type.validate("http://test.com"), str)

    def test_validate_invalid_url(self) -> None:
        self.assertIsNone(self.param_type.validate("test"))

    def test_validate_valid_ip(self) -> None:
        self.assertIsInstance(self.param_type.validate("http://192.168.1.3:9091"), str)

    def test_validate_invalid_ip(self) -> None:
        self.assertIsNone(self.param_type.validate("ftp://127.0.0.1"))

    def test_convert_type_error(self) -> None:
        with self.assertRaises(BadParameter):
            self.param_type.convert(127.001, "dummy", None)

    def test_convert_value_error(self) -> None:
        with self.assertRaises(BadParameter):
            self.param_type.convert("http://8430", "dummy", None)

    def test_convert_valid(self) -> None:
        convert = self.param_type.convert("https://python.com", "dummy", None)
        self.assertIsInstance(convert, str)

    def test_convert_invalid(self) -> None:
        with self.assertRaises(BadParameter):
            self.param_type.convert("8.8.8", "dummy", None)
