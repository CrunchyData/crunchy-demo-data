# Weather observations from San Benito County, CA, USA 
This data is from a weather station starting in March 1, 1998 until August 16th 2020.

Here is some of the metadata
County: San Benito
Latitude/Longitude: 36 deg 49 min N / 121 deg 28 min W 	Elevation: 245 ft

Data was downloaded from here
http://ipm.ucanr.edu/calludt.cgi/WXSTATIONDATA?MAP=&STN=SJ_VALLEY.A

On Aug. 17th 2020.

Data was then cleaned to: 
1. remove mostly blank columns so that the only remaining columns are
```sql
id       | integer           |           | not null | nextval('weather_id_seq'::regclass)
 date     | character varying |           |          |
 time     | character varying |           |          |
 precip   | character varying |           |          |
 air max  | character varying |           |          |
 min      | character varying |           |          |
 soil max | character varying |           |          |
 min_1    | character varying |           |          |
 solar    | character varying |           |          |
 eto      | character varying |           |          |
 rh max   | character varying |           |          |
 min_2    | character varying |           |          |
```
2. renamed columns
```sql
alter table weather rename "air max" to "air_max_temp";
alter table weather rename "min" to "air_min_temp";
alter table weather rename "soil max" to "soil_max_temp";
alter table weather rename "min_1" to "soil_min_temp";
alter table weather rename "rh max" to "rh_max";
alter table weather rename "min_2" to "rh_min";
```

3. Made a new column to hold concatenated time and date
```sql
 alter table weather add column date_time timestamp;
``` 
4. updated some time values from 24:00 (invalid) to 23:59
```sql
fire=# update weather set  time = '23:59' where date = '20101221';
```

5. update 
```sql
update weather set date_time = to_timestamp((date || ' ' || time || '-7'), 'YYYYMMDD HH24:MI');
UPDATE 8205
``` 

6. Then removed the date and the time column
```sql
alter table weather drop column "date";
alter table weather drop column "time";
```

7. Then made all the columns the right data type
```sql
alter table weather alter column precip type numeric(5,2) using precip::numeric(5,2);
alter table weather alter column air_max_temp type smallint using air_max_temp::smallint;
alter table weather alter column air_min_temp type smallint using air_min_temp::smallint;
alter table weather alter column soil_max_temp type smallint using soil_max_temp::smallint;
alter table weather alter column soil_min_temp type smallint using soil_min_temp::smallint;
alter table weather alter column solar type smallint using solar::smallint;
alter table weather alter column eto type numeric(5,2) using eto::numeric(5,2);
alter table weather alter column rh_max type numeric(5,2) using rh_max::numeric(5,2);
alter table weather alter column rh_min type numeric(5,2) using rh_min::numeric(5,2);
```

exported with:
```
pg_dump -h localhost -U postgres -Fp --compress=9 --no-owner --no-privileges -d fire -t 'fire19*' -t 'weather'  -f crunchy-demo-fire.dump.sql.gz
```

imports with
```
gunzip -c crunchy-demo-fire.dump.sql.gz |psql -h localhost -U postgres -p 5432 fire
```