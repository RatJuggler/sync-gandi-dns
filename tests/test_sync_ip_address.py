from typing import Optional

from testfixtures import LogCapture
from unittest import TestCase
from unittest.mock import patch, MagicMock

from syncgandidns.sync_ip_address import do_sync
import syncgandidns.configure_logging as cl


def _log_check(log_out: LogCapture, *expects: str) -> None:
    root = 'root'
    log_level = cl.logging.getLevelName(cl.logging.INFO)
    for expected in expects:
        log_out.check_present((root, log_level, expected))


@patch('syncgandidns.gandi_api.GandiAPI.update_ipv4_address')
@patch('syncgandidns.gandi_api.GandiAPI.update_ipv6_address')
@patch('syncgandidns.gandi_api.GandiAPI.get_ipv4_address')
@patch('syncgandidns.gandi_api.GandiAPI.get_ipv6_address')
class TestSyncIPAddress(TestCase):

    def setUp(self) -> None:
        self.DUMMY_IPV4 = "86.144.65.49"
        self.DUMMY_IPV6 = "2a00:23c6:290c:2700:3bf1:5e62:c213:89ce"
        self.DUMMY_DOMAIN = "test.domain"
        self.DUMMY_APIKEY = "secretpassword"
        self.UNKNOWN = "<unknown>"

    def do_sync_wrap(self, no_ipv4: bool, ipv4: Optional[str], no_ipv6: bool, ipv6: Optional[str]) -> LogCapture:
        with LogCapture(level=cl.logging.INFO) as log_out:
            do_sync((self.DUMMY_DOMAIN,), self.DUMMY_APIKEY, no_ipv4, ipv4, no_ipv6, ipv6)
            return log_out

    def test_automatic(self,
                       get_ipv6_address_mock: MagicMock,
                       get_ipv4_address_mock: MagicMock,
                       update_ipv6_address_mock: MagicMock,
                       update_ipv4_address_mock: MagicMock) -> None:
        get_ipv4_address_mock.return_value = self.DUMMY_IPV4
        get_ipv6_address_mock.return_value = self.DUMMY_IPV6
        log_out = self.do_sync_wrap(False, None, False, None)
        self.assertEqual(1, get_ipv6_address_mock.call_count)
        self.assertEqual(1, get_ipv4_address_mock.call_count)
        self.assertEqual(1, update_ipv6_address_mock.call_count)
        self.assertEqual(1, update_ipv4_address_mock.call_count)
        _log_check(log_out,
                   "Update IPV4 to: <automatic lookup>",
                   "Update IPV6 to: <automatic lookup>",
                   "{0} current IPV4 address: {1}".format(self.DUMMY_DOMAIN, self.DUMMY_IPV4),
                   "{0} current IPV6 address: {1}".format(self.DUMMY_DOMAIN, self.DUMMY_IPV6))

    def test_sync_ip_address_no_change(self,
                                       get_ipv6_address_mock: MagicMock,
                                       get_ipv4_address_mock: MagicMock,
                                       update_ipv6_address_mock: MagicMock,
                                       update_ipv4_address_mock: MagicMock) -> None:
        get_ipv6_address_mock.return_value = self.DUMMY_IPV6
        get_ipv4_address_mock.return_value = self.DUMMY_IPV4
        log_out = self.do_sync_wrap(False, self.DUMMY_IPV4, False, self.DUMMY_IPV6)
        self.assertEqual(1, get_ipv6_address_mock.call_count)
        self.assertEqual(1, get_ipv4_address_mock.call_count)
        self.assertEqual(0, update_ipv6_address_mock.call_count)
        self.assertEqual(0, update_ipv4_address_mock.call_count)
        _log_check(log_out,
                   "{0} current IPV4 address: {1}".format(self.DUMMY_DOMAIN, self.DUMMY_IPV4),
                   "{0} IPV4 address already current so not updated.".format(self.DUMMY_DOMAIN),
                   "{0} current IPV6 address: {1}".format(self.DUMMY_DOMAIN, self.DUMMY_IPV6),
                   "{0} IPV6 address already current so not updated.".format(self.DUMMY_DOMAIN))

    def test_sync_ip_address_change_both(self,
                                         get_ipv6_address_mock: MagicMock,
                                         get_ipv4_address_mock: MagicMock,
                                         update_ipv6_address_mock: MagicMock,
                                         update_ipv4_address_mock: MagicMock) -> None:
        get_ipv6_address_mock.return_value = self.UNKNOWN
        get_ipv4_address_mock.return_value = self.UNKNOWN
        log_out = self.do_sync_wrap(False, self.DUMMY_IPV4, False, self.DUMMY_IPV6)
        self.assertEqual(1, get_ipv6_address_mock.call_count)
        self.assertEqual(1, get_ipv4_address_mock.call_count)
        self.assertEqual(1, update_ipv6_address_mock.call_count)
        self.assertEqual(1, update_ipv4_address_mock.call_count)
        _log_check(log_out,
                   "{0} current IPV4 address: {1}".format(self.DUMMY_DOMAIN, self.UNKNOWN),
                   "{0} IPV4 address updated to: {1}".format(self.DUMMY_DOMAIN, self.DUMMY_IPV4),
                   "{0} current IPV6 address: {1}".format(self.DUMMY_DOMAIN, self.UNKNOWN),
                   "{0} IPV6 address updated to: {1}".format(self.DUMMY_DOMAIN, self.DUMMY_IPV6))

    def test_sync_ip_address_change_ipv4(self,
                                         get_ipv6_address_mock: MagicMock,
                                         get_ipv4_address_mock: MagicMock,
                                         update_ipv6_address_mock: MagicMock,
                                         update_ipv4_address_mock: MagicMock) -> None:
        get_ipv6_address_mock.return_value = self.DUMMY_IPV6
        get_ipv4_address_mock.return_value = self.UNKNOWN
        log_out = self.do_sync_wrap(False, self.DUMMY_IPV4, False, self.DUMMY_IPV6)
        self.assertEqual(1, get_ipv6_address_mock.call_count)
        self.assertEqual(1, get_ipv4_address_mock.call_count)
        self.assertEqual(0, update_ipv6_address_mock.call_count)
        self.assertEqual(1, update_ipv4_address_mock.call_count)
        _log_check(log_out,
                   "{0} current IPV4 address: {1}".format(self.DUMMY_DOMAIN, self.UNKNOWN),
                   "{0} IPV4 address updated to: {1}".format(self.DUMMY_DOMAIN, self.DUMMY_IPV4),
                   "{0} current IPV6 address: {1}".format(self.DUMMY_DOMAIN, self.DUMMY_IPV6),
                   "{0} IPV6 address already current so not updated.".format(self.DUMMY_DOMAIN))

    def test_sync_ip_address_change_ipv6(self,
                                         get_ipv6_address_mock: MagicMock,
                                         get_ipv4_address_mock: MagicMock,
                                         update_ipv6_address_mock: MagicMock,
                                         update_ipv4_address_mock: MagicMock) -> None:
        get_ipv6_address_mock.return_value = self.UNKNOWN
        get_ipv4_address_mock.return_value = self.DUMMY_IPV4
        log_out = self.do_sync_wrap(False, self.DUMMY_IPV4, False, self.DUMMY_IPV6)
        self.assertEqual(1, get_ipv6_address_mock.call_count)
        self.assertEqual(1, get_ipv4_address_mock.call_count)
        self.assertEqual(1, update_ipv6_address_mock.call_count)
        self.assertEqual(0, update_ipv4_address_mock.call_count)
        _log_check(log_out,
                   "{0} current IPV4 address: {1}".format(self.DUMMY_DOMAIN, self.DUMMY_IPV4),
                   "{0} IPV4 address already current so not updated.".format(self.DUMMY_DOMAIN),
                   "{0} current IPV6 address: {1}".format(self.DUMMY_DOMAIN, self.UNKNOWN),
                   "{0} IPV6 address updated to: {1}".format(self.DUMMY_DOMAIN, self.DUMMY_IPV6))

    def test_sync_ip_address_change_none(self,
                                         get_ipv6_address_mock: MagicMock,
                                         get_ipv4_address_mock: MagicMock,
                                         update_ipv6_address_mock: MagicMock,
                                         update_ipv4_address_mock: MagicMock) -> None:
        get_ipv6_address_mock.return_value = self.DUMMY_IPV6
        get_ipv4_address_mock.return_value = self.DUMMY_IPV4
        log_out = self.do_sync_wrap(True, None, True, None)
        self.assertEqual(1, get_ipv6_address_mock.call_count)
        self.assertEqual(1, get_ipv4_address_mock.call_count)
        self.assertEqual(0, update_ipv6_address_mock.call_count)
        self.assertEqual(0, update_ipv4_address_mock.call_count)
        _log_check(log_out,
                   "{0} current IPV4 address: {1}".format(self.DUMMY_DOMAIN, self.DUMMY_IPV4),
                   "{0} not updated, new IPV4 address not supplied!".format(self.DUMMY_DOMAIN),
                   "{0} current IPV6 address: {1}".format(self.DUMMY_DOMAIN, self.DUMMY_IPV6),
                   "{0} not updated, new IPV6 address not supplied!".format(self.DUMMY_DOMAIN))
