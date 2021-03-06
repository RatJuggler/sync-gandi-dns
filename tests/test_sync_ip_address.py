from typing import Optional

from testfixtures import LogCapture
from unittest import TestCase
from unittest.mock import patch, MagicMock

from syncgandidns.sync_ip_address import sync_ip_address
import syncgandidns.configure_logging as cl

DUMMY_IPV4 = "86.144.65.49"
DUMMY_IPV6 = "2a00:23c6:290c:2700:3bf1:5e62:c213:89ce"
DUMMY_DOMAIN = "test.domain"
DUMMY_API_KEY = "secretpassword"
NO_MATCH = "nomatch"


def _log_check(log_out: LogCapture, expected1: str, expected2: str, expected3: str, expected4: str) -> None:
    root = 'root'
    log_level = cl.logging.getLevelName(cl.logging.INFO)
    log_out.check_present((root, log_level, expected1),
                          (root, log_level, expected2),
                          (root, log_level, expected3),
                          (root, log_level, expected4))


@patch('syncgandidns.gandi_api.GandiAPI.update_ipv4_address')
@patch('syncgandidns.gandi_api.GandiAPI.update_ipv6_address')
@patch('syncgandidns.gandi_api.GandiAPI.get_ipv4_address')
@patch('syncgandidns.gandi_api.GandiAPI.get_ipv6_address')
class TestSyncIPAddress(TestCase):

    def setUp(self) -> None:
        pass

    @staticmethod
    def do_sync(ipv4: Optional[str], ipv6: Optional[str]) -> LogCapture:
        with LogCapture(level=cl.logging.INFO) as log_out:
            sync_ip_address(DUMMY_DOMAIN, ipv4, ipv6, DUMMY_API_KEY)
        return log_out

    def test_sync_ip_address_no_change(self,
                                       get_ipv6_address_mock: MagicMock,
                                       get_ipv4_address_mock: MagicMock,
                                       update_ipv6_address_mock: MagicMock,
                                       update_ipv4_address_mock: MagicMock) -> None:
        get_ipv6_address_mock.return_value = DUMMY_IPV6
        get_ipv4_address_mock.return_value = DUMMY_IPV4
        log_out = self.do_sync(DUMMY_IPV4, DUMMY_IPV6)
        self.assertEqual(1, get_ipv6_address_mock.call_count)
        self.assertEqual(1, get_ipv4_address_mock.call_count)
        self.assertEqual(0, update_ipv6_address_mock.call_count)
        self.assertEqual(0, update_ipv4_address_mock.call_count)
        _log_check(log_out,
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
        log_out = self.do_sync(DUMMY_IPV4, DUMMY_IPV6)
        self.assertEqual(1, get_ipv6_address_mock.call_count)
        self.assertEqual(1, get_ipv4_address_mock.call_count)
        self.assertEqual(1, update_ipv6_address_mock.call_count)
        self.assertEqual(1, update_ipv4_address_mock.call_count)
        _log_check(log_out,
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
        log_out = self.do_sync(DUMMY_IPV4, DUMMY_IPV6)
        self.assertEqual(1, get_ipv6_address_mock.call_count)
        self.assertEqual(1, get_ipv4_address_mock.call_count)
        self.assertEqual(0, update_ipv6_address_mock.call_count)
        self.assertEqual(1, update_ipv4_address_mock.call_count)
        _log_check(log_out,
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
        log_out = self.do_sync(DUMMY_IPV4, DUMMY_IPV6)
        self.assertEqual(1, get_ipv6_address_mock.call_count)
        self.assertEqual(1, get_ipv4_address_mock.call_count)
        self.assertEqual(1, update_ipv6_address_mock.call_count)
        self.assertEqual(0, update_ipv4_address_mock.call_count)
        _log_check(log_out,
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
        log_out = self.do_sync(None, None)
        self.assertEqual(1, get_ipv6_address_mock.call_count)
        self.assertEqual(1, get_ipv4_address_mock.call_count)
        self.assertEqual(0, update_ipv6_address_mock.call_count)
        self.assertEqual(0, update_ipv4_address_mock.call_count)
        _log_check(log_out,
                   "Current IPV4: {0}".format(DUMMY_IPV4),
                   "New IPV4 not supplied so not updated.",
                   "Current IPV6: {0}".format(DUMMY_IPV6),
                   "New IPV6 not supplied so not updated.")
