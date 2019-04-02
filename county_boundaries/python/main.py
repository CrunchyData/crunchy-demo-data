import fiona
from shapely.geometry import shape
from shapely.geometry import Point
from shapely.geometry import Polygon
from shapely.geometry import MultiPolygon
from shapely.wkb import dumps
import pprint



with fiona.open("../shapefile/tl_2018_us_county.shp", "r") as features:
    pprint.pprint(next(features))
    pprint.pprint(features.crs)
    with open("../output/county_boundaries_copy.txt", "w") as output:
        for item in features:
            #pprint.pprint(item['id'])
            output.write('"'+ item['properties']['STATEFP'] + '","')
            output.write(item['properties']['COUNTYFP'] + '","')
            output.write(item['properties']['COUNTYNS'] + '","')
            output.write(item['properties']['GEOID'] + '","')
            output.write(item['properties']['NAME'] + '","')
            output.write(item['properties']['NAMELSAD'] + '","')
            output.write(item['properties']['FUNCSTAT'] + '",')
            output.write(str(item['properties']['ALAND']) + ',')
            output.write(str(item['properties']['AWATER']) + ',')

            lat = float(item['properties']['INTPTLAT'])
            lon = float(item['properties']['INTPTLON'])
            the_point = Point(lon, lat)

            output.write(dumps(the_point, hex=True, include_srid=True, srid=4326) + ',')

            geom = None
            try:
                geom = MultiPolygon(item['geometry'])
            except:
                tempgeom = shape(item['geometry'])
                geom = MultiPolygon([tempgeom])
            output.write(dumps(geom, hex=True, include_srid=True, srid=4326))

            output.write('\n')

print("Done")
