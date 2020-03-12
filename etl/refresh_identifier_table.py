#!/usr/bin/env python3
"""
etl to get and write each of the identifier's data
1. load all of the identifier modules listed in identifier.__all__
2. create an instance of the Identifier class
3. get the data
4. write the data to the identifier table
"""

import importlib
import logging
import identifier
from classes.identifier import Identifier

LOGGER = logging.getLogger(__name__)


def run_etl(s):
    """
    run each of the identifier etls
    :param s: sqlalchemy session
    """

    LOGGER.debug('running run_etl')

    modules_to_load = identifier.__all__

    LOGGER.debug('processing %s identifier modules', len(modules_to_load))

    # iterate through each of the modules
    for m in modules_to_load:

        LOGGER.debug('processing %s', m)

        # load the modules and create the Identifier object
        curr_module = importlib.import_module("identifier." + m)
        curr_identifier = Identifier(curr_module, s)

        # get the data and write to the db
        curr_identifier.get_data()
        curr_identifier.write_data()
