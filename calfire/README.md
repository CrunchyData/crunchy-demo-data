# CalFire historical perimeter data
This data contains perimeter boundaries for historical fires in California through the end of the 2019 fire season. We also include the table for the fire region names and 3 letter abbreviations. 

The purpose of this data was to do predictive fire modeling with the weather data set. That data starts at March 3rd 1998. Therefore, to reduce file size, we removed all fire perimeters pre March 3rd 1998.  

There was an obvious typo in the original data set for one fire that we corrected the year 
from 2106 to 2016. 

We did not extract any of the prescribed fires or legacy fires from fire19_1.gdb nor did we extract any of the line data from cfadmin19_1.gdb

There was no dictionary provided to translate the integer for cause of fire to a text string.
All the data was downloaded as ESRI filegeodb and then translated in QGIS 3.14.15 to either direct import to PostGIS or PostgreSQL dump files.

The data is in EPSG:3310 which is valid for all of California and has units of meters so there was no reason to project to another CRS or use a Geometry type in Postgis.


All data is from this site:
https://frap.fire.ca.gov/mapping/gis-data/

-----------------------------------

Conversion from a Filegeodb to a geopackage in QGIS altered some of the column types. We had to restore some of the column types:

Then made all the columns the right data type
```sql
alter table fire19 alter column alarm_date type date using alarm_date::date;
alter table fire19 alter column cont_date type date using cont_date::date;
```

exported with:
```
pg_dump -h localhost -U postgres -Fp --compress=9 --no-owner --no-privileges -d fire -t 'fire19*' -t 'weather'  -f crunchy-demo-fire.dump.sql.gz
```

imports with
```
gunzip -c crunchy-demo-fire.dump.sql.gz |psql -h localhost -U postgres -p 5432 fire
```