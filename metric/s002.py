#!/usr/bin/env python3
"""
populates person birth date
from genomic record patient table
"""

from models import gr

CONFIG = {
    'concept_code': 'person_birth_date',
    'destination_column': 'value_datetime'
}

def get_data(s):
    """
    source data and return list of dictionaries
    """

    q = s.query(gr.Patient.uid,
                gr.Patient.patient_date_of_birth.label('metric'))

    return [x._asdict() for x in q]
