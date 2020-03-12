#!/usr/bin/env python3
"""
various helper functions for working with ncm db
"""

import logging
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
