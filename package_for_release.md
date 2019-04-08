# Package the data for release

1. Run the county_boundaries, storm_data, and wikipedia python scripts
    * we don't change county typology
    * Update the readme in Wikipedia to reflect the date you are running the script
2. Make a new directory to store all the data and ddl and call it crunchy_demo_data
3. Inside that directory make a directory for county_boundaries, county_typology, storm_data, and wikipedia
4. For each directory copy in the README, the codebook, the DDL, and the data for the copy command
5. Then zip up all the contents into crunchy_demo_data_vX.X.zip where X.X is the tag for the data
6. Upload this file with the release
7. Notify the authors in Crunchy-katacoda that there is a new data release if they want to update