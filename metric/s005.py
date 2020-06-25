#!/usr/bin/env python3
"""
populates ethnic category from identifier table
for all patients
"""

from models import gr

CONFIG = {
    'concept_code': 'ethnic_category',
    'destination_column': 'value_cid:ethnicity'
}

def get_data(s):
    """
    source data and return list of dictionaries
    """

    q = s.query(gr.Patient.uid,
                gr.concept.concept_code.label('metric')
    ).\
    join(gr.Concept,
             gr.Patient.ethnicity_cid ==
             gr.Concept.uid)
    
    return [x._asdict() for x in q]
