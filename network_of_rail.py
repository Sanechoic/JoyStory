import networkx as nx
import matplotlib.pyplot as plt
import random
import csv
import mpld3
import numpy as np
import cartopy.crs as ccrs
import os
from convertbng.util import convert_bng, convert_lonlat

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

    G=nx.Graph()
    size = []
    node_colours = []
    # add nodes
    for station in stations:
        position = convert_lonlat([int(station['easting'])], [int(station['northing'])])

        G.add_node(station['name'],
                   pos=(position[0][0],position[1][0])
                 )

        in_out = float(station['entries_exits'].replace(',', ''))

        node_colours.append(in_out)

        rel_size = in_out/100000
        size.append(rel_size)



    '''
    # add edges
    for link in links:
        G.add_edge(link['from'],link['to'],
                   colour=line_to_hex[link['common_line']])
    '''

    pos=nx.get_node_attributes(G,'pos')

    #fig, ax = plt.subplots(subplot_kw=dict(facecolor='#EEEEEE'))


    # Map
    crs = ccrs.PlateCarree()

    fig, ax = plt.subplots(subplot_kw=dict(projection=crs))

    ax.coastlines()
    #ax.set_extent([-128, -62, 20, 50])



    scatter = nx.draw_networkx_nodes(G,pos, node_size=size, font_size=16,
                 alpha=.5,
                 width=.075, ax=ax, node_color=node_colours, cmap=plt.cm.autumn)

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
