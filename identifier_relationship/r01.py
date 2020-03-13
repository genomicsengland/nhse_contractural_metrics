#!/usr/bin/env python3
"""
relationship:
genomic_record_patient : genomic_record_referral
"""

from models import gr

CONFIG = {
    'child_identifier_type': 'genomic_record_patient',
    'parent_identifier_type': 'genomic_record_referral',
    'concept_code': 'genomic_record_patient:genomic_record_referral'
}


def get_data(s):
    """
    source data and return list of dictionaries
    """

    q = s.query(gr.ReferralParticipant.patient_uid.
                label('child_identifier_uid'),
                gr.ReferralParticipant.referral_uid.
                label('parent_identifier_uid'))

    return [x._asdict() for x in q]
