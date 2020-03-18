from unittest import TestCase
from unittest.mock import patch

from syncgandidns.sync_ip_address import sync_ip_address

DUMMY_IPV4 = "86.144.65.49"
DUMMY_IPV6 = "2a00:23c6:290c:2700:3bf1:5e62:c213:89ce"
DUMMY_DOMAIN = "test.domain"
DUMMY_API_KEY = "secretpassword"
NO_MATCH = "nomatch"


def dummy_get_domain_record_resource_value(resource: str) -> str:
    if resource == 'A':
        return DUMMY_IPV4
    if resource == 'AAAA':
        return DUMMY_IPV6


@patch('syncgandidns.gandi_api.GandiAPI.update_domain_record_resource')
@patch('syncgandidns.gandi_api.GandiAPI.get_domain_record_resource_value')
class TestSyncIPAddress(TestCase):

    def setUp(self) -> None:
        pass

    def test_sync_ip_address_no_change(self,
                                       get_domain_record_resource_value_mock,
                                       update_domain_record_resource_mock) -> None:
        get_domain_record_resource_value_mock.side_effect = dummy_get_domain_record_resource_value
        sync_ip_address(DUMMY_DOMAIN, DUMMY_IPV4, DUMMY_IPV6, DUMMY_API_KEY)
        self.assertEqual(2, get_domain_record_resource_value_mock.call_count)
        self.assertEqual(0, update_domain_record_resource_mock.call_count)

    def test_sync_ip_address_change_both(self,
                                         get_domain_record_resource_value_mock,
                                         update_domain_record_resource_mock) -> None:
        get_domain_record_resource_value_mock.return_value = NO_MATCH
        sync_ip_address(DUMMY_DOMAIN, DUMMY_IPV4, DUMMY_IPV6, DUMMY_API_KEY)
        self.assertEqual(2, get_domain_record_resource_value_mock.call_count)
        self.assertEqual(2, update_domain_record_resource_mock.call_count)

    def test_sync_ip_address_change_ipv4(self,
                                         get_domain_record_resource_value_mock,
                                         update_domain_record_resource_mock) -> None:
        get_domain_record_resource_value_mock.side_effect = [NO_MATCH, DUMMY_IPV6]
        sync_ip_address(DUMMY_DOMAIN, DUMMY_IPV4, DUMMY_IPV6, DUMMY_API_KEY)
        self.assertEqual(2, get_domain_record_resource_value_mock.call_count)
        self.assertEqual(1, update_domain_record_resource_mock.call_count)

    def test_sync_ip_address_change_ipv6(self,
                                         get_domain_record_resource_value_mock,
                                         update_domain_record_resource_mock) -> None:
        get_domain_record_resource_value_mock.side_effect = [DUMMY_IPV4, NO_MATCH]
        sync_ip_address(DUMMY_DOMAIN, DUMMY_IPV4, DUMMY_IPV6, DUMMY_API_KEY)
        self.assertEqual(2, get_domain_record_resource_value_mock.call_count)
        self.assertEqual(1, update_domain_record_resource_mock.call_count)
