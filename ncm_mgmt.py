#!/usr/bin/env python3
"""
processes for maintaining ncm and setup processes
each of the functions within the ncm class below can be called from
the command line with python main.py <function>
"""
import logging
import os
import subprocess
import importlib
import fire
from models import ncm, get_engine, make_session
from modules import sql, log
import concept_data
from classes import concept
import local_config

# set up loggers and make one for this module
log.setup_logger()
LOGGER = logging.getLogger(__name__)


def auto_model_gen(db_conn_str, schema, outfile):
    """
    automatically generate sqlalchemy model from existing db
    :param db_conn_str: psycopg2 connection string for db
    :param schema: schema to be used
    :outfile: path to location of file
    """

    LOGGER.debug("running auto_model_gen for %s",
                 db_conn_str)
    subprocess.call(["sqlacodegen", db_conn_str,
                     "--schema", schema,
                     "--outfile", outfile])


class ncm_fire:
    """
    creates the fire command line class
    """

    def create_ncm_db(self):
        """
        create the db tables as defined in models/ncm.py
        """
        LOGGER.info("creating ncm database")

        e = get_engine(local_config.NCM_DB_CONN_STR)

        # prepare database
        sql.run_sql_script(os.path.abspath(
            "sql_scripts/before_table_creation.sql"), e)

        # make the tables
        ncm.BASE.metadata.create_all(e)

        # amend tables and add other stuff
        sql.run_sql_script(os.path.abspath(
            "sql_scripts/after_table_creation.sql"), e)

    def create_gr_model(self):
        """
        create the model for the genomic record database
        """

        LOGGER.info('generating model for genomic record database')

        auto_model_gen(local_config.GR_DB_CONN_STR,
                       "public",
                       os.path.abspath("models/gr.py"))

    def create_bb_model(self):
        """
        create the model for the biobank database
        """

        LOGGER.info('generating model for biobank database')

        auto_model_gen(local_config.BB_DB_CONN_STR,
                       "public",
                       os.path.abspath("models/bb.py"))

    def upload_concept_tables(self):
        """
        upload concept tables from concept_data files to reference schema
        """

        LOGGER.info("uploading the concept tables")

        e = get_engine(local_config.NCM_DB_CONN_STR)
        con = e.raw_connection()
        csr = con.cursor()

        for c in concept_data.__all__:
            LOGGER.info("processing %s", c)
            curr_m = importlib.import_module("concept_data." + c)
            curr_c = concept.Concept(curr_m, c)
            curr_c.qc_data()
            curr_c.save_to_table(csr)
        con.commit()

    def refresh_concept_table(self):
        """
        copy contents of the concept tables in reference schema
        to the concept table in main db
        """

        LOGGER.info('loading reference concept tables into main db')

        e = get_engine(local_config.NCM_DB_CONN_STR)
        s = make_session()

        concept_tables = sql.get_reference_concept_manifest(e)

        # iterate through each of the tables in reference schema
        for i, r in concept_tables.iterrows():
            d = sql.get_reference_concept_table(r.codesystem,
                                                r.table_name,
                                                e)
            # add each of the table's rows to the concept table in main db
            for x, y in d.iterrows():
                s.add(ncm.Concept(
                    local_concept_code=y.local_concept_code,
                    nhs_concept_code=y.nhs_concept_code,
                    codesystem=r.codesystem
                ))

        s.commit()


if __name__ == "__main__":
    fire.Fire(ncm_fire)
