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


class TestMain(TestCase):

    def setUp(self) -> None:
        self.runner = CliRunner()

    def test_help(self) -> None:
        result = self.runner.invoke(main.syncgandidns, ['--help'])
        self.assertEqual(result.exit_code, 0)
        self.assertIn(" --version ", result.output)
        self.assertIn(" -d, --domain ", result.output)
        self.assertIn(" -a, --apikey ", result.output)
        self.assertIn(" -no-ipv6, --no-ipv6-update ", result.output)
        self.assertIn(" -ipv4, --ipv4-address ", result.output)
        self.assertIn(" -ipv6, --ipv6-address ", result.output)
        self.assertIn(" -l, --log-level ", result.output)
        self.assertIn(" --help ", result.output)

    # TODO: Requires "python3 setup.py sdist" to have been run to pass, review.
    def test_version(self) -> None:
        result = self.runner.invoke(main.syncgandidns, ['--version'])
        self.assertEqual(0, result.exit_code)
        self.assertIn("syncgandidns, version ", result.output)

    def test_missing_domain(self) -> None:
        result = self.runner.invoke(main.syncgandidns, ['-a', 'secretpassword'])
        self.assertEqual(2, result.exit_code)
        self.assertIn('Error: Missing option \'-d\' / \'--domain\'.', result.output)

    def test_missing_apikey(self) -> None:
        result = self.runner.invoke(main.syncgandidns, ['-d', 'dinosaur.tea'])
        self.assertEqual(2, result.exit_code)
        self.assertIn('Error: Missing option \'-a\' / \'--apikey\'.', result.output)

    def test_invalid_ipv4_address(self) -> None:
        result = self.runner.invoke(main.syncgandidns, ['-ipv4', 'localhost'])
        self.assertEqual(2, result.exit_code)
        self.assertIn('Error: Invalid value for \'-ipv4\' / \'--ipv4-address\': localhost is not a valid IPV4 address',
                      result.output)

    def test_invalid_ipv6_address(self) -> None:
        result = self.runner.invoke(main.syncgandidns, ['-ipv6', 'localhost'])
        self.assertEqual(2, result.exit_code)
        self.assertIn('Error: Invalid value for \'-ipv6\' / \'--ipv6-address\': localhost is not a valid IPV6 address',
                      result.output)

    def _found_check(self, msg: str) -> str:
        found = '...found:'
        self.assertTrue((msg.startswith(found)))
        return msg[len(found) + 1:]

    def _found_ipv4_check(self, msg: str, ipv4: str) -> None:
        ipv4_found = self._found_check(msg)
        self.assertEqual(ipv4_found, ipv4)

    def _found_ipv6_check(self, msg: str, ipv6: str) -> None:
        ipv6_found = self._found_check(msg)
        self.assertEqual(ipv6_found, ipv6)

    @patch('syncgandidns.__main__.get_ipv4_address')
    @patch('syncgandidns.__main__.get_ipv6_address')
    @patch('syncgandidns.__main__.sync_ip_address')
    def test_automatic(self,
                       sync_ip_address_mock: MagicMock,
                       get_ipv6_address_mock: MagicMock,
                       get_ipv4_address_mock: MagicMock) -> None:
        get_ipv4_address_mock.return_value = "127.0.0.1"
        get_ipv6_address_mock.return_value = "0001:0002:0003:0004:0005:0006:0007:0008"
        with LogCapture(level=cl.logging.INFO) as log_out:
            result = self.runner.invoke(main.syncgandidns, ['-d', 'pickle.jar',
                                                            '-a', 'secretpassword'])
        self.assertEqual(0, result.exit_code)
        _init_log_check(log_out,
                        "Updating DNS for domain: pickle.jar",
                        "Update IPV4 to: <automatic lookup>",
                        "Update IPV6 to: <automatic lookup>")
        self._found_ipv4_check(log_out.records[2].msg, get_ipv4_address_mock.return_value)
        self._found_ipv6_check(log_out.records[4].msg, get_ipv6_address_mock.return_value)
        sync_ip_address_mock.assert_called_once()

    @patch('syncgandidns.__main__.sync_ip_address')
    def test_override_both(self, sync_ip_address_mock: MagicMock) -> None:
        with LogCapture(level=cl.logging.INFO) as log_out:
            result = self.runner.invoke(main.syncgandidns, ['-d', 'pickle.jar',
                                                            '-a', 'secretpassword',
                                                            '-ipv4', '192.168.0.1',
                                                            '-ipv6', '2001:0db8:85a3:0000:0000:8a2e:0370:7334'])
        self.assertEqual(0, result.exit_code)
        _init_log_check(log_out,
                        "Updating DNS for domain: pickle.jar",
                        "Update IPV4 to: 192.168.0.1",
                        "Update IPV6 to: 2001:db8:85a3::8a2e:370:7334")
        sync_ip_address_mock.assert_called_once()

    @patch('syncgandidns.__main__.get_ipv4_address')
    @patch('syncgandidns.__main__.sync_ip_address')
    def test_debug_log(self,
                       sync_ip_address_mock: MagicMock,
                       get_ipv4_address_mock: MagicMock) -> None:
        get_ipv4_address_mock.return_value = "127.0.0.1"
        with LogCapture(level=cl.logging.DEBUG) as log_out:
            result = self.runner.invoke(main.syncgandidns, ['-d', 'jam.jar',
                                                            '-a', 'secretpassword',
                                                            '-ipv6', '2701:db8:86a3::8a3e:371:7734'])
        self.assertEqual(0, result.exit_code)
        _init_log_check(log_out,
                        "Updating DNS for domain: jam.jar",
                        "Update IPV4 to: <automatic lookup>",
                        "Update IPV6 to: 2701:db8:86a3::8a3e:371:7734")
        log_out.check_present(('root', cl.logging.getLevelName(cl.logging.DEBUG), "Using API key: secretpassword"))
        self._found_ipv4_check(log_out.records[3].msg, get_ipv4_address_mock.return_value)
        sync_ip_address_mock.assert_called_once()
