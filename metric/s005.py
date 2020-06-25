#!/usr/bin/env python3
"""
populates ethnic category from identifier table
for all patients
"""

from models import gr

CONFIG = {
    'concept_code': 'ethnic_category',
<<<<<<< HEAD
    'destination_column': 'value_cid:ethnicity'
=======
    'destination_column': 'value_string'
>>>>>>> 4bf8a3677b4d338b6fe3c65dfd36b4b4db8865a7
}

def get_data(s):
    """
    source data and return list of dictionaries
    """

<<<<<<< HEAD
    q = s.query(gr.Patient.uid,
=======
    q = s.query(gr.patient.uid.label('uid'),
>>>>>>> 4bf8a3677b4d338b6fe3c65dfd36b4b4db8865a7
                gr.concept.concept_code.label('metric')
    ).\
    join(gr.Concept,
             gr.Patient.ethnicity_cid ==
             gr.Concept.uid)
    
    return [x._asdict() for x in q]
