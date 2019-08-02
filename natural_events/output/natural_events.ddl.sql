create table natural_events
(
    id text primary key,
    json_content jsonb
);

-- The default GIN operator class for jsonb supports queries with top-level key-exists operators ?, ?& and ?| operators and path/value-exists operator @>
-- https://www.postgresql.org/docs/11/datatype-json.html#JSON-INDEXING
create index natural_events_json_content_indx on natural_events using gin (json_content);

--Then to load the data
--PGPASSWORD="password" psql -h localhost -U groot -d workshop -c '\COPY natural_events from '\''./natural_events.csv'\'' WITH DELIMITER '\''|'\'' '