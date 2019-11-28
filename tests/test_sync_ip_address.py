from unittest import TestCase
from unittest.mock import patch

from syncgandidns.sync_ip_address import sync_ip_address


def dummy_get_domain_record_resource_value(resource: str):
    if resource == 'A':
        return "86.144.65.49"
    if resource == 'AAAA':
        return "2a00:23c6:290c:2700:3bf1:5e62:c213:89ce"


@patch('syncgandidns.gandi_api.GandiAPI.update_domain_record_resource')
@patch('syncgandidns.gandi_api.GandiAPI.get_domain_record_resource_value')
class TestSyncIPAddress(TestCase):

    def setUp(self):
        pass

    def test_sync_ip_address_no_change(self,
                                       get_domain_record_resource_value_mock,
                                       update_domain_record_resource_mock):
        get_domain_record_resource_value_mock.side_effect = dummy_get_domain_record_resource_value
        sync_ip_address("test.domain", "86.144.65.49", "2a00:23c6:290c:2700:3bf1:5e62:c213:89ce", "secretpassword")
        self.assertEqual(2, get_domain_record_resource_value_mock.call_count)
        self.assertEqual(0, update_domain_record_resource_mock.call_count)

    def test_sync_ip_address_change_both(self,
                                         get_domain_record_resource_value_mock,
                                         update_domain_record_resource_mock):
        get_domain_record_resource_value_mock.return_value = "nomatch"
        sync_ip_address("test.domain", "86.144.65.49", "2a00:23c6:290c:2700:3bf1:5e62:c213:89ce", "secretpassword")
        self.assertEqual(2, get_domain_record_resource_value_mock.call_count)
        self.assertEqual(2, update_domain_record_resource_mock.call_count)

    def test_sync_ip_address_change_ipv4(self,
                                         get_domain_record_resource_value_mock,
                                         update_domain_record_resource_mock):
        get_domain_record_resource_value_mock.side_effect = ["nomatch", "2a00:23c6:290c:2700:3bf1:5e62:c213:89ce"]
        sync_ip_address("test.domain", "86.144.65.49", "2a00:23c6:290c:2700:3bf1:5e62:c213:89ce", "secretpassword")
        self.assertEqual(2, get_domain_record_resource_value_mock.call_count)
        self.assertEqual(1, update_domain_record_resource_mock.call_count)

    def test_sync_ip_address_change_ipv6(self,
                                         get_domain_record_resource_value_mock,
                                         update_domain_record_resource_mock):
        get_domain_record_resource_value_mock.side_effect = ["86.144.65.49", "nomatch"]
        sync_ip_address("test.domain", "86.144.65.49", "2a00:23c6:290c:2700:3bf1:5e62:c213:89ce", "secretpassword")
        self.assertEqual(2, get_domain_record_resource_value_mock.call_count)
        self.assertEqual(1, update_domain_record_resource_mock.call_count)
