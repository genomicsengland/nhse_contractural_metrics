#!/usr/bin/env python3
"""
main file for the nshe contractural metrics etls
each of the functions within the ncm class below can be called from
the command line with python main.py <function>
"""
# set up loggers and make one for this module
from modules import log
log.setup_logger()

import logging
import fire
from models import make_session
from etl import refresh_identifier_table,\
    refresh_metric_table,\
    refresh_identifier_relationship_table

LOGGER = logging.getLogger(__name__)


class ncm_fire:
    """
    creates the fire command line class
    """

    def refresh_identifier_table(self):
        """
        gather all identifiers required and add/update table in main
        db
        """

        LOGGER.info('fetching and refreshing all identifiers')

        s = make_session()
        refresh_identifier_table.run_etl(s)
        s.commit()

    def refresh_identifier_relationship_table(self):
        """
        gather all identifier relationships required and add/update table
        in main db
        """

        LOGGER.info('fetching and refreshing all identifier relationships')

        s = make_session()
        refresh_identifier_relationship_table.run_etl(s)
        s.commit()


    def refresh_metric_table(self):
        """
        gather all metrics required and add/update table in main db
        """

        LOGGER.info('fetching and refreshing all metrics')

        s = make_session()
        refresh_metric_table.run_etl(s)
        s.commit()

    def refresh_db(self):
        """
        gather all identifiers, relationships and metrics and update db
        """

        LOGGER.info('refreshing ncm db')

        self.refresh_identifier_table()
        self.refresh_identifier_relationship_table()
        self.refresh_metric_table()


if __name__ == "__main__":
    fire.Fire(ncm_fire)
