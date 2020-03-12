#!/usr/bin/env python3
"""
populates person stated gender code using administrative gender_cid
from genomic record patient table
"""

from models import gr

CONFIG = {
    'concept_code': 'person_stated_gender_code',
    'destination_column': 'value_cid:administrative_gender'
}

def get_data(s):
    """
    source data and return list of dictionaries
    """

    q = s.query(gr.Patient.uid,
                gr.Concept.concept_code.label('metric')).\
        join(gr.Concept,
             gr.Patient.administrative_gender_cid ==\
             gr.Concept.uid)

    return [x._asdict() for x in q]
