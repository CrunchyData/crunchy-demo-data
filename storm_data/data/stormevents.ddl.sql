-- we are going to create all three tables here

--removed all
  -- from BEGIN_YEARMONTH up to and including END_TIME
  -- flood_cause
  -- category
  -- tor_
  -- from begin_range up to and including end_lon (these are not documented in the data dictionary)
-- The data did not include last_date_modified and last_date_certified
create table se_details (
    episode_id int,
    event_id int primary key,
    state text,
    state_fips smallint,
    event_year smallint,
    month_name text,
    event_type text,
    cz_type char(1),
    cz_fips smallint,
    cz_name text,
    wfo char(3),
    begin_date_time timestamp,
    cz_timezone text,
    end_date_time timestamp,
    injuries_direct int,
    injuries_indirect int,
    deaths_direct int,
    deaths_indirect int,
    damage_property text,
    damage_crops text,
    source text,
    magnitude float,
    magnitude_type char(2),
    episode_narrative text,
    event_narrative text
);

-- then import the data
-- \copy se_details from '/home/spousty/git/crunchydemodata/storm_data/data/StormEvents_details-ftp_v1.0_d2018_c20190130.csv' WITH CSV HEADER\copy se_details from '/home/spousty/git/crunchydemodata/storm_data/data/StormEvents_details-ftp_v1.0_d2018_c20190130.csv' WITH CSV HEADER


--removed all
  -- from FAT_YEARMONTH up to and including FAT_TIME
  -- EVENT_YEARMONTH
create table se_fatalities (
  fatality_id int primary key,
  event_id int,
  fatality_type char(1),
  fatality_date timestamp,
  fatality_age smallint,
  fatality_sex char(1),
  fatality_location text
);
    create index strm_fatal_idx on se_fatalities(event_id);
-- \copy se_fatalities from './StormEvents_fatalities-ftp_v1.0_d2018_c20190130.csv' with CSV HEADER


create table se_locations (
  locationid serial primary key,
  episode_id int,
  event_id int,
  location_index smallint,
  range real,
  azimuth varchar(6),
  location text,
  latitude real,
  longitude real,
  the_geom geometry(POINT, 4326)
);
create index selocation_pt_indx on se_locations using gist (the_geom);
create index selocation_event_indx on se_locations(event_id);
create index selocation_episode_indx on se_locations(episode_id);

--\copy se_locations (episode_id, event_id, location_index, range, azimuth, location, latitude, longitude, the_geom) from '../output/storm_locations_copy.txt' WITH CSV QUOTE '"';
