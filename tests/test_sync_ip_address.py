import mock

from unittest import TestCase

from syncgandidns.sync_ip_address import sync_ip_address


@mock.patch('syncgandidns.gandi_api.GandiAPI.get_domain_record_resource_value')
@mock.patch('syncgandidns.gandi_api.GandiAPI.update_domain_record_resource')
class TestSyncIPAddress(TestCase):

    def setUp(self):
        pass

    def test_sync_ip_address(self, get_domain_record_resource_value_mock, update_domain_record_resource_mock):
        get_domain_record_resource_value_mock.return_value = "0.0.0.0"
        sync_ip_address("test.domain", "86.144.65.49", "2a00:23c6:290c:2700:3bf1:5e62:c213:89ce", "secretpassword")
        self.assertEqual(2, get_domain_record_resource_value_mock.call_count)
        self.assertEqual(2, update_domain_record_resource_mock.call_count)
