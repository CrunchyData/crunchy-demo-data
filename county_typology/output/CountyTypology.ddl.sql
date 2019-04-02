CREATE TABLE county_typology
(
  fipsid varchar(5),
  state  char(2),
  name text,
  is_metro boolean,
  econ_type smallint,
  econ_type_txt text,
  is_farming boolean,
  is_mining boolean,
  is_manufacturing boolean,
  is_govt boolean,
  is_recreation boolean,
  is_nonspecialized boolean,
  is_low_education boolean,
  is_low_employment boolean,
  had_pop_loss boolean,
  is_retirement_dest boolean,
  has_pers_poverty boolean,
  has_pers_child_poverty boolean
);

create index countytopo_state_indx on county_typology (state);
create index countytopo_name_indx on county_typology (name);
create index countytopo_econtype_txt_indx on county_typology (econ_type_txt);

-- Then assuming your shell is in this directory you can do
-- \COPY county_typology from '../2015CountyTypologyCodes.csv' with CSV HEADER