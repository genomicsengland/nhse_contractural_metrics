# NHSE Contractural Metrics

This repository holds the scripts and data required to build the contractural metrics datasets sent to GLHs, for ultimate submission to NHSE.
The two main scripts, `ncm_mgmt.py` and `ncm_run.py` hold various functions for managing and running the enclosed ETLs.

The database to which the ETLs write is composed of the following tables and relationships:

* `identifier` holding all identifiers assigned to the objects that metrics are generated against e.g. samples, patients, referrals;
* `identifier_relationship` holding the 1:1 relationships between identifiers, i.e. which sample belongs to which patient, and which referral that patient is in;
* `concept` holds all of the enumerations used throughout the database (where a field ends with `_cid`), the table is assembled from the `nhse_contractural_metrics_reference.c_*` tables which themselves are assembled from the fiels within the `metric` folder;
* `metric` holds all metrics (singular pieces of data) associated with an identifier, the value of the metric is given in one (and only one) of the `value_` columns, and the type of metric is given by the `type_cid` column;
* `metric_archive` is a copy of the `metric` table which is appended to any time a new record is added to `metric`.
The `valid_from_datetime` is set to the current datetime when the row is created, and the `valid_to_datetime` column of any rows having the same value in `identifier_uid` and `type_cid` as the new row is updated to the current datetime, therefore allowing the value of a given metric to be taken at any point in time.
* `status` TBD
