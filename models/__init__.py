#!/usr/bin/env python3
"""
folders holds the various different sqlalchemy models for the project
"""
import logging
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from local_config import NCM_DB_CONN_STR,\
    GR_DB_CONN_STR
from . import ncm, gr

LOGGER = logging.getLogger(__name__)


def make_session():
    """
    get SQLAlchemy session bound to all required DBs
    """
    LOGGER.debug("making session")
    session = sessionmaker()
    session.configure(binds={ncm.BASE: get_engine(NCM_DB_CONN_STR),
                             gr.Base: get_engine(GR_DB_CONN_STR),
                             })
    return session()


def get_engine(conn_str):
    """
    Get an engine for a db
    :param conn_str: psycopg2 connection string for db
    """
    LOGGER.debug("received call to get_engine")
    return create_engine(conn_str, echo=False)
