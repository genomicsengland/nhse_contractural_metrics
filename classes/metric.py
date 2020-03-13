#!/usr/bin/env python3
"""
provides a Metric class that is initiated with one of
the metric modules.
the modules contain data and functions to gather a single
metric.
the classes standardises the collection, qc and writing of
the data to db
"""

import logging
from models import ncm
from modules import db

LOGGER = logging.getLogger(__name__)


class Metric:
    """
    class for collecting, qcing and uploading metric data
    """

    def __init__(self, m, s):
        """
        initiate a new instance of the class
        :param m: an instance of the metric module
        :param s: sqlalchemy session
        """

        LOGGER.debug('making new instance of metric')

        self.m = m
        self.s = s
        self.concept_code = m.CONFIG['concept_code']
        self.get_data_f = m.get_data
        self.data = None
        self.type_cid = db.get_cid([self.concept_code],
                                   'metric',
                                   self.s)[self.concept_code]

        # for metrics where the destination column is value_cid then get
        # value_cid:<concept_code for the metric> from config field
        if m.CONFIG['destination_column'].startswith('value_cid:'):

            self.destination_column, self.metric_codesystem =\
                m.CONFIG['destination_column'].split(":", 2)

        else:

            self.destination_column = m.CONFIG['destination_column']

    def get_data(self):
        """
        get the metric data
        """

        self.data = self.get_data_f(self.s)

    def write_data(self):
        """
        write the results to the db
        """

        # if the metric is a concept code then need to fetch cid
        if self.destination_column == "value_cid":

            # get all the concept code values for the metric
            # then get their cids from the concept table
            all_metric_concept_codes = set([x['metric'] for x in self.data])
            all_metric_cid = db.get_cid(list(all_metric_concept_codes),
                                        self.metric_codesystem,
                                        self.s)

            # replace each metric_concept_code with the matching cid
            for x in self.data:
                x['metric'] = all_metric_cid[x['metric']]

        for x in self.data:

            a = ncm.Metric(
                identifier_uid=x['uid'],
                type_cid=self.type_cid
            )

            # add the metric value to the configured destination column
            setattr(a, self.destination_column, x['metric'])

            self.s.merge(a)
