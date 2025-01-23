"""Tests for the logging module"""
from dkist_service_configuration.logging import logger


def test_log_levels():
    logger.trace("trace")
    logger.debug("debug")
    logger.info("info")
    logger.warning("warning")
    logger.error("error")
    logger.critical("critical")
