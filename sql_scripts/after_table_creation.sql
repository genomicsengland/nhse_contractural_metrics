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

/* trigger function to copy row into archives table */
/* metrics table */
create table nhse_contractural_metrics.metric_archive (
	uid uuid not null default uuid_generate_v4(),
	identifier_uid uuid not null,
	type_cid uuid not null,
	value_cid uuid null,
	value_integer int4 null,
	value_numeric numeric null,
	value_boolean bool null,
	value_string varchar null,
	value_datetime timestamp null,
	de_datetime timestamp not null,
	valid_from_datetime timestamptz not null default now(),
	valid_to_datetime timestamptz
);
/* function */
create or replace function nhse_contractural_metrics.metric_archive_f ()
returns trigger
as
$$
begin
update nhse_contractural_metrics.metric_archive
set valid_to_datetime = now()
where identifier_uid = new.identifier_uid and type_cid = new.type_cid and valid_to_datetime is null;
insert into nhse_contractural_metrics.metric_archive
    (
        identifier_uid,
        type_cid,
        value_cid,
        value_integer,
        value_numeric,
        value_boolean,
        value_string,
        value_datetime,
        de_datetime
    )
    values
    (
        new.identifier_uid,
        new.type_cid,
        new.value_cid,
        new.value_integer,
        new.value_numeric,
        new.value_boolean,
        new.value_string,
        new.value_datetime,
        new.de_datetime
    );
return new;
end;
$$
language plpgsql;
alter function nhse_contractural_metrics.metric_archive_f owner to cdt_user;
/* trigger */
create trigger metric_archive_t
after insert or update
on nhse_contractural_metrics.metric
for each row
execute procedure nhse_contractural_metrics.metric_archive_f();


