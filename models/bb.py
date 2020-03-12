# coding: utf-8
from sqlalchemy import BigInteger, Boolean, CheckConstraint, Column, DateTime, ForeignKey, Integer, Numeric, SmallInteger, String, Text, UniqueConstraint, text
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class AuthGroup(Base):
    __tablename__ = 'auth_group'
    __table_args__ = {'schema': 'public'}

    id = Column(Integer, primary_key=True, server_default=text("nextval('\"public\".auth_group_id_seq'::regclass)"))
    name = Column(String(150), nullable=False, unique=True)


class AuthUser(Base):
    __tablename__ = 'auth_user'
    __table_args__ = {'schema': 'public'}

    id = Column(Integer, primary_key=True, server_default=text("nextval('\"public\".auth_user_id_seq'::regclass)"))
    password = Column(String(128), nullable=False)
    last_login = Column(DateTime(True))
    is_superuser = Column(Boolean, nullable=False)
    username = Column(String(150), nullable=False, unique=True)
    first_name = Column(String(30), nullable=False)
    last_name = Column(String(150), nullable=False)
    email = Column(String(254), nullable=False)
    is_staff = Column(Boolean, nullable=False)
    is_active = Column(Boolean, nullable=False)
    date_joined = Column(DateTime(True), nullable=False)


class BiobankIlluminaBatchcronhistory(Base):
    __tablename__ = 'biobank_illumina_batchcronhistory'
    __table_args__ = {'schema': 'public'}

    id = Column(Integer, primary_key=True, server_default=text("nextval('\"public\".biobank_illumina_batchcronhistory_id_seq'::regclass)"))
    created = Column(DateTime(True), nullable=False)
    type = Column(String(255), nullable=False)


class BiobankIlluminaBatchimporthistory(Base):
    __tablename__ = 'biobank_illumina_batchimporthistory'
    __table_args__ = {'schema': 'public'}

    id = Column(Integer, primary_key=True, server_default=text("nextval('\"public\".biobank_illumina_batchimporthistory_id_seq'::regclass)"))
    path = Column(Text, nullable=False, unique=True)
    filename = Column(Text, nullable=False, unique=True)
    created = Column(DateTime(True), nullable=False)
    status = Column(String(255), nullable=False)
    error_msgs = Column(Text)
    warning_msgs = Column(Text)
    submitted_by_code = Column(String(6))


class DjangoContentType(Base):
    __tablename__ = 'django_content_type'
    __table_args__ = (
        UniqueConstraint('app_label', 'model'),
        {'schema': 'public'}
    )

    id = Column(Integer, primary_key=True, server_default=text("nextval('\"public\".django_content_type_id_seq'::regclass)"))
    app_label = Column(String(100), nullable=False)
    model = Column(String(100), nullable=False)


class DjangoMigration(Base):
    __tablename__ = 'django_migrations'
    __table_args__ = {'schema': 'public'}

    id = Column(Integer, primary_key=True, server_default=text("nextval('\"public\".django_migrations_id_seq'::regclass)"))
    app = Column(String(255), nullable=False)
    name = Column(String(255), nullable=False)
    applied = Column(DateTime(True), nullable=False)


class AuthPermission(Base):
    __tablename__ = 'auth_permission'
    __table_args__ = (
        UniqueConstraint('content_type_id', 'codename'),
        {'schema': 'public'}
    )

    id = Column(Integer, primary_key=True, server_default=text("nextval('\"public\".auth_permission_id_seq'::regclass)"))
    name = Column(String(255), nullable=False)
    content_type_id = Column(ForeignKey('public.django_content_type.id', deferrable=True, initially='DEFERRED'), nullable=False, index=True)
    codename = Column(String(100), nullable=False)

    content_type = relationship('DjangoContentType')


class AuthUserGroup(Base):
    __tablename__ = 'auth_user_groups'
    __table_args__ = (
        UniqueConstraint('user_id', 'group_id'),
        {'schema': 'public'}
    )

    id = Column(Integer, primary_key=True, server_default=text("nextval('\"public\".auth_user_groups_id_seq'::regclass)"))
    user_id = Column(ForeignKey('public.auth_user.id', deferrable=True, initially='DEFERRED'), nullable=False, index=True)
    group_id = Column(ForeignKey('public.auth_group.id', deferrable=True, initially='DEFERRED'), nullable=False, index=True)

    group = relationship('AuthGroup')
    user = relationship('AuthUser')


