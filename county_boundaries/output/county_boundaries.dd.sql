CREATE TABLE county_geometry
(
  id SMALLSERIAL PRIMARY KEY, --not in the file

  statefp CHAR(2), -- Current state FIPS code
  countyfp CHAR(3), -- Current county FIPS code
  countyns CHAR(8), -- Current county GNIS code
  geoid CHAR(5), -- The GEOID attribute is a concatenation of the state FIPS code followed by the county FIPS code.
  county_name TEXT, -- National Standard Codes (ANSI INCITS 31-2009), Federal Information Processing Series (FIPS) - Counties/County Equivalents
  namelsad TEXT, -- current name and the translated legal/statistical area description for county
--  lsad CHAR(2), -- Current legal/statistical area description code for county
--  classfp CHAR(2), -- Current Federal Information Processing Series (FIPS) class code
--  mtfcc CHAR(5), excluded bc these would all be G4040 =  County or Equivalent Feature
--  csafp CHAR(3), excluded bc these are mostly null
--  cbsafp CHAR(5), excluded bc these are mostly null
--  metdivfp CHAR(5), excluded bc these are mostly null
  funcstat CHAR(1), -- Current functional status
  aland BIGINT,  --area of land in m2
  awater BIGINT, --area of water in m2
  interior_pnt geometry(POINT, 4326), --generated from geom in the file
  the_geom geometry(MULTIPOLYGON,4326) --generated from geom in the file
);
create index countygeom_interiorpt_indx on county_geometry using gist (interior_pnt);
create index countygeom_the_geom_indx on county_geometry using gist (the_geom);
create index countygeom_geoid_indx on county_geometry (geoid);

-- then use the copy command like so
-- \COPY county_geometry (statefp, countyfp, countyns, geoid, county_name, namelsad, funcstat, aland, awater, interior_pnt, the_geom) from '~/git/crunchydemodata/county_boundaries/output/county_boundaries_copy.txt' WITH CSV QUOTE '"';