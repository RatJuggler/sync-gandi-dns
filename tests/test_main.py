from ipaddress import IPv4Address, AddressValueError, IPv6Address
from unittest import TestCase
from unittest.mock import patch, MagicMock
from testfixtures import LogCapture
from click.testing import CliRunner

import syncgandidns.__main__ as main
import syncgandidns.configure_logging as cl


def _init_log_check(log_out: LogCapture, expected1: str, expected2: str, expected3: str) -> None:
    root = 'root'
    log_level = cl.logging.getLevelName(cl.logging.INFO)
    log_out.check_present((root, log_level, expected1),
                          (root, log_level, expected2),
                          (root, log_level, expected3))


class TestBaseCommand(TestCase):

    def setUp(self) -> None:
        self.runner = CliRunner()

    def test_help(self) -> None:
        result = self.runner.invoke(main.syncgandidns, ['--help'])
        self.assertEqual(result.exit_code, 0)
        self.assertIn(" --version ", result.output)
        self.assertIn(" -ipv4 ", result.output)
        self.assertIn(" -ipv6 ", result.output)
        self.assertIn(" --log-level ", result.output)
        self.assertIn(" --help ", result.output)

    def test_version(self) -> None:
        result = self.runner.invoke(main.syncgandidns, ['--version'])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("syncgandidns, version ", result.output)

    def test_missing_domain(self) -> None:
        result = self.runner.invoke(main.syncgandidns, [])
        self.assertEqual(result.exit_code, 2)
        self.assertIn('Error: Missing argument \'DOMAIN\'.', result.output)

    def test_missing_apikey(self) -> None:
        result = self.runner.invoke(main.syncgandidns, ['dinosaur.tea'])
        self.assertEqual(result.exit_code, 2)
        self.assertIn('Error: Missing argument \'APIKEY\'.', result.output)

    def test_invalid_ipv4_address(self) -> None:
        result = self.runner.invoke(main.syncgandidns, ['-ipv4', 'localhost'])
        self.assertEqual(result.exit_code, 2)
        self.assertIn('Error: Invalid value for \'-ipv4\': localhost is not a valid IPV4 address', result.output)

    def test_invalid_ipv6_address(self) -> None:
        result = self.runner.invoke(main.syncgandidns, ['-ipv6', 'localhost'])
        self.assertEqual(result.exit_code, 2)
        self.assertIn('Error: Invalid value for \'-ipv6\': localhost is not a valid IPV6 address', result.output)

    def _found_check(self, msg: str) -> str:
        found = '...found:'
        self.assertTrue((msg.startswith(found)))
        return msg[len(found) + 1:]

    def _found_ipv4_check(self, msg: str) -> None:
        ipv4 = self._found_check(msg)
        try:
            IPv4Address(ipv4)
        except AddressValueError:
            self.fail("{0} is not a valid IPV4 address".format(ipv4))

    def _found_ipv6_check(self, msg: str) -> None:
        ipv6 = self._found_check(msg)
        try:
            IPv6Address(ipv6)
        except AddressValueError:
            self.fail("{0} is not a valid IPV6 address".format(ipv6))

    @patch('syncgandidns.__main__.sync_ip_address')
    def test_automatic(self, sync_ip_address_mock: MagicMock) -> None:
        with LogCapture(level=cl.logging.INFO) as log_out:
            result = self.runner.invoke(main.syncgandidns, ['pickle.jar',
                                                            'secretpassword'])
        self.assertEqual(result.exit_code, 0)
        _init_log_check(log_out,
                        "Updating DNS for domain: pickle.jar",
                        "Update IPV4 to: <automatic lookup>",
                        "Update IPV6 to: <automatic lookup>")
        self._found_ipv4_check(log_out.records[2].msg)
        self._found_ipv6_check(log_out.records[4].msg)
        sync_ip_address_mock.assert_called_once()

    @patch('syncgandidns.__main__.sync_ip_address')
    def test_override_both(self, sync_ip_address_mock: MagicMock) -> None:
        with LogCapture(level=cl.logging.INFO) as log_out:
            result = self.runner.invoke(main.syncgandidns, ['pickle.jar',
                                                            'secretpassword',
                                                            '-ipv4', '192.168.0.1',
                                                            '-ipv6', '2001:0db8:85a3:0000:0000:8a2e:0370:7334'])
        self.assertEqual(result.exit_code, 0)
        _init_log_check(log_out,
                        "Updating DNS for domain: pickle.jar",
                        "Update IPV4 to: 192.168.0.1",
                        "Update IPV6 to: 2001:db8:85a3::8a2e:370:7334")
        sync_ip_address_mock.assert_called_once()

    @patch('syncgandidns.__main__.sync_ip_address')
    def test_debug_log(self, sync_ip_address_mock: MagicMock) -> None:
        with LogCapture(level=cl.logging.DEBUG) as log_out:
            result = self.runner.invoke(main.syncgandidns, ['jam.jar',
                                                            'secretpassword',
                                                            '-ipv6', '2701:db8:86a3::8a3e:371:7734'])
        self.assertEqual(result.exit_code, 0)
        _init_log_check(log_out,
                        "Updating DNS for domain: jam.jar",
                        "Update IPV4 to: <automatic lookup>",
                        "Update IPV6 to: 2701:db8:86a3::8a3e:371:7734")
        log_out.check_present(('root', cl.logging.getLevelName(cl.logging.DEBUG), "Using API key: secretpassword"))
        self._found_ipv4_check(log_out.records[6].msg)
        sync_ip_address_mock.assert_called_once()
