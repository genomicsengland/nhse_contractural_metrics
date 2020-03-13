#!/usr/bin/env python3
"""
main file for the nshe contractural metrics etls
each of the functions within the ncm class below can be called from
the command line with python main.py <function>
"""
import logging
import fire
from models import make_session
from modules import log
from etl import refresh_identifier_table,\
    refresh_metric_table

# set up loggers and make one for this module
log.setup_logger()
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
        refresh_identifier_table2.run_etl(s)
        s.commit()

    def refresh_metric_table(self):
        """
        gather all metrics required and add/update table in main db
        """

        LOGGER.info('fetching and refreshing all metrics')

        s = make_session()
        refresh_metric_table.run_etl(s)
        s.commit()


if __name__ == "__main__":
    fire.Fire(ncm_fire)