class BiobankIlluminaGel1001(Base):
    __tablename__ = 'biobank_illumina_gel1001'
    __table_args__ = {'schema': 'public'}

    created = Column(DateTime(True), nullable=False)
    warning_msgs = Column(Text)
    row = Column(Integer)
    referral_id = Column(Text, nullable=False)
    clinical_indication_test_type_id = Column(Text, nullable=False)
    clinical_indication_test_type_uid = Column(UUID)
    patient_nhs_number = Column(String(10))
    patient_ngis_id = Column(Text, nullable=False)
    ordering_entity_id = Column(String(5))
    glh_laboratory_id = Column(String(5), nullable=False)
    primary_sample_received_date = Column(DateTime(True))
    patient_dob = Column(DateTime(True), nullable=False)
    primary_sample_id_received_glh = Column(Text)
    primary_sample_id_glh_lims = Column(Text, nullable=False)
    primary_sample_type = Column(String(255), nullable=False)
    primary_sample_state = Column(String(255), nullable=False)
    received_sample_topography = Column(Text)
    received_sample_morphology = Column(Text)
    received_sample_tumour_content = Column(Integer)
    received_sample_comments = Column(Text)
    received_sample_collection_date = Column(DateTime(True))
    dispatched_sample_id_glh_lims = Column(Text)
    dispatched_sample_lsid = Column(BigInteger, primary_key=True)
    dispatched_sample_type = Column(String(255), nullable=False)
    dispatched_sample_state = Column(String(255), nullable=False)
    dispatched_sample_volume_ul = Column(Integer, nullable=False)
    laboratory_remaining_volume_banked_ul = Column(Integer)
    glh_concentration_ng_ul = Column(Numeric(6, 2), nullable=False)
    glh_od_260_280 = Column(Numeric(4, 2), nullable=False)
    glh_din_value = Column(Numeric(4, 2))
    glh_percentage_dna = Column(Numeric(5, 2))
    glh_qc_status = Column(String(255), nullable=False)
    glh_sample_dispatch_date = Column(DateTime(True), nullable=False)
    glh_sample_consignment_number = Column(Text, nullable=False)
    plating_organisation = Column(String(255), nullable=False)
    gmc_rack_id = Column(Text, nullable=False)
    gmc_rack_well = Column(Text, nullable=False)
    dna_extraction_protocol = Column(String(255))
    prolonged_sample_storage = Column(String(255))
    retrospective_sample = Column(String(20), nullable=False)
    approved_by = Column(Text, nullable=False)
    referral_uid = Column(UUID, nullable=False)
    patient_uid = Column(UUID, nullable=False)
    referral = Column(JSONB(astext_type=Text()))
    patient = Column(JSONB(astext_type=Text()))
    clinical_indication = Column(JSONB(astext_type=Text()))
    tumour = Column(JSONB(astext_type=Text()))
    ordering_entity = Column(JSONB(astext_type=Text()))
    patient_mask = Column(JSONB(astext_type=Text()))
    samples = Column(JSONB(astext_type=Text()))
    is_proband = Column(Boolean, nullable=False)
    priority = Column(Text)
    disease_area = Column(String(255))
    clinic_sample_type = Column(String(255), nullable=False)
    received_sample_topography_uid = Column(UUID)
    received_sample_morphology_uid = Column(UUID)
    batch_import_id = Column(ForeignKey('public.biobank_illumina_batchimporthistory.id', deferrable=True, initially='DEFERRED'), index=True)
    clinical_indication_code = Column(Text)

    batch_import = relationship('BiobankIlluminaBatchimporthistory')


