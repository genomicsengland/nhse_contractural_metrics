#!/usr/bin/env python3
"""
populates referral test urgency from genomic record
for all patients
"""

from models import gr

CONFIG = {
    'concept_code': 'test_urgency',
    'destination_column': 'value_cid:priority'
}

def get_data(s):
    """
    source data and return list of dictionaries
    """

    q = s.query(gr.Referral.uid,
                gr.Concept.concept_code.label('metric')
    ).\
    join(gr.Concept,
             gr.referral.priority_cid ==
             gr.Concept.uid)
    
    return [x._asdict() for x in q]
