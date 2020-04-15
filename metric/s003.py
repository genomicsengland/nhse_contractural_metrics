#!/usr/bin/env python3
"""
populates postcode of usual address
from genomic record address table
"""

from models import gr

CONFIG = {
    'concept_code': 'postcode_of_usual_address',
    'destination_column': 'value_string'
}

def get_data(s):
    """
    source data and return list of dictionaries
    """

    q = s.query(gr.Patient.uid,
                gr.Addres.address_postcode.label('metric')).\
        join(gr.Addres,
             gr.Patient.address_uid == gr.Addres.uid).\
        filter(gr.Addres.address_postcode.isnot(None))

    return [x._asdict() for x in q]
