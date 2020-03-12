#!/usr/bin/env python3
"""
provides a Identifier class that is initiated with one of
the identifier modules.
the modules contain data and functions to gather all instances
for a single identifier type
the class standardises the collection, qc and writing of
the data to db
"""

from models import ncm
from modules import db

class Identifier:
    """
    class for collecting, qcing and uploading identifier data
    """

    def __init__(self, m, s):
        """
        initiate a new instance of the class
        :param m: an instance of the identifier module
        :param s: sqlalchemy session
        """

        self.m = m
        self.s = s
        self.concept_code = m.CONFIG['concept_code']
        self.get_data_f = m.get_data
        self.data = None
        self.type_cid = db.get_cid([self.concept_code],
                                   'identifier',
                                   self.s)[self.concept_code]

    def get_data(self):
        """
        get the identifier data
        """

        self.data = self.get_data_f(self.s)

    def write_data(self):
        """
        merge the identifier data into the identifier table
        """

        for x in self.data:

            a = ncm.Identifier(
                uid=x['uid'],
                human_readable_id=x['human_readable_id'],
                type_cid=self.type_cid
            )

            self.s.merge(a)
