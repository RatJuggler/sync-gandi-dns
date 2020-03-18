from unittest import TestCase
from testfixtures import LogCapture

import syncgandidns.configure_logging as cl


class TestConfigureLogging(TestCase):

    USER = "root"
    DEBUG_TEST_MESSAGE = "This is a DEBUG test..."
    VERBOSE_TEST_MESSAGE = "This is a VERBOSE test..."
    INFO_TEST_MESSAGE = "This is a INFO test..."
    WARNING_TEST_MESSAGE = "This is a WARNING test..."

    def test_invalid_log_level(self) -> None:
        with self.assertRaises(ValueError):
            cl.configure_logging("INVALID")

    def test_debug_log_level(self) -> None:
        with LogCapture(level=cl.logging.DEBUG) as log_out:
            cl.logging.debug(self.DEBUG_TEST_MESSAGE)
            cl.verbose(self.VERBOSE_TEST_MESSAGE)
        log_out.check((self.USER, cl.logging.getLevelName(cl.logging.DEBUG), self.DEBUG_TEST_MESSAGE),
                      (self.USER, cl.logging.getLevelName(cl.VERBOSE), self.VERBOSE_TEST_MESSAGE),)

    def test_verbose_log_level(self) -> None:
        with LogCapture(level=cl.VERBOSE) as log_out:
            cl.logging.debug(self.DEBUG_TEST_MESSAGE)
            cl.verbose(self.VERBOSE_TEST_MESSAGE)
            cl.logging.info(self.INFO_TEST_MESSAGE)
        log_out.check((self.USER, cl.logging.getLevelName(cl.VERBOSE), self.VERBOSE_TEST_MESSAGE),
                      (self.USER, cl.logging.getLevelName(cl.logging.INFO), self.INFO_TEST_MESSAGE),)

    def test_info_log_level(self) -> None:
        with LogCapture(level=cl.logging.INFO) as log_out:
            cl.logging.debug(self.DEBUG_TEST_MESSAGE)
            cl.verbose(self.VERBOSE_TEST_MESSAGE)
            cl.logging.info(self.INFO_TEST_MESSAGE)
            cl.logging.warning(self.WARNING_TEST_MESSAGE)
        log_out.check((self.USER, cl.logging.getLevelName(cl.logging.INFO), self.INFO_TEST_MESSAGE),
                      (self.USER, cl.logging.getLevelName(cl.logging.WARNING), self.WARNING_TEST_MESSAGE),)

    def test_warning_log_level(self) -> None:
        with LogCapture(level=cl.logging.WARNING) as log_out:
            cl.logging.debug(self.DEBUG_TEST_MESSAGE)
            cl.verbose(self.VERBOSE_TEST_MESSAGE)
            cl.logging.info(self.INFO_TEST_MESSAGE)
            cl.logging.warning(self.WARNING_TEST_MESSAGE)
        log_out.check((self.USER, cl.logging.getLevelName(cl.logging.WARNING), self.WARNING_TEST_MESSAGE),)
