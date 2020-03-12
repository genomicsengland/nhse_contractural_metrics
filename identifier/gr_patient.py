#!/usr/bin/env python3
"""
fetches all patient uids
"""

from models import gr

CONFIG = {
    'concept_code': 'genomic_record_patient',
}

def get_data(s):
    """
    source data and return list of dictionaries
    """

    q = s.query(gr.Patient.uid,
                gr.Patient.patient_human_readable_stored_id.\
                label('human_readable_id'))

    return [x._asdict() for x in q]
