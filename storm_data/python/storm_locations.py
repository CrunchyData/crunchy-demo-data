from shapely.geometry import shape
from shapely.geometry import Point
from shapely.wkb import dumps
import csv

import pprint

if __name__ == '__main__':

    # read a line from the file
    with open('../data/StormEvents_locations-ftp_v1.0_d2018_c20190130.csv', 'r' ) as input_file:
        csv_file = csv.DictReader(input_file)
        with open("../output/storm_locations_copy.txt", "w") as output:
            for i, line in enumerate(csv_file):
                if i > 0:
                    output.write(line['EPISODE_ID'] + ',' + line['EVENT_ID'] + ',' + line['LOCATION_INDEX'] + ',' + line['RANGE'] + ',"' + line['AZIMUTH'] + '","')
                    output.write(line['LOCATION'] + '",' + line['LATITUDE'] + ',' + line['LONGITUDE'] + ',')
                    lat = float(line['LATITUDE'])
                    lon = float(line['LONGITUDE'])

                    the_point = Point(lon, lat)
                    output.write(dumps(the_point, hex=True, include_srid=True, srid=4326) + '\n')

    print("done")
