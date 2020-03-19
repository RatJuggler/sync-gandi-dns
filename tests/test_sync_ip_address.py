from unittest import TestCase
from unittest.mock import patch

from syncgandidns.sync_ip_address import sync_ip_address

DUMMY_IPV4 = "86.144.65.49"
DUMMY_IPV6 = "2a00:23c6:290c:2700:3bf1:5e62:c213:89ce"
DUMMY_DOMAIN = "test.domain"
DUMMY_API_KEY = "secretpassword"
NO_MATCH = "nomatch"


@patch('syncgandidns.gandi_api.GandiAPI.update_domain_record_resource')
@patch('syncgandidns.gandi_api.GandiAPI.get_ipv4_address')
@patch('syncgandidns.gandi_api.GandiAPI.get_ipv6_address')
class TestSyncIPAddress(TestCase):

    def setUp(self) -> None:
        pass

    def test_sync_ip_address_no_change(self,
                                       get_ipv6_address_mock,
                                       get_ipv4_address_mock,
                                       update_domain_record_resource_mock) -> None:
        get_ipv6_address_mock.return_value = DUMMY_IPV6
        get_ipv4_address_mock.return_value = DUMMY_IPV4
        sync_ip_address(DUMMY_DOMAIN, DUMMY_IPV4, DUMMY_IPV6, DUMMY_API_KEY)
        self.assertEqual(1, get_ipv6_address_mock.call_count)
        self.assertEqual(1, get_ipv4_address_mock.call_count)
        self.assertEqual(0, update_domain_record_resource_mock.call_count)

    def test_sync_ip_address_change_both(self,
                                         get_ipv6_address_mock,
                                         get_ipv4_address_mock,
                                         update_domain_record_resource_mock) -> None:
        get_ipv6_address_mock.return_value = NO_MATCH
        get_ipv4_address_mock.return_value = NO_MATCH
        sync_ip_address(DUMMY_DOMAIN, DUMMY_IPV4, DUMMY_IPV6, DUMMY_API_KEY)
        self.assertEqual(1, get_ipv6_address_mock.call_count)
        self.assertEqual(1, get_ipv4_address_mock.call_count)
        self.assertEqual(2, update_domain_record_resource_mock.call_count)

    def test_sync_ip_address_change_ipv4(self,
                                         get_ipv6_address_mock,
                                         get_ipv4_address_mock,
                                         update_domain_record_resource_mock) -> None:
        get_ipv6_address_mock.return_value = DUMMY_IPV6
        get_ipv4_address_mock.return_value = NO_MATCH
        sync_ip_address(DUMMY_DOMAIN, DUMMY_IPV4, DUMMY_IPV6, DUMMY_API_KEY)
        self.assertEqual(1, get_ipv6_address_mock.call_count)
        self.assertEqual(1, get_ipv4_address_mock.call_count)
        self.assertEqual(1, update_domain_record_resource_mock.call_count)

    def test_sync_ip_address_change_ipv6(self,
                                         get_ipv6_address_mock,
                                         get_ipv4_address_mock,
                                         update_domain_record_resource_mock) -> None:
        get_ipv6_address_mock.return_value = NO_MATCH
        get_ipv4_address_mock.return_value = DUMMY_IPV4
        sync_ip_address(DUMMY_DOMAIN, DUMMY_IPV4, DUMMY_IPV6, DUMMY_API_KEY)
        self.assertEqual(1, get_ipv6_address_mock.call_count)
        self.assertEqual(1, get_ipv4_address_mock.call_count)
        self.assertEqual(1, update_domain_record_resource_mock.call_count)
