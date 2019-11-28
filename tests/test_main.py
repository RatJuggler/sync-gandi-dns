from unittest import TestCase
from testfixtures import LogCapture
from click.testing import CliRunner

import syncgandidns.__main__ as main
import syncgandidns.configure_logging as cl


class TestBaseCommand(TestCase):

    def setUp(self):
        self.runner = CliRunner()

    def test_help(self):
        result = self.runner.invoke(main.syncgandidns, ['--help'])
        self.assertEqual(result.exit_code, 0)
        self.assertIn(" --version ", result.output)
        self.assertIn(" -ipv4 ", result.output)
        self.assertIn(" -ipv6 ", result.output)
        self.assertIn(" --log-level ", result.output)
        self.assertIn(" --help ", result.output)

    def test_version(self):
        result = self.runner.invoke(main.syncgandidns, ['--version'])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("syncgandidns, version ", result.output)

    def test_missing_domain(self):
        result = self.runner.invoke(main.syncgandidns, [])
        self.assertEqual(result.exit_code, 2)
        self.assertIn('Error: Missing argument "DOMAIN".', result.output)

    def test_missing_apikey(self):
        result = self.runner.invoke(main.syncgandidns, ['dinosaur.tea'])
        self.assertEqual(result.exit_code, 2)
        self.assertIn('Error: Missing argument "APIKEY".', result.output)

    def test_invalid_ipv4_address(self):
        result = self.runner.invoke(main.syncgandidns, ['-ipv4', 'localhost'])
        self.assertEqual(result.exit_code, 2)
        self.assertIn('Error: Invalid value for "-ipv4": localhost is not a valid IPV4 address', result.output)

    def test_invalid_ipv6_address(self):
        result = self.runner.invoke(main.syncgandidns, ['-ipv6', 'localhost'])
        self.assertEqual(result.exit_code, 2)
        self.assertIn('Error: Invalid value for "-ipv6": localhost is not a valid IPV6 address', result.output)

    def test_usage(self):
        expected = "Update DNS for 'pickle.jar' with IPV4 '192.168.0.1' and IV6 '2001:db8:85a3::8a2e:370:7334' using " \
                   "API key 'secretpassword'."
        with LogCapture(level=cl.logging.INFO) as log_out:
            result = self.runner.invoke(main.syncgandidns, ['pickle.jar',
                                                            'secretpassword',
                                                            '-ipv4', '192.168.0.1',
                                                            '-ipv6', '2001:0db8:85a3:0000:0000:8a2e:0370:7334'])
        self.assertEqual(result.exit_code, 0)
        log_out.check(("root", cl.logging.getLevelName(cl.logging.INFO), expected))
