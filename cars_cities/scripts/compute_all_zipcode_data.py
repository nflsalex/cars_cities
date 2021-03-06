from os import path
import sys

import shapefile

from constants import CACHE_DIR, SHAPEFILE_DIR, CONVEXHULL_DIR, CITY_IDS, PROJECTION_FILE
from utils import pickle_load, pickle_save


def format_zipcode(zipcode):
    zipcode = str(zipcode)
    while len(zipcode) < 5:
        zipcode = '0' + zipcode
    return zipcode
    
if __name__=='__main__':
    all_cars_data = pickle_load(path.join(CACHE_DIR, 'all_cars_data'))
    all_census_data = pickle_load(path.join(CACHE_DIR, 'all_census_data'))
    reader = shapefile.Reader(path.join(CACHE_DIR, 'zipcodes/zip_poly/zip_poly'))
    
    zipcodeList = {}
    for key, data in all_cars_data.iteritems():
        zipcode = data[94]
        cityid = int(data[95])
        formatted_zipcode = format_zipcode(zipcode)

        if formatted_zipcode not in zipcodeList:
            zipcodeList[formatted_zipcode] = 1
   

    print 'Reading polygon file...'
    zip_poly = {}
    for sr in reader.shapeRecords():
        if sr.record[0] in zipcodeList:
            polygon = sr.shape.points
            zip_poly[str(sr.record[0])] = map(lambda x: [x[1], x[0]], polygon)
    print 'Finished reading polygon file!'


    print 'Writing city zipcodes file'
    city_zipcode_data = {}
    for key, data in all_cars_data.iteritems():
        zipcode = data[94]
        cityid = int(data[95])
   
         
            
        formatted_zipcode = format_zipcode(zipcode)
        
        if (formatted_zipcode not in city_zipcode_data) and  (formatted_zipcode in zip_poly):
            city_zipcode_data[formatted_zipcode] = {}
            poly = zip_poly[formatted_zipcode]
            city_zipcode_data[formatted_zipcode]['polygon'] = poly
            print "adding %s" % formatted_zipcode
        else:
            pass
            
        
    print 'Saving pickle files'
    pickle_save(city_zipcode_data, path.join(CACHE_DIR, 'zipcodes/pickled/allCities'))
      
        
    print 'Finished!'
        