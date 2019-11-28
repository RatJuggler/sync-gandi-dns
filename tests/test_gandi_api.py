import os

from unittest import TestCase
from testfixtures import LogCapture

import syncgandidns.configure_logging as cl
import syncgandidns.gandi_api as gandi_api


class TestGandiAPI(TestCase):

    def setUp(self):
        self.API_KEY = os.getenv("GANDI_API_KEY")
        self.TEST_DOMAIN = os.getenv("GANDI_TEST_DOMAIN")

    def test_get_domain_record_resource(self):
        expected = "GET: " + gandi_api.URL + self.TEST_DOMAIN + "/records/@/A"
        with LogCapture(level=cl.logging.INFO) as log_out:
            gandi_api.get_domain_record_resource(self.API_KEY, self.TEST_DOMAIN, 'A')
        log_out.check(("root", cl.logging.getLevelName(cl.logging.INFO), expected))
