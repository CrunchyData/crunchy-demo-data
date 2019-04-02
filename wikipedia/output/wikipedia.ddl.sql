create table wikipedia
(
  id SMALLSERIAL PRIMARY KEY, --not in the file
  county text,
  state text,
  json_content jsonb,
  response_attr hstore

);

-- hstore has GiST and GIN index support for the @>, ?, ?& and ?|
-- https://www.postgresql.org/docs/11/hstore.html#id-1.11.7.25.6
create index wikipedia_response_attr_indx on wikipedia using gist (response_attr);

-- The default GIN operator class for jsonb supports queries with top-level key-exists operators ?, ?& and ?| operators and path/value-exists operator @>
-- https://www.postgresql.org/docs/11/datatype-json.html#JSON-INDEXING
create index wikipedia_json_content_indx on wikipedia using gin (json_content);

-- A multicolumn B-tree index can be used with query conditions that involve any subset of the index's columns,
-- but the index is most efficient when there are constraints on the leading (leftmost) columns
-- https://www.postgresql.org/docs/11/indexes-multicolumn.html
-- Our queries will usually set the state and then look the county
create index wikipedia_county_state_indx on wikipedia (state, county);

--then load data with
-- \copy wikipedia (county, state, json_content, response_attr) from './wikipedia_copy.txt' WITH CSV QUOTE '^'
