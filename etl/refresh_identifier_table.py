#!/usr/bin/env python3
"""
etl to get and write each of the identifier's data
1. iterate through each of the sections of ID_CONFIG
2. assemble the query to get the relevant data
3. get the data
4. write it to identifier table
"""
import logging
from modules import db
from models import ncm

LOGGER = logging.getLogger(__name__)

# this holds all the different types of identifier associated
# with metrics being collected
# each of the identifiers must correspond to a concept code within
# the concept table
# if the identifier does not have hr_id then set it to None, same for uid
# the table name and column name must correspond to that as specified in the
# relevant model file in the models folder
ID_CONFIG = {
    'genomic_record_patient':
    {
        'source': {
            'db': 'gr',
            'table': 'Patient',
            'uid': 'uid',
            'human_readable_id': 'patient_human_readable_stored_id'
        }
    },
    'genomic_record_person':
    {
        'source': {
            'db': 'gr',
            'table': 'Person',
            'uid': 'uid',
            'human_readable_id': None
        }
    },
    'genomic_record_referral':
    {
        'source': {
            'db': 'gr',
            'table': 'Referral',
            'uid': 'uid',
            'human_readable_id': 'referral_human_readable_stored_id'
        }
    },
    'biobank_gel1008_platekey':
    {
        'source': {
            'db': 'bb',
            'table': 'BiobankIlluminaGel1008',
            'uid': None,
            'human_readable_id': 'plate_well_id'
        }
    },
}


def run_etl(s):
    """
    gather each of the different identifiers
    :param s: sqlalchemy session
    """

    LOGGER.debug('running run_etl')

    # get cid for each of the different identifier concept_codes
    cids = db.get_cid(list(ID_CONFIG.keys()), 'identifier', s)

    # iterate through each of the different identifiers
    for concept_code in ID_CONFIG:

        LOGGER.debug('processing %s', concept_code)

        # get the cid for identifier type
        type_cid = cids[concept_code]

        # assemble the query
        source_config = ID_CONFIG[concept_code]['source']

        # if identifier has both uid and hr_id already
        if source_config['uid'] and source_config['human_readable_id']:
            q = s.query(
                db.get_db_column(source_config['db'],
                                 source_config['table'],
                                 source_config['uid']).
                label('uid'),
                db.get_db_column(source_config['db'],
                                 source_config['table'],
                                 source_config['human_readable_id']).
                label('human_readable_id')
            )

        # if identifier only had uid and not hr_id
        elif source_config['uid'] and not source_config['human_readable_id']:
            q = s.query(
                db.get_db_column(source_config['db'],
                                 source_config['table'],
                                 source_config['uid']).
                label('uid')
            )

        # if identifier only has hr_id
        elif not source_config['uid'] and source_config['human_readable_id']:
            q = s.query(
                db.get_db_column(source_config['db'],
                                 source_config['table'],
                                 source_config['human_readable_id']).
                label('human_readable_id')
            )

        else:
            LOGGER.critical('missing columns for %s', concept_code)

        collected_identifiers = [x._asdict() for x in q]

        LOGGER.info('Collected %s instances of %s',  len(collected_identifiers),
                    concept_code)

        # collected identifiers will now include either uid or
        # human_readable_id or both, now convert each into an identifer
        # object to be loaded to db
        for x in collected_identifiers:

            i = ncm.Identifier(
                type_cid=type_cid
            )

            for attr in x.keys():
                setattr(i, attr, x[attr])

            s.merge(i)
