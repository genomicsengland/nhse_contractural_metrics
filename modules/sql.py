#!/usr/bin/env python3
"""
run sql scripts 
"""

import logging
import sqlparse
import pandas as pd

LOGGER = logging.getLogger(__name__)

def run_sql_script(fn, e):
    """
    run contents of a sql file on a given engine
    :param fn: path of file to be executed
    :param e: db engine to execute on
    """

    LOGGER.debug("executing %s", fn)

    # create connection to db engine
    db_con = e.connect()

    # get contents of file and remove comments
    file_obj = open(fn, "r")
    file_lines = file_obj.readlines()
    clean_lines = sqlparse.format(" ".join(file_lines), strip_comments=True)

    # execute then close down
    db_con.execute(clean_lines)
    db_con.close()
    file_obj.close()


def get_reference_concept_manifest(e):
    """
    gets the concept table details from reference schema
    :param e: engine bound to ncm database
    :returns: pandas dataframe of table_name, codesystem
    """

    LOGGER.debug('running get_reference_concept_manifest')

    sql = "select table_name" \
        ",regexp_replace(table_name, '^c_', '')  as codesystem " \
        "from information_schema.tables where table_name like 'c_%%' " \
        "and table_schema = 'nhse_contractural_metrics_reference'"

    df = pd.read_sql(sql, con=e)

    LOGGER.debug('got %s rows', len(df))

    return df


def get_reference_concept_table(codesystem, table_name, e):
    """
    get the table of data present in one of the concept data tables
    in reference schema
    :param table_name: the name of the table being queried
    :param codesystem: the name of the codesystem being loaded
    :param e: engine bound to ncm database
    :returns: pandas df of data
    """

    LOGGER.debug('running get_reference_concept_table for %s', codesystem)

    sql = f"select uid, local_concept_code, nhs_concept_code from " \
        f"nhse_contractural_metrics_reference.{table_name}"

    df = pd.read_sql(sql, con=e)

    LOGGER.debug('got %s rows', len(df))

    return df