class BiobankIlluminaGel1004(BiobankIlluminaGel1001):
    __tablename__ = 'biobank_illumina_gel1004'
    __table_args__ = {'schema': 'public'}

    created = Column(DateTime(True), nullable=False)
    participant_id = Column(Text, nullable=False)
    group_id = Column(Text, nullable=False)
    disease_area = Column(String(255), nullable=False)
    gmc_rack_id = Column(Text, nullable=False)
    clinic_sample_type = Column(String(255), nullable=False)
    glh_sample_consignment_number = Column(Text, nullable=False)
    gel1001_id = Column(ForeignKey('public.biobank_illumina_gel1001.dispatched_sample_lsid', deferrable=True, initially='DEFERRED'), primary_key=True)
    laboratory_id = Column(String(5), nullable=False)
    laboratory_sample_volume = Column(Integer, nullable=False)
    gmc_rack_well = Column(Text, nullable=False)
    plating_organisation = Column(Text, nullable=False)
    priority = Column(Text)
    patient_uid = Column(Text)
    is_proband = Column(Boolean, nullable=False)
    retrospective_sample = Column(String(255), nullable=False)
    primary_sample_type = Column(String(255), nullable=False)
    batch_import_id = Column(ForeignKey('public.biobank_illumina_batchimporthistory.id', deferrable=True, initially='DEFERRED'), index=True)

    batch_import = relationship('BiobankIlluminaBatchimporthistory')


class BiobankIlluminaGel1005(BiobankIlluminaGel1001):
    __tablename__ = 'biobank_illumina_gel1005'
    __table_args__ = {'schema': 'public'}

    created = Column(DateTime(True), nullable=False)
    warning_msgs = Column(Text)
    row = Column(Integer)
    participant_id = Column(Text, nullable=False)
    laboratory_id = Column(String(5), nullable=False)
    sample_received = Column(String(3), nullable=False)
    sample_received_datetime = Column(DateTime(True))
    datetime_report_generated = Column(DateTime(True), nullable=False)
    patient_uid = Column(Text)
    batch_import_id = Column(ForeignKey('public.biobank_illumina_batchimporthistory.id', deferrable=True, initially='DEFERRED'), index=True)
    gel1001_id = Column(ForeignKey('public.biobank_illumina_gel1001.dispatched_sample_lsid', deferrable=True, initially='DEFERRED'), primary_key=True)

    batch_import = relationship('BiobankIlluminaBatchimporthistory')


class BiobankIlluminaGel1006(BiobankIlluminaGel1001):
    __tablename__ = 'biobank_illumina_gel1006'
    __table_args__ = {'schema': 'public'}

    created = Column(DateTime(True), nullable=False)
    warning_msgs = Column(Text)
    row = Column(Integer)
    gel1001_id = Column(ForeignKey('public.biobank_illumina_gel1001.dispatched_sample_lsid', deferrable=True, initially='DEFERRED'), primary_key=True)
    participant_id = Column(Text, nullable=False)
    biorepository_sample_volume = Column(Numeric(8, 2), nullable=False)
    biorepository_concentration = Column(Numeric(8, 2), nullable=False)
    biorepository_od260_280 = Column(Numeric(4, 2), nullable=False)
    din_value = Column(Numeric(8, 2), nullable=False)
    percentagednaover23kb = Column(Numeric(8, 2), nullable=False)
    biorepository_qc_status = Column(String(4), nullable=False)
    biorepository_dna_status = Column(Text)
    biorepository_deltacq = Column(Text)
    biorepository_agarose = Column(Text)
    patient_uid = Column(Text)
    batch_import_id = Column(ForeignKey('public.biobank_illumina_batchimporthistory.id', deferrable=True, initially='DEFERRED'), index=True)

    batch_import = relationship('BiobankIlluminaBatchimporthistory')


class BiobankIlluminaGel1007(BiobankIlluminaGel1001):
    __tablename__ = 'biobank_illumina_gel1007'
    __table_args__ = {'schema': 'public'}

    created = Column(DateTime(True), nullable=False)
    warning_msgs = Column(Text)
    row = Column(Integer)
    gel1001_id = Column(ForeignKey('public.biobank_illumina_gel1001.dispatched_sample_lsid', deferrable=True, initially='DEFERRED'), primary_key=True)
    client_name = Column(String(100))
    type = Column(String(100))
    location = Column(Text)
    position = Column(Text)
    rack_barcode = Column(Text)
    participant = Column(Text, nullable=False)
    patient_uid = Column(Text)
    batch_import_id = Column(ForeignKey('public.biobank_illumina_batchimporthistory.id', deferrable=True, initially='DEFERRED'), index=True)

    batch_import = relationship('BiobankIlluminaBatchimporthistory')


