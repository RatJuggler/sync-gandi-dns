from unittest import TestCase
from click.testing import CliRunner

from testfixtures import LogCapture
from unittest.mock import patch, MagicMock

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
        self.assertIn(" -t, --test ", result.output)
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

    @patch('syncgandidns.__main__.GandiAPI')
    def test_test(self,
                  gandi_api_mock: MagicMock) -> None:
        gandi_api_mock.return_value.get_domain_records.return_value = '<Test DNS records output>'
        with LogCapture(level=cl.logging.INFO) as log_out:
            result = self.runner.invoke(main.syncgandidns, ['-d', 'pickle.jar',
                                                            '-a', 'secretpassword',
                                                            '-t'])
        self.assertEqual(0, result.exit_code)
        _init_log_check(log_out,
                        'Testing access to DNS records for domain: pickle.jar',
                        'DNS Records retrieved:',
                        '<Test DNS records output>')
        gandi_api_mock.assert_called_once()
