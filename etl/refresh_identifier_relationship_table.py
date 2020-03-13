#!/usr/bin/env python3
"""
etl to get and write all the different relationship within the identifier_relationship
folder
1. load all the different files as modules
2. run the get_data function
3. write the data to the identifier_relationship table
"""

import importlib
import logging
import identifier_relationship
from models import ncm
from modules import db

LOGGER = logging.getLogger(__name__)


def run_etl(s):
    """
    run each of the relationship etls
    :param s: sqlalchemy session
    """

    LOGGER.debug('running run_etl')

    modules_to_load = identifier_relationship.__all__

    LOGGER.debug('processing %s identifier_relationship modules', len(modules_to_load))

    for m in modules_to_load:

        LOGGER.debug('processing %s', m)

        # load the modules and create the Identifier object
        curr_module = importlib.import_module("identifier_relationship." + m)

        # get the cid for the relationship
        cid = db.get_cid([curr_module.CONFIG['concept_code']],
                         'identifier_relationship',
                         s)[curr_module.CONFIG['concept_code']]

        # get the data
        d = curr_module.get_data(s)

        # for each element returned create the identifier_relationship row
        for x in d:
            a = ncm.IdentifierRelationship(
                child_identifier_uid=x['child_identifier_uid'],
                parent_identifier_uid=x['parent_identifier_uid'],
                type_cid=cid
            )
            s.add(a)