class BiobankIlluminaGel1001error(Base):
    __tablename__ = 'biobank_illumina_gel1001error'
    __table_args__ = {'schema': 'public'}

    id = Column(Integer, primary_key=True, server_default=text("nextval('\"public\".biobank_illumina_gel1001error_id_seq'::regclass)"))
    created = Column(DateTime(True), nullable=False)
    data = Column(JSONB(astext_type=Text()), nullable=False)
    error_msgs = Column(Text)
    row = Column(Integer)
    batch_import_id = Column(ForeignKey('public.biobank_illumina_batchimporthistory.id', deferrable=True, initially='DEFERRED'), index=True)

    batch_import = relationship('BiobankIlluminaBatchimporthistory')


class BiobankIlluminaGel1004error(Base):
    __tablename__ = 'biobank_illumina_gel1004error'
    __table_args__ = {'schema': 'public'}

    id = Column(Integer, primary_key=True, server_default=text("nextval('\"public\".biobank_illumina_gel1004error_id_seq'::regclass)"))
    created = Column(DateTime(True), nullable=False)
    data = Column(JSONB(astext_type=Text()), nullable=False)
    error_msgs = Column(Text)
    row = Column(Integer)
    batch_import_id = Column(ForeignKey('public.biobank_illumina_batchimporthistory.id', deferrable=True, initially='DEFERRED'), index=True)

    batch_import = relationship('BiobankIlluminaBatchimporthistory')


class BiobankIlluminaGel1005error(Base):
    __tablename__ = 'biobank_illumina_gel1005error'
    __table_args__ = {'schema': 'public'}

    id = Column(Integer, primary_key=True, server_default=text("nextval('\"public\".biobank_illumina_gel1005error_id_seq'::regclass)"))
    created = Column(DateTime(True), nullable=False)
    data = Column(JSONB(astext_type=Text()), nullable=False)
    error_msgs = Column(Text)
    row = Column(Integer)
    batch_import_id = Column(ForeignKey('public.biobank_illumina_batchimporthistory.id', deferrable=True, initially='DEFERRED'), index=True)

    batch_import = relationship('BiobankIlluminaBatchimporthistory')


class BiobankIlluminaGel1006error(Base):
    __tablename__ = 'biobank_illumina_gel1006error'
    __table_args__ = {'schema': 'public'}

    id = Column(Integer, primary_key=True, server_default=text("nextval('\"public\".biobank_illumina_gel1006error_id_seq'::regclass)"))
    created = Column(DateTime(True), nullable=False)
    data = Column(JSONB(astext_type=Text()), nullable=False)
    error_msgs = Column(Text)
    row = Column(Integer)
    batch_import_id = Column(ForeignKey('public.biobank_illumina_batchimporthistory.id', deferrable=True, initially='DEFERRED'), index=True)

    batch_import = relationship('BiobankIlluminaBatchimporthistory')


class BiobankIlluminaGel1007error(Base):
    __tablename__ = 'biobank_illumina_gel1007error'
    __table_args__ = {'schema': 'public'}

    id = Column(Integer, primary_key=True, server_default=text("nextval('\"public\".biobank_illumina_gel1007error_id_seq'::regclass)"))
    created = Column(DateTime(True), nullable=False)
    data = Column(JSONB(astext_type=Text()), nullable=False)
    error_msgs = Column(Text)
    row = Column(Integer)
    batch_import_id = Column(ForeignKey('public.biobank_illumina_batchimporthistory.id', deferrable=True, initially='DEFERRED'), index=True)

    batch_import = relationship('BiobankIlluminaBatchimporthistory')


class BiobankIlluminaGel1008error(Base):
    __tablename__ = 'biobank_illumina_gel1008error'
    __table_args__ = {'schema': 'public'}

    id = Column(Integer, primary_key=True, server_default=text("nextval('\"public\".biobank_illumina_gel1008error_id_seq'::regclass)"))
    created = Column(DateTime(True), nullable=False)
    data = Column(JSONB(astext_type=Text()), nullable=False)
    error_msgs = Column(Text)
    row = Column(Integer)
    batch_import_id = Column(ForeignKey('public.biobank_illumina_batchimporthistory.id', deferrable=True, initially='DEFERRED'), index=True)

    batch_import = relationship('BiobankIlluminaBatchimporthistory')


