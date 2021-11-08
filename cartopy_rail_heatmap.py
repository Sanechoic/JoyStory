import matplotlib.pyplot as plt
import random
import csv
import numpy as np
import os
from convertbng.util import convert_bng, convert_lonlat
from cartopy import config
import cartopy.crs as ccrs
from netCDF4 import Dataset as netcdf_dataset

owner_to_hex = {'Arriva Trains Wales':'#138b85',
                'C2C':'#b8228e',
                'Chiltern Railways':'#28a0d4',
                'East Midlands Trains':'#132e50',
                'Glasgow Prestwick Airport Ltd':'#3fb4e4',
                'Govia Thameslink Railway':'#d6509a',
                'Great Western Railway':'#0c483c',
                }

line_to_hex = {}

def main(csv_path):
    with open(csv_path, newline='') as csvfile:
        filereader = list(csv.reader(csvfile, delimiter=','))
        headers = [header.replace('\ufeff', '') for header in filereader[0]]
        stations = [dict(zip(headers,row)) for row in filereader[1:]]


    lons = []
    lats = []
    in_out = []



    for station in stations:
        lon,lat = convert_lonlat([int(station['easting'])], [int(station['northing'])])
        lons.append(lon[0])
        lats.append(lat[0])
        in_out.append(float(station['entries_exits'].replace(',', '')))


    # Map
    # Get some parameters for the Stereographic Projection
    lons = np.array(lons)
    lats = np.array(lats)
    sst = np.array([in_out for i in range(len(in_out))])


    ax = plt.axes(projection=ccrs.PlateCarree())

    plt.contourf(lons, lats, sst, 60,
             transform=ccrs.PlateCarree())

    ax.coastlines()

    plt.show()

    '''
    # Interactive Map
    labels = G.nodes()
    tooltip = mpld3.plugins.PointLabelTooltip(scatter, labels=labels)
    mpld3.plugins.connect(fig, tooltip)
    mpld3.show()
    '''



if __name__ == '__main__':
    main('station_data.csv')
