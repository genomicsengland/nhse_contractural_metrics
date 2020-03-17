#!/usr/bin/env python3
"""
defines tables and relationships for the ncm database
requires uuid extension to be available in destination db:
create EXTENSION if not EXISTS "uuid-ossp";
run as superuser
"""
from sqlalchemy import BigInteger, Boolean, Column, Date, DateTime, Integer,\
    Numeric, String, Table, Text, UniqueConstraint, ForeignKey, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import datetime
import uuid

BASE = declarative_base()
METADATA = BASE.metadata


class Concept(BASE):
    """
    holds all concepts (lookups, categories )referenced in the database and
    their equivalent value to be given in the final submission (if applicable)
    """
    __tablename__ = "concept"
    __table_args__ = {"schema": "nhse_contractural_metrics"}

    uid = Column(UUID(as_uuid=True), primary_key=True,
                 server_default=text("uuid_generate_v4()"))
    local_concept_code = Column(String, nullable=False)
    codesystem = Column(String, nullable=False)
    nhs_concept_code = Column(String)
    de_datetime = Column(DateTime, nullable=False,
                         default=datetime.datetime.now())


class Identifier(BASE):
    """
    holds the system and human readable identifiers for the different
    objects being tracked (samples, patients, referrals etc.)
    """

    __tablename__ = "identifier"
    __table_args__ = {"schema": "nhse_contractural_metrics"}

    uid = Column(UUID(as_uuid=True), primary_key=True,
                 server_default=text("uuid_generate_v4()"))
    human_readable_id = Column(String)
    type_cid = Column(ForeignKey("nhse_contractural_metrics.concept.uid"),
                      nullable=False)
    de_datetime = Column(DateTime, nullable=False,
                         default=datetime.datetime.now())


class IdentifierRelationship(BASE):
    """
    tracks associations between identifiers (objects), i.e. which samples
    belong to which patient and which patient is in which referral
    """

    __tablename__ = "identifier_relationship"
    __table_args__ = {"schema": "nhse_contractural_metrics"}

    child_identifier_uid = Column(ForeignKey(
        "nhse_contractural_metrics.identifier.uid"), primary_key=True)
    parent_identifier_uid = Column(ForeignKey(
        "nhse_contractural_metrics.identifier.uid"), primary_key=True)
    type_cid = Column(ForeignKey("nhse_contractural_metrics.concept.uid"),
                      nullable=False)
    de_datetime = Column(DateTime, nullable=False,
                         default=datetime.datetime.now())


class Metric(BASE):
    """
    holds the metrics gathered against a particular identifier
    various different values can be stored for a single metric
    including a concept
    """

    __tablename__ = "metric"
    __table_args__ = {"schema": "nhse_contractural_metrics"}

    identifier_uid = Column(ForeignKey("nhse_contractural_metrics.identifier.uid"),
                            primary_key=True)
    type_cid = Column(ForeignKey("nhse_contractural_metrics.concept.uid"),
                      primary_key=True)
    value_cid = Column(ForeignKey("nhse_contractural_metrics.concept.uid"))
    value_integer = Column(Integer)
    value_numeric = Column(Numeric)
    value_boolean = Column(Boolean)
    value_string = Column(String)
    value_datetime = Column(DateTime)
    de_datetime = Column(DateTime, nullable=False,
                         default=datetime.datetime.now())


class Status(BASE):
    """
    holds status start and end date for different types of status
    against identifiers
    """

    __tablename__ = "status"
    __table_args__ = {"schema": "nhse_contractural_metrics"}


    uid = Column(UUID(as_uuid=True), primary_key=True,
                 server_default=text("uuid_generate_v4()"))
    status_type_cid = Column(ForeignKey("nhse_contractural_metrics.concept.uid"))
    start_datetime = Column(DateTime, nullable=False)
    end_datetime = Column(DateTime, nullable=False)