class BiobankIlluminaGel1008plate(Base):
    __tablename__ = 'biobank_illumina_gel1008plate'
    __table_args__ = {'schema': 'public'}

    plate_id = Column(Text, primary_key=True, index=True)
    created = Column(DateTime(True), nullable=False)
    warning_msgs = Column(Text)
    batch_import_id = Column(ForeignKey('public.biobank_illumina_batchimporthistory.id', deferrable=True, initially='DEFERRED'), index=True)
    type_of_case = Column(String(2))

    batch_import = relationship('BiobankIlluminaBatchimporthistory')


class BiobankIlluminaGel1009error(Base):
    __tablename__ = 'biobank_illumina_gel1009error'
    __table_args__ = {'schema': 'public'}

    id = Column(Integer, primary_key=True, server_default=text("nextval('\"public\".biobank_illumina_gel1009error_id_seq'::regclass)"))
    created = Column(DateTime(True), nullable=False)
    data = Column(JSONB(astext_type=Text()), nullable=False)
    error_msgs = Column(Text)
    row = Column(Integer)
    batch_import_id = Column(ForeignKey('public.biobank_illumina_batchimporthistory.id', deferrable=True, initially='DEFERRED'), index=True)

    batch_import = relationship('BiobankIlluminaBatchimporthistory')


class BiobankIlluminaGel1010error(Base):
    __tablename__ = 'biobank_illumina_gel1010error'
    __table_args__ = {'schema': 'public'}

    id = Column(Integer, primary_key=True, server_default=text("nextval('\"public\".biobank_illumina_gel1010error_id_seq'::regclass)"))
    created = Column(DateTime(True), nullable=False)
    data = Column(JSONB(astext_type=Text()), nullable=False)
    error_msgs = Column(Text)
    row = Column(Integer)
    batch_import_id = Column(ForeignKey('public.biobank_illumina_batchimporthistory.id', deferrable=True, initially='DEFERRED'), index=True)

    batch_import = relationship('BiobankIlluminaBatchimporthistory')


class BiobankIlluminaHistoricalgel1001(Base):
    __tablename__ = 'biobank_illumina_historicalgel1001'
    __table_args__ = {'schema': 'public'}

    created = Column(DateTime(True), nullable=False)
    warning_msgs = Column(Text)
    row = Column(Integer)
    referral_id = Column(Text, nullable=False)
    clinical_indication_test_type_id = Column(Text, nullable=False)
    clinical_indication_test_type_uid = Column(UUID)
    patient_nhs_number = Column(String(10))
    patient_ngis_id = Column(Text, nullable=False)
    ordering_entity_id = Column(String(5))
    glh_laboratory_id = Column(String(5), nullable=False)
    primary_sample_received_date = Column(DateTime(True))
    patient_dob = Column(DateTime(True), nullable=False)
    primary_sample_id_received_glh = Column(Text)
    primary_sample_id_glh_lims = Column(Text, nullable=False)
    primary_sample_type = Column(String(255), nullable=False)
    primary_sample_state = Column(String(255), nullable=False)
    received_sample_topography = Column(Text)
    received_sample_morphology = Column(Text)
    received_sample_tumour_content = Column(Integer)
    received_sample_comments = Column(Text)
    received_sample_collection_date = Column(DateTime(True))
    dispatched_sample_id_glh_lims = Column(Text)
    dispatched_sample_lsid = Column(BigInteger, nullable=False, index=True)
    dispatched_sample_type = Column(String(255), nullable=False)
    dispatched_sample_state = Column(String(255), nullable=False)
    dispatched_sample_volume_ul = Column(Integer, nullable=False)
    laboratory_remaining_volume_banked_ul = Column(Integer)
    glh_concentration_ng_ul = Column(Numeric(6, 2), nullable=False)
    glh_od_260_280 = Column(Numeric(4, 2), nullable=False)
    glh_din_value = Column(Numeric(4, 2))
    glh_percentage_dna = Column(Numeric(5, 2))
    glh_qc_status = Column(String(255), nullable=False)
    glh_sample_dispatch_date = Column(DateTime(True), nullable=False)
    glh_sample_consignment_number = Column(Text, nullable=False)
    plating_organisation = Column(String(255), nullable=False)
    gmc_rack_id = Column(Text, nullable=False)
    gmc_rack_well = Column(Text, nullable=False)
    dna_extraction_protocol = Column(String(255))
    prolonged_sample_storage = Column(String(255))
    retrospective_sample = Column(String(20), nullable=False)
    approved_by = Column(Text, nullable=False)
    referral_uid = Column(UUID, nullable=False)
    patient_uid = Column(UUID, nullable=False)
    referral = Column(JSONB(astext_type=Text()))
    patient = Column(JSONB(astext_type=Text()))
    clinical_indication = Column(JSONB(astext_type=Text()))
    tumour = Column(JSONB(astext_type=Text()))
    ordering_entity = Column(JSONB(astext_type=Text()))
    patient_mask = Column(JSONB(astext_type=Text()))
    samples = Column(JSONB(astext_type=Text()))
    is_proband = Column(Boolean, nullable=False)
    priority = Column(Text)
    disease_area = Column(String(255))
    clinic_sample_type = Column(String(255), nullable=False)
    received_sample_topography_uid = Column(UUID)
    received_sample_morphology_uid = Column(UUID)
    history_id = Column(Integer, primary_key=True, server_default=text("nextval('\"public\".biobank_illumina_historicalgel1001_history_id_seq'::regclass)"))
    history_date = Column(DateTime(True), nullable=False)
    history_change_reason = Column(String(100))
    history_type = Column(String(1), nullable=False)
    batch_import_id = Column(Integer, index=True)
    history_user_id = Column(ForeignKey('public.auth_user.id', deferrable=True, initially='DEFERRED'), index=True)
    history_relation_id = Column(BigInteger, nullable=False, index=True)
    clinical_indication_code = Column(Text)

    history_user = relationship('AuthUser')


