from unittest import TestCase
from click.testing import CliRunner

import syncgandidns.__main__ as main


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

    def test_invalid_ipv4_address(self):
        result = self.runner.invoke(main.syncgandidns, ['-ipv4', 'localhost'])
        self.assertEqual(result.exit_code, 2)
        self.assertIn('Error: Invalid value for "-ipv4": localhost is not a valid IP address', result.output)
