from typing import Optional
from prometheus_client import REGISTRY

from testfixtures import LogCapture
from unittest import TestCase
from unittest.mock import patch, MagicMock

from tests.utils import log_check

from syncgandidns.configure_logging import logging
from syncgandidns.sync_ip_address import do_sync


@patch('syncgandidns.gandi_api.GandiAPI.update_ipv4_address')
@patch('syncgandidns.gandi_api.GandiAPI.update_ipv6_address')
@patch('syncgandidns.gandi_api.GandiAPI.get_ipv4_address')
@patch('syncgandidns.gandi_api.GandiAPI.get_ipv6_address')
@patch('syncgandidns.sync_ip_address.get_ipv4_address')
@patch('syncgandidns.sync_ip_address.get_ipv6_address')
class TestSyncIPAddress(TestCase):

    def setUp(self) -> None:
        self.DUMMY_IPIFY_IPV4 = "86.144.243.79"
        self.DUMMY_IPIFY_IPV6 = "2a00:23c6:2915:1a00:955:e42d:8a1f:2301"
        self.DUMMY_GANDI_IPV4 = "86.144.65.49"
        self.DUMMY_GANDI_IPV6 = "2a00:23c6:290c:2700:3bf1:5e62:c213:89ce"
        self.DUMMY_SET_IPV4 = "86.144.189.114"
        self.DUMMY_SET_IPV6 = "2a00:23c6:2292:b389:11bc:42f6:40b0:1964"
        self.DUMMY_DOMAIN = "test.domain"
        self.DUMMY_APIKEY = "secretpassword"

    def do_sync_wrap(self, no_ipv4: bool, ipv4: Optional[str], no_ipv6: bool, ipv6: Optional[str]) -> LogCapture:
        REGISTRY.unregister(REGISTRY._names_to_collectors['do_sync_last_success'])
        REGISTRY.unregister(REGISTRY._names_to_collectors['do_sync_last_failure'])
        REGISTRY.unregister(REGISTRY._names_to_collectors['do_sync_duration'])
        REGISTRY.unregister(REGISTRY._names_to_collectors['do_sync_processed'])
        with LogCapture(level=logging.INFO) as log_out:
            do_sync((self.DUMMY_DOMAIN,), self.DUMMY_APIKEY, no_ipv4, ipv4, no_ipv6, ipv6, None)
            return log_out

    def test_automatic(self,
                       ipify_get_ipv6_address_mock: MagicMock,
                       ipify_get_ipv4_address_mock: MagicMock,
                       gandi_get_ipv6_address_mock: MagicMock,
                       gandi_get_ipv4_address_mock: MagicMock,
                       update_ipv6_address_mock: MagicMock,
                       update_ipv4_address_mock: MagicMock) -> None:
        ipify_get_ipv6_address_mock.return_value = self.DUMMY_IPIFY_IPV6
        ipify_get_ipv4_address_mock.return_value = self.DUMMY_IPIFY_IPV4
        gandi_get_ipv6_address_mock.return_value = self.DUMMY_GANDI_IPV6
        gandi_get_ipv4_address_mock.return_value = self.DUMMY_GANDI_IPV4
        log_out = self.do_sync_wrap(False, None, False, None)
        self.assertEqual(1, update_ipv6_address_mock.call_count)
        self.assertEqual(1, update_ipv4_address_mock.call_count)
        log_check(log_out,
                  "Update IPV4 to: <automatic lookup>",
                  "Update IPV6 to: <automatic lookup>",
                  "{0} current IPV4 address: {1}".format(self.DUMMY_DOMAIN, self.DUMMY_GANDI_IPV4),
                  "{0} IPV4 address updated to: {1}".format(self.DUMMY_DOMAIN, self.DUMMY_IPIFY_IPV4),
                  "{0} current IPV6 address: {1}".format(self.DUMMY_DOMAIN, self.DUMMY_GANDI_IPV6),
                  "{0} IPV6 address updated to: {1}".format(self.DUMMY_DOMAIN, self.DUMMY_IPIFY_IPV6))

    def test_sync_ip_automatic_no_change(self,
                                         ipify_get_ipv6_address_mock: MagicMock,
                                         ipify_get_ipv4_address_mock: MagicMock,
                                         gandi_get_ipv6_address_mock: MagicMock,
                                         gandi_get_ipv4_address_mock: MagicMock,
                                         update_ipv6_address_mock: MagicMock,
                                         update_ipv4_address_mock: MagicMock) -> None:
        ipify_get_ipv6_address_mock.return_value = self.DUMMY_IPIFY_IPV6
        ipify_get_ipv4_address_mock.return_value = self.DUMMY_IPIFY_IPV4
        gandi_get_ipv6_address_mock.return_value = self.DUMMY_IPIFY_IPV6
        gandi_get_ipv4_address_mock.return_value = self.DUMMY_IPIFY_IPV4
        log_out = self.do_sync_wrap(False, None, False, None)
        self.assertEqual(0, update_ipv6_address_mock.call_count)
        self.assertEqual(0, update_ipv4_address_mock.call_count)
        log_check(log_out,
                  "Update IPV4 to: <automatic lookup>",
                  "Update IPV6 to: <automatic lookup>",
                  "{0} current IPV4 address: {1}".format(self.DUMMY_DOMAIN, self.DUMMY_IPIFY_IPV4),
                  "{0} IPV4 address already current so not updated.".format(self.DUMMY_DOMAIN),
                  "{0} current IPV6 address: {1}".format(self.DUMMY_DOMAIN, self.DUMMY_IPIFY_IPV6),
                  "{0} IPV6 address already current so not updated.".format(self.DUMMY_DOMAIN))

    def test_sync_ip_address_change_both(self,
                                         ipify_get_ipv6_address_mock: MagicMock,
                                         ipify_get_ipv4_address_mock: MagicMock,
                                         gandi_get_ipv6_address_mock: MagicMock,
                                         gandi_get_ipv4_address_mock: MagicMock,
                                         update_ipv6_address_mock: MagicMock,
                                         update_ipv4_address_mock: MagicMock) -> None:
        ipify_get_ipv6_address_mock.return_value = self.DUMMY_IPIFY_IPV6
        ipify_get_ipv4_address_mock.return_value = self.DUMMY_IPIFY_IPV4
        gandi_get_ipv6_address_mock.return_value = self.DUMMY_GANDI_IPV6
        gandi_get_ipv4_address_mock.return_value = self.DUMMY_GANDI_IPV4
        log_out = self.do_sync_wrap(False, self.DUMMY_SET_IPV4, False, self.DUMMY_SET_IPV6)
        self.assertEqual(1, update_ipv6_address_mock.call_count)
        self.assertEqual(1, update_ipv4_address_mock.call_count)
        log_check(log_out,
                  "Update IPV4 to: {0}".format(self.DUMMY_SET_IPV4),
                  "Update IPV6 to: {0}".format(self.DUMMY_SET_IPV6),
                  "{0} current IPV4 address: {1}".format(self.DUMMY_DOMAIN, self.DUMMY_GANDI_IPV4),
                  "{0} IPV4 address updated to: {1}".format(self.DUMMY_DOMAIN, self.DUMMY_SET_IPV4),
                  "{0} current IPV6 address: {1}".format(self.DUMMY_DOMAIN, self.DUMMY_GANDI_IPV6),
                  "{0} IPV6 address updated to: {1}".format(self.DUMMY_DOMAIN, self.DUMMY_SET_IPV6))

    def test_sync_ip_address_change_ipv4(self,
                                         ipify_get_ipv6_address_mock: MagicMock,
                                         ipify_get_ipv4_address_mock: MagicMock,
                                         gandi_get_ipv6_address_mock: MagicMock,
                                         gandi_get_ipv4_address_mock: MagicMock,
                                         update_ipv6_address_mock: MagicMock,
                                         update_ipv4_address_mock: MagicMock) -> None:
        ipify_get_ipv6_address_mock.return_value = self.DUMMY_IPIFY_IPV6
        ipify_get_ipv4_address_mock.return_value = self.DUMMY_IPIFY_IPV4
        gandi_get_ipv6_address_mock.return_value = self.DUMMY_IPIFY_IPV6
        gandi_get_ipv4_address_mock.return_value = self.DUMMY_GANDI_IPV4
        log_out = self.do_sync_wrap(False, self.DUMMY_SET_IPV4, False, None)
        self.assertEqual(0, update_ipv6_address_mock.call_count)
        self.assertEqual(1, update_ipv4_address_mock.call_count)
        log_check(log_out,
                  "Update IPV4 to: {0}".format(self.DUMMY_SET_IPV4),
                  "Update IPV6 to: <automatic lookup>",
                  "{0} current IPV4 address: {1}".format(self.DUMMY_DOMAIN, self.DUMMY_GANDI_IPV4),
                  "{0} IPV4 address updated to: {1}".format(self.DUMMY_DOMAIN, self.DUMMY_SET_IPV4),
                  "{0} current IPV6 address: {1}".format(self.DUMMY_DOMAIN, self.DUMMY_IPIFY_IPV6),
                  "{0} IPV6 address already current so not updated.".format(self.DUMMY_DOMAIN))

    def test_sync_ip_address_change_ipv6(self,
                                         ipify_get_ipv6_address_mock: MagicMock,
                                         ipify_get_ipv4_address_mock: MagicMock,
                                         gandi_get_ipv6_address_mock: MagicMock,
                                         gandi_get_ipv4_address_mock: MagicMock,
                                         update_ipv6_address_mock: MagicMock,
                                         update_ipv4_address_mock: MagicMock) -> None:
        ipify_get_ipv6_address_mock.return_value = self.DUMMY_IPIFY_IPV6
        ipify_get_ipv4_address_mock.return_value = self.DUMMY_IPIFY_IPV4
        gandi_get_ipv6_address_mock.return_value = self.DUMMY_GANDI_IPV6
        gandi_get_ipv4_address_mock.return_value = self.DUMMY_IPIFY_IPV4
        log_out = self.do_sync_wrap(False, None, False, self.DUMMY_SET_IPV6)
        self.assertEqual(1, update_ipv6_address_mock.call_count)
        self.assertEqual(0, update_ipv4_address_mock.call_count)
        log_check(log_out,
                  "Update IPV4 to: <automatic lookup>",
                  "Update IPV6 to: {0}".format(self.DUMMY_SET_IPV6),
                  "{0} current IPV4 address: {1}".format(self.DUMMY_DOMAIN, self.DUMMY_IPIFY_IPV4),
                  "{0} IPV4 address already current so not updated.".format(self.DUMMY_DOMAIN),
                  "{0} current IPV6 address: {1}".format(self.DUMMY_DOMAIN, self.DUMMY_GANDI_IPV6),
                  "{0} IPV6 address updated to: {1}".format(self.DUMMY_DOMAIN, self.DUMMY_SET_IPV6))

    def test_sync_ip_address_change_none(self,
                                         ipify_get_ipv6_address_mock: MagicMock,
                                         ipify_get_ipv4_address_mock: MagicMock,
                                         gandi_get_ipv6_address_mock: MagicMock,
                                         gandi_get_ipv4_address_mock: MagicMock,
                                         update_ipv6_address_mock: MagicMock,
                                         update_ipv4_address_mock: MagicMock) -> None:
        ipify_get_ipv6_address_mock.return_value = self.DUMMY_IPIFY_IPV6
        ipify_get_ipv4_address_mock.return_value = self.DUMMY_IPIFY_IPV4
        gandi_get_ipv6_address_mock.return_value = self.DUMMY_GANDI_IPV6
        gandi_get_ipv4_address_mock.return_value = self.DUMMY_GANDI_IPV4
        log_out = self.do_sync_wrap(True, self.DUMMY_SET_IPV4, True, self.DUMMY_SET_IPV6)
        self.assertEqual(0, update_ipv6_address_mock.call_count)
        self.assertEqual(0, update_ipv4_address_mock.call_count)
        log_check(log_out,
                  "Update IPV4 to: <disabled>",
                  "Update IPV6 to: <disabled>",
                  "{0} current IPV4 address: {1}".format(self.DUMMY_DOMAIN, self.DUMMY_GANDI_IPV4),
                  "{0} IPV4 address not updated, new address not supplied!".format(self.DUMMY_DOMAIN),
                  "{0} current IPV6 address: {1}".format(self.DUMMY_DOMAIN, self.DUMMY_GANDI_IPV6),
                  "{0} IPV6 address not updated, new address not supplied!".format(self.DUMMY_DOMAIN))