class DjangoAdminLog(Base):
    __tablename__ = 'django_admin_log'
    __table_args__ = (
        CheckConstraint('action_flag >= 0'),
        {'schema': 'public'}
    )

    id = Column(Integer, primary_key=True, server_default=text("nextval('\"public\".django_admin_log_id_seq'::regclass)"))
    action_time = Column(DateTime(True), nullable=False)
    object_id = Column(Text)
    object_repr = Column(String(200), nullable=False)
    action_flag = Column(SmallInteger, nullable=False)
    change_message = Column(Text, nullable=False)
    content_type_id = Column(ForeignKey('public.django_content_type.id', deferrable=True, initially='DEFERRED'), index=True)
    user_id = Column(ForeignKey('public.auth_user.id', deferrable=True, initially='DEFERRED'), nullable=False, index=True)

    content_type = relationship('DjangoContentType')
    user = relationship('AuthUser')


class AuthGroupPermission(Base):
    __tablename__ = 'auth_group_permissions'
    __table_args__ = (
        UniqueConstraint('group_id', 'permission_id'),
        {'schema': 'public'}
    )

    id = Column(Integer, primary_key=True, server_default=text("nextval('\"public\".auth_group_permissions_id_seq'::regclass)"))
    group_id = Column(ForeignKey('public.auth_group.id', deferrable=True, initially='DEFERRED'), nullable=False, index=True)
    permission_id = Column(ForeignKey('public.auth_permission.id', deferrable=True, initially='DEFERRED'), nullable=False, index=True)

    group = relationship('AuthGroup')
    permission = relationship('AuthPermission')


class AuthUserUserPermission(Base):
    __tablename__ = 'auth_user_user_permissions'
    __table_args__ = (
        UniqueConstraint('user_id', 'permission_id'),
        {'schema': 'public'}
    )

    id = Column(Integer, primary_key=True, server_default=text("nextval('\"public\".auth_user_user_permissions_id_seq'::regclass)"))
    user_id = Column(ForeignKey('public.auth_user.id', deferrable=True, initially='DEFERRED'), nullable=False, index=True)
    permission_id = Column(ForeignKey('public.auth_permission.id', deferrable=True, initially='DEFERRED'), nullable=False, index=True)

    permission = relationship('AuthPermission')
    user = relationship('AuthUser')


