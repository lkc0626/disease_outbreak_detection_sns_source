import os
import json
import pickle
import heapq
import random
import datetime
import json
import math
from math import radians, cos, sin, asin, sqrt
from os.path import join
from utils import normalize_str as nstr
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from math import *

def euclidean(lat1, long1, lat2, long2):
    return sqrt(pow(lat1 - lat2, 2) + pow(long1 - long2, 2))

def haversine(lat1, long1, lat2, long2):

    # Convert latitude and longitude to 
    # spherical coordinates in radians.
    degrees_to_radians = math.pi/180.0
         
    # phi = 90 - latitude
    phi1 = (90.0 - lat1)*degrees_to_radians
    phi2 = (90.0 - lat2)*degrees_to_radians
         
    # theta = longitude
    theta1 = long1*degrees_to_radians
    theta2 = long2*degrees_to_radians
         
    # Compute spherical distance from spherical coordinates.
         
    # For two locations in spherical coordinates 
    # (1, theta, phi) and (1, theta, phi)
    # cosine( arc length ) = 
    #    sin phi sin phi' cos(theta-theta') + cos phi cos phi'
    # distance = rho * arc length
     
    cos = (math.sin(phi1)*math.sin(phi2)*math.cos(theta1 - theta2) + 
           math.cos(phi1)*math.cos(phi2))
    arc = math.acos( cos )
 
    # Remember to multiply arc by the radius of the earth 
    # in your favorite set of units to get length.
    r = 6373

    return arc*6373

def getnetwork(place, K):
    network = {}

    edge = []
    for k1, x1 in place.items():
        for k2, x2 in place.items():
            if k1 == k2:
                continue
            #d = haversine(x1[0], x1[1], x2[0], x2[1])
            d = euclidean(x1[0], x1[1], x2[0], x2[1])
            temp = {}
            temp['edge'] = k1 + '___' + k2
            temp['distance'] = d
            edge.append(temp)

    edges = heapq.nsmallest(K*len(place), edge, key = lambda s: s['distance'])

    for i in range(len(edges)):
        network[edges[i]['edge']] = edges[i]['distance']

    return network

folder = '/raid/home/nvcfchen/data'
ci_co_st_2_latlong = pickle.load(open(os.path.join(folder, 'ci_co_st_2_latlong.pkl')))

cos = ['argentina', 'ecuador', 'colombia', 'chile', 'mexico']
for co1 in cos[:]:
    print co1
    i = 0
    id_2_ci_latlong = dict()
    ci_2_id = dict()
    place = dict()
    for (ci, co, st), (lat, long) in ci_co_st_2_latlong.items():
        ci = nstr(ci)
        co = nstr(co)
        st = nstr(st)
        if co == co1:
            id_2_ci_latlong[i] = [ci + '_' + co + '_' + st, (lat, long)]
            ci_2_id[ci + '_' + co + '_' + st] = i
            place[ci + '_' + co + '_' + st] = [lat, long]
            i += 1
    for k in [15, 10, 5, 20, 25]:
        print k
        graph = getnetwork(place, k)
        #print co1, i
        #print graph.keys()
        #print graph.items()[1]
        #print len(place), len(graph.keys())
        g = open('data/{0}/{1}_k_{2}_graph.txt'.format(co1, co1, k), 'w')
        for edge, dist in graph.items():
            [n1, n2] = edge.split('___')
            g.write('{0} {1} {2}'.format(ci_2_id[n1], ci_2_id[n2], dist)+'\n')
        #    print edge, n1, n2, ci_2_id[n1], ci_2_id[n2]
        g.close()
    #f = open('data/{0}/id_2_ci_latlong.txt'.format(co1), 'w')
    #f.write(json.dumps(id_2_ci_latlong))
    #f.close()
    #f = open('data/{0}/ci_2_id.txt'.format(co1), 'w')
    #f.write(json.dumps(ci_2_id))





