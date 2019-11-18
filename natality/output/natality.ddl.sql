CREATE TABLE natality
(
notes text,
county text,
county_code char(5) PRIMARY KEY,
births int,
total_population int,
birth_rate numeric(8,2),
female_population int,
fertility_rate numeric(8,2),
mean_birth_weight numeric(8,2),
std_dev_birth_weight numeric(8,2),
mean_age_mother numeric(8,2),
std_dev_age_mother numeric(8,2),
mean_lmp_gest_age numeric(8,2),
st_dev_lmp_gest_age numeric(8,2),
mean_obs_est_gest_age numeric(8,2),
std_dev_obs_est_gest_age numeric(8,2)
)


-- Then assuming your shell is in this directory you can do
-- psql -h 192.168.99.100 -U groot -c '\COPY natality from '\''./Natality-2007-2017-1.txt'\'' with CSV HEADER' workshop