class BiobankIlluminaGel1008(Base):
    __tablename__ = 'biobank_illumina_gel1008'
    __table_args__ = {'schema': 'public'}

    created = Column(DateTime(True), nullable=False)
    warning_msgs = Column(Text)
    row = Column(Integer)
    plate_well_id = Column(Text, primary_key=True, index=True)
    participant_id = Column(Text)
    normalised_biorepository_sample_volume = Column(Numeric(6, 2))
    normalised_biorepository_concentration = Column(Numeric(4, 2))
    well_id = Column(Text, nullable=False)
    plate_consignment_number = Column(Text, nullable=False)
    plate_date_of_dispatch = Column(DateTime(True), nullable=False)
    patient_uid = Column(Text)
    batch_import_id = Column(ForeignKey('public.biobank_illumina_batchimporthistory.id', deferrable=True, initially='DEFERRED'), index=True)
    gel1001_id = Column(ForeignKey('public.biobank_illumina_gel1001.dispatched_sample_lsid', deferrable=True, initially='DEFERRED'), index=True)
    plate_id = Column(ForeignKey('public.biobank_illumina_gel1008plate.plate_id', deferrable=True, initially='DEFERRED'), nullable=False, index=True)
    well_type = Column(String(6))

    batch_import = relationship('BiobankIlluminaBatchimporthistory')
    gel1001 = relationship('BiobankIlluminaGel1001')
    plate = relationship('BiobankIlluminaGel1008plate')


class BiobankIlluminaGel1009(BiobankIlluminaGel1008):
    __tablename__ = 'biobank_illumina_gel1009'
    __table_args__ = {'schema': 'public'}

    created = Column(DateTime(True), nullable=False)
    patient_id = Column(Text)
    group_id = Column(Text)
    sample_id = Column(BigInteger, index=True)
    plate_barcode = Column(Text, nullable=False)
    well = Column(String(3), nullable=False)
    gel1008_id = Column(ForeignKey('public.biobank_illumina_gel1008.plate_well_id', deferrable=True, initially='DEFERRED'), primary_key=True, index=True)
    species = Column(Text)
    gender = Column(String(20))
    volume_ul = Column(Integer)
    concentration_ng_ul = Column(Numeric(6, 2))
    od_260_280 = Column(Numeric(4, 2))
    tissue_source = Column(Text)
    extraction_method = Column(String(255))
    ethnicity = Column(String(1))
    parent_1_id = Column(Text)
    parent_2_id = Column(Text)
    replicate_id = Column(Text)
    cancer_sample_y_n = Column(String(3))
    is_longitudinal = Column(Boolean)
    matched_sample_id = Column(Text)
    matched_sample_type = Column(String(200))
    comment = Column(Text)
    coverage = Column(Text)
    due_date = Column(DateTime(True))
    analysis = Column(Text)
    so = Column(Text)
    sample_prep_workflow = Column(Text)
    sample_type = Column(String(255))
    instrument_type = Column(Text)
    delta_cq = Column(Text)
    plate_date_of_dispatch = Column(DateTime(True), nullable=False)
    plate_consignment_number = Column(Text, nullable=False)
    priority = Column(String(255))
    type_of_case = Column(String(255))
    masked_pid = Column(Text)
    program = Column(String(255))
    delivery_type = Column(String(255))
    molecule = Column(String(255))
    tissue_prep = Column(String(255))
    source = Column(String(255))
    low_dna_bool = Column(Boolean)
    is_repeat = Column(Boolean, nullable=False)
    batch_import_id = Column(ForeignKey('public.biobank_illumina_batchimporthistory.id', deferrable=True, initially='DEFERRED'), index=True)
    row = Column(Integer)

    batch_import = relationship('BiobankIlluminaBatchimporthistory')


class BiobankIlluminaGel1010(BiobankIlluminaGel1008):
    __tablename__ = 'biobank_illumina_gel1010'
    __table_args__ = {'schema': 'public'}

    created = Column(DateTime(True), nullable=False)
    warning_msgs = Column(Text)
    row = Column(Integer)
    gel1008_id = Column(ForeignKey('public.biobank_illumina_gel1008.plate_well_id', deferrable=True, initially='DEFERRED'), primary_key=True, index=True)
    illumina_qc_status = Column(String(4), nullable=False)
    illumina_sample_concentration = Column(Numeric(6, 2), nullable=False)
    illumina_sequence_gender = Column(Text)
    illumina_delta_cq = Column(Numeric(4, 2))
    dna_amount = Column(Numeric(4, 2))
    laboratory_sample_id = Column(BigInteger, index=True)
    batch_import_id = Column(ForeignKey('public.biobank_illumina_batchimporthistory.id', deferrable=True, initially='DEFERRED'), index=True)

    batch_import = relationship('BiobankIlluminaBatchimporthistory')
