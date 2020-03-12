/* alter the table owners*/
alter table nhse_contractural_metrics.concept owner to cdt_user;
alter table nhse_contractural_metrics.identifier owner to cdt_user;
alter table nhse_contractural_metrics.identifier_relationship owner to cdt_user;
alter table nhse_contractural_metrics.metric owner to cdt_user;
alter table nhse_contractural_metrics.status owner to cdt_user;

/* constraint to prevent more than one value being entered for a single metric*/
alter table nhse_contractural_metrics.metric
add constraint only_one_non_null check (
    (value_integer is not null)::integer +
    (value_numeric is not null)::integer +
    (value_boolean is not null)::integer +
    (value_string is not null)::integer +
    (value_datetime is not null)::integer +
    (value_cid is not null)::integer
    = 1
);

