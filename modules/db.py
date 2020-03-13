#!/usr/bin/env python3
"""
various helper functions for working with dbs
"""

import logging
import importlib
from sqlalchemy import and_
from models import ncm

LOGGER = logging.getLogger(__name__)


def get_cid(concept_code, codesystem, s):
    """
    get the uid for the given concept_code:codesystem
    :param concept_code: list of local_concept_code needed
    :param codesystem: value of codesystem for the given concept code
    :returns: dictionary of concept_code:cid
    """

    LOGGER.debug('fetching cid for %s:%s',
                 concept_code,
                 codesystem)

    q = s.query(ncm.Concept.uid,
                ncm.Concept.local_concept_code).\
        filter(and_(ncm.Concept.local_concept_code.in_(concept_code),
                    ncm.Concept.codesystem == codesystem))

    return {x[1]: x[0] for x in q}


def get_db_column(db_name, table_name, column_name):
    """
    get a column from a sqlalchemy model given parameters
    :param db_name: string of db, equivalent to the name of the file in models
    :param table_name: string of table name in model e.g. Person
    :param column_name: string of the column name to retrieve
    :returns: sqlalchemy column object
    """

    LOGGER.debug('fetching %s.%s.%s', db_name, table_name, column_name)

    db = importlib.import_module('models.' + db_name)
    table = getattr(db, table_name)
    column = getattr(table, column_name)

    return column
