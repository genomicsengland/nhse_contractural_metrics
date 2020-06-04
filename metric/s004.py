#!/usr/bin/env python3
"""
populates NHS number from identifier table
for all patients
"""

from models import gr

CONFIG = {
    'concept_code': 'nhs_number',
    'destination_column': 'value_string'
}

def get_data(s):
    """
    source data and return list of dictionaries
    """

    q = s.query(gr.Identifier.patient_uid.label('uid'),
                gr.Identifier.value.label('metric')
    ).\
    join(gr.Concept,
         gr.Concept.uid == gr.Identifier.type_cid).\
         filter(gr.Identifier.patient_uid.isnot_(None)).\

    return [x._asdict() for x in q]
