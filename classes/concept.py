#!/usr/bin/env python3
"""
provides a Concept class for processing the various concepts within the
database
ultimately it pulls in all the data within the different files in the
concept folder, and writes it to a table in the ncm_reference schema
"""

import logging

LOGGER = logging.getLogger(__name__)


class Concept:
    """
    class for processing the different consent types
    """

    def __init__(self, m, codesystem):
        """
        initiate a new instance of Concept
        :param m: module file containing details of the concept
        :param codesystem: name of the codesystem
        """

        LOGGER.debug('creating new concept class for %s', codesystem)

        self.codesystem = codesystem
        self.data = [{'local_concept_code': x,
                      'nhs_concept_code': y}
                     for x, y in m.DATA]

    def qc_data(self):
        """
        QC the concept data
        """

        LOGGER.debug('qcing data for %s', self.codesystem)

        # check that there aren't any duplicate local_concept_code
        assert len(self.data) ==\
            len(set([x['local_concept_code'] for x in self.data])),\
            "duplicate local_concept_code"

    def save_to_table(self, cur):
        """
        write out the data to a table in ncm_reference
        :param cur: psycopg2 cursor
        """

        LOGGER.debug('uploading data for %s', self.codesystem)

        # drop table if exists
        sql_str = f'drop table if exists\
            nhse_contractural_metrics_reference.c_{self.codesystem}'
        cur.execute(sql_str)

        # create table
        sql_str = f'create table nhse_contractural_metrics_reference.c_{self.codesystem}\
            (local_concept_code varchar not null,\
            nhs_concept_code varchar,\
            de_datetime timestamptz default now());'
        cur.execute(sql_str)

        # write rows
        cur.executemany(f'insert into nhse_contractural_metrics_reference.c_{self.codesystem}\
                        (local_concept_code, nhs_concept_code) values\
                        (%(local_concept_code)s, %(nhs_concept_code)s)',
                        self.data)
