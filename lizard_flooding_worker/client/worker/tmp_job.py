#!/usr/bin/python
# (c) Nelen & Schuurmans.  GPL licensed.

import logging
import logging.handlers


def main(logger, body):
    logger.debug('Test 1')
    logger.info('Test 2')
    logger.warning('Test 3')
    logger.error('Test 4')
    logger.critical('Test 5')
