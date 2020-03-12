#!/usr/bin/env python3
"""
etl to get and write each of the metric's data
1. load all of the metric modules listed in metric.__all__
2. create an instance of the Metric class
3. get the data
4. write the data to the metric table
"""

import importlib
import logging
import metric
from classes.metric import Metric

LOGGER = logging.getLogger(__name__)


def run_etl(s):
    """
    run each of the metric etls
    :param s: sqlalchemy session
    """

    LOGGER.debug('running run_etl')

    modules_to_load = metric.__all__

    LOGGER.debug('processing %s metric modules', len(modules_to_load))

    # iterate through each of the modules
    for m in modules_to_load:

        LOGGER.debug('processing %s', m)

        # load the modules and create the Identifier object
        curr_module = importlib.import_module("metric." + m)
        curr_metric = Metric(curr_module, s)

        # get the data and write to the db
        curr_metric.get_data()
        curr_metric.write_data()
