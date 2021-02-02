from typing import Optional

from testfixtures import LogCapture
from unittest import TestCase
from unittest.mock import patch, MagicMock

from syncgandidns.sync_ip_address import do_sync
import syncgandidns.configure_logging as cl

DUMMY_IPV4 = "86.144.65.49"
DUMMY_IPV6 = "2a00:23c6:290c:2700:3bf1:5e62:c213:89ce"
DUMMY_DOMAIN = "test.domain"
DUMMY_API_KEY = "secretpassword"
NO_MATCH = "nomatch"


def _log_check(log_out: LogCapture, expected1: str, expected2: str, expected3: str, expected4: str, expected5: str) -> None:
    root = 'root'
    log_level = cl.logging.getLevelName(cl.logging.INFO)
    log_out.check_present((root, log_level, expected1),
                          (root, log_level, expected2),
                          (root, log_level, expected3),
                          (root, log_level, expected4),
                          (root, log_level, expected5))


@patch('syncgandidns.gandi_api.GandiAPI.update_ipv4_address')
@patch('syncgandidns.gandi_api.GandiAPI.update_ipv6_address')
@patch('syncgandidns.gandi_api.GandiAPI.get_ipv4_address')
@patch('syncgandidns.gandi_api.GandiAPI.get_ipv6_address')
class TestSyncIPAddress(TestCase):

    def setUp(self) -> None:
        pass

    @staticmethod
    def do_sync_wrap(no_ipv4: bool, ipv4: Optional[str], no_ipv6: bool, ipv6: Optional[str]) -> LogCapture:
        with LogCapture(level=cl.logging.INFO) as log_out:
            do_sync(DUMMY_DOMAIN, DUMMY_API_KEY, no_ipv4, ipv4, no_ipv6, ipv6)
            return log_out

    def test_automatic(self,
                       get_ipv6_address_mock: MagicMock,
                       get_ipv4_address_mock: MagicMock,
                       update_ipv6_address_mock: MagicMock,
                       update_ipv4_address_mock: MagicMock) -> None:
        get_ipv4_address_mock.return_value = DUMMY_IPV4
        get_ipv6_address_mock.return_value = DUMMY_IPV6
        log_out = self.do_sync_wrap(False, None, False, None)
        self.assertEqual(1, get_ipv6_address_mock.call_count)
        self.assertEqual(1, get_ipv4_address_mock.call_count)
        self.assertEqual(1, update_ipv6_address_mock.call_count)
        self.assertEqual(1, update_ipv4_address_mock.call_count)
        _log_check(log_out,
                   "Updating DNS for domain: {0}".format(DUMMY_DOMAIN),
                   "Update IPV4 to: <automatic lookup>",
                   "Update IPV6 to: <automatic lookup>",
                   "Current IPV4: {0}".format(DUMMY_IPV4),
                   "Current IPV6: {0}".format(DUMMY_IPV6))

    def test_sync_ip_address_no_change(self,
                                       get_ipv6_address_mock: MagicMock,
                                       get_ipv4_address_mock: MagicMock,
                                       update_ipv6_address_mock: MagicMock,
                                       update_ipv4_address_mock: MagicMock) -> None:
        get_ipv6_address_mock.return_value = DUMMY_IPV6
        get_ipv4_address_mock.return_value = DUMMY_IPV4
        log_out = self.do_sync_wrap(False, DUMMY_IPV4, False, DUMMY_IPV6)
        self.assertEqual(1, get_ipv6_address_mock.call_count)
        self.assertEqual(1, get_ipv4_address_mock.call_count)
        self.assertEqual(0, update_ipv6_address_mock.call_count)
        self.assertEqual(0, update_ipv4_address_mock.call_count)
        _log_check(log_out,
                   "Updating DNS for domain: {0}".format(DUMMY_DOMAIN),
                   "Current IPV4: {0}".format(DUMMY_IPV4),
                   "IPV4 already current so not updated.",
                   "Current IPV6: {0}".format(DUMMY_IPV6),
                   "IPV6 already current so not updated.")

    def test_sync_ip_address_change_both(self,
                                         get_ipv6_address_mock: MagicMock,
                                         get_ipv4_address_mock: MagicMock,
                                         update_ipv6_address_mock: MagicMock,
                                         update_ipv4_address_mock: MagicMock) -> None:
        get_ipv6_address_mock.return_value = NO_MATCH
        get_ipv4_address_mock.return_value = NO_MATCH
        log_out = self.do_sync_wrap(False, DUMMY_IPV4, False, DUMMY_IPV6)
        self.assertEqual(1, get_ipv6_address_mock.call_count)
        self.assertEqual(1, get_ipv4_address_mock.call_count)
        self.assertEqual(1, update_ipv6_address_mock.call_count)
        self.assertEqual(1, update_ipv4_address_mock.call_count)
        _log_check(log_out,
                   "Updating DNS for domain: {0}".format(DUMMY_DOMAIN),
                   "Current IPV4: {0}".format(NO_MATCH),
                   "IPV4 updated to: {0}".format(DUMMY_IPV4),
                   "Current IPV6: {0}".format(NO_MATCH),
                   "IPV6 updated to: {0}".format(DUMMY_IPV6))

    def test_sync_ip_address_change_ipv4(self,
                                         get_ipv6_address_mock: MagicMock,
                                         get_ipv4_address_mock: MagicMock,
                                         update_ipv6_address_mock: MagicMock,
                                         update_ipv4_address_mock: MagicMock) -> None:
        get_ipv6_address_mock.return_value = DUMMY_IPV6
        get_ipv4_address_mock.return_value = NO_MATCH
        log_out = self.do_sync_wrap(False, DUMMY_IPV4, False, DUMMY_IPV6)
        self.assertEqual(1, get_ipv6_address_mock.call_count)
        self.assertEqual(1, get_ipv4_address_mock.call_count)
        self.assertEqual(0, update_ipv6_address_mock.call_count)
        self.assertEqual(1, update_ipv4_address_mock.call_count)
        _log_check(log_out,
                   "Updating DNS for domain: {0}".format(DUMMY_DOMAIN),
                   "Current IPV4: {0}".format(NO_MATCH),
                   "IPV4 updated to: {0}".format(DUMMY_IPV4),
                   "Current IPV6: {0}".format(DUMMY_IPV6),
                   "IPV6 already current so not updated.")

    def test_sync_ip_address_change_ipv6(self,
                                         get_ipv6_address_mock: MagicMock,
                                         get_ipv4_address_mock: MagicMock,
                                         update_ipv6_address_mock: MagicMock,
                                         update_ipv4_address_mock: MagicMock) -> None:
        get_ipv6_address_mock.return_value = NO_MATCH
        get_ipv4_address_mock.return_value = DUMMY_IPV4
        log_out = self.do_sync_wrap(False, DUMMY_IPV4, False, DUMMY_IPV6)
        self.assertEqual(1, get_ipv6_address_mock.call_count)
        self.assertEqual(1, get_ipv4_address_mock.call_count)
        self.assertEqual(1, update_ipv6_address_mock.call_count)
        self.assertEqual(0, update_ipv4_address_mock.call_count)
        _log_check(log_out,
                   "Updating DNS for domain: {0}".format(DUMMY_DOMAIN),
                   "Current IPV4: {0}".format(DUMMY_IPV4),
                   "IPV4 already current so not updated.",
                   "Current IPV6: {0}".format(NO_MATCH),
                   "IPV6 updated to: {0}".format(DUMMY_IPV6))

    def test_sync_ip_address_change_none(self,
                                         get_ipv6_address_mock: MagicMock,
                                         get_ipv4_address_mock: MagicMock,
                                         update_ipv6_address_mock: MagicMock,
                                         update_ipv4_address_mock: MagicMock) -> None:
        get_ipv6_address_mock.return_value = DUMMY_IPV6
        get_ipv4_address_mock.return_value = DUMMY_IPV4
        log_out = self.do_sync_wrap(True, None, True, None)
        self.assertEqual(1, get_ipv6_address_mock.call_count)
        self.assertEqual(1, get_ipv4_address_mock.call_count)
        self.assertEqual(0, update_ipv6_address_mock.call_count)
        self.assertEqual(0, update_ipv4_address_mock.call_count)
        _log_check(log_out,
                   "Updating DNS for domain: {0}".format(DUMMY_DOMAIN),
                   "Current IPV4: {0}".format(DUMMY_IPV4),
                   "New IPV4 not supplied so not updated.",
                   "Current IPV6: {0}".format(DUMMY_IPV6),
                   "New IPV6 not supplied so not updated.")
