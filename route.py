#!/usr/local/bin/python3
# route.py : Find routes through maps
#
# Code by: bkmaturi-josatiru-tsadey
#
# Based on skeleton code by V. Mathur and D. Crandall, January 2021
#


# !/usr/bin/env python3
from queue import PriorityQueue
import sys

#loading the source and destination cities from the input text file
def source_destination_file(file):
    road={}
    with open(file, 'r') as f:
        for line in f.readlines():
            segments = line.split()
            city1 = segments[0]
            city2 = segments[1]
            if city1 not in road:
                road[city1] = {}
            if city2 not in road:
                road[city2] = {}
            road[city1][city2] = (float(segments[2]), float(segments[3]), segments[4])
            road[city2][city1] = (float(segments[2]), float(segments[3]), segments[4])
    return road

#loading the co-ordinates of cities
def read_gps_from_input_file(filename):
    locations = {}
    with open(filename, 'r') as f:
        for line in f.readlines():
            gps_data = line.split()
            city = gps_data[0]
            x = float(gps_data[1])
            y = float(gps_data[2])
            locations[city] = (x,y)
    return locations

road,gps={},{}
road=source_destination_file('road-segments.txt')
gps=read_gps_from_input_file('city-gps.txt')


#depeding on the chosen cost function returning the cost value
def priority_cost_function(h,last_city,current_state):
    (route,miles,segments,time_taken,accidents)=current_state
    cur_city=route[-1]
    if h=="distance":
        distance=distance_between_cities(cur_city,last_city)
        return miles+distance
    if h=="time":
        distance=distance_between_cities(cur_city,last_city)
        speed=65
        time=distance/speed
        return time_taken+time
    if h=="safe":
        probability_of_accident=1/(10**6)
        distance=probability_of_accident*distance_between_cities(cur_city,last_city)
        return accidents+distance
    if h=="segments":
        return segments+1

#we are considering eucledian distance as heuristic which provides us the displacement from one city to other
def distance_between_cities(city1,city2):
    if city1 not in gps.keys():
        return 0
    if city2 not in gps.keys():
        return 0
    x1,y1=gps[city1]
    x2,y2=gps[city2]
    return (((x2-x1)**2)+((y2-y1)**2))**0.5

#this function returns the length of route which is finally considered, total number of miles one travels, estimated time, expected number of accidents and route map.
def get_route(initial_city,destination,h):
    route=[initial_city]
    miles=0
    segments=0
    accidents=0
    time=0
    g=0
    visited={}
    index_of_visited={}
    priority_index=priority_cost_function(h,destination,(route,miles,segments,accidents,time))
    #defining fringe as a priority queue
    fringe = PriorityQueue()
    #pushing initial state in the fringe
    fringe.put((priority_index, (route,miles,segments,accidents,time)))
    while not fringe.empty():
        #popping out of fringe
        fringevalues = fringe.get()
        priority_index = fringevalues[0]
        route = fringevalues[1][0]
        miles = fringevalues[1][1]
        segments = fringevalues[1][2]
        time = fringevalues[1][3]
        accidents = fringevalues[1][4]
        source=route[-1]
        g+=1
        #loop terminating condition if source has become destination
        if source==destination:
            temp1=[]
            temp2=[]
            for i in range(len(route)-1):
                keys=[]
                for key in road.keys():
                    keys.append(key)
                for j in range(len(keys)):
                    if keys[j]==route[i]:
                        temp1.append((road[keys[j]][route[i + 1]]))
            for i in range(1,len(route)):
                temp2.append(route[i])
            route_taken=[]
            for i in range(len(temp1)):
                a=[]
                a.append(temp2[i])
                a.append(temp1[i][2] + " for " + str(int(temp1[i][0])) + " miles")
                route_taken.append(tuple(a))
            return {"total-segments": len(route_taken),
                    "total-miles": miles,
                    "total-hours": time,
                    "total-expected-accidents": accidents,
                    "route-taken": route_taken}
        visited[source] = 1
        index_of_visited[source]=priority_index
        intermediate_city=road[source].keys()
        #modifying different parameters depending on the successor cities
        for city in intermediate_city:
            miles1, speed_limit1, highway_name1=road[source][city]
            time1=miles1/speed_limit1
            prob=1/(10**6)
            if "I-" in highway_name1 :
                accidents1 = 2*prob*miles1
            else:
                accidents1 = 1*prob*miles1
            priority_index=priority_cost_function(h,destination,(route + [city],miles + miles1, segments + 1,time + time1, accidents + accidents1))
            is_city_visited=visited.get(city,0)
            if is_city_visited==1 and priority_index < index_of_visited[city] and h != "segments":
                visited[city] = 0
                fringe.put((priority_index+g,(route + [city],miles + miles1, segments + 1,time + time1, accidents + accidents1)))
            if is_city_visited==0:
                fringe.put((priority_index+g,(route + [city],miles + miles1, segments + 1,time + time1, accidents + accidents1)))

if __name__ == "__main__":
    if len(sys.argv) != 4:
        raise(Exception("Error: expected 3 arguments"))
    (_, start_city, end_city, cost_function) = sys.argv
    if cost_function not in ("segments", "distance", "time", "safe"):
        raise(Exception("Error: invalid cost function"))
    #start_city = 'Bloomington,_Indiana'
    #end_city = 'Indianapolis,_Indiana'
    #cost_function = "time"
    result = get_route(start_city, end_city, cost_function)
    #Pretty print the route
    print("Start in %s" % start_city)
    for step in result["route-taken"]:
        print("Then go to %s via %s" % step)
    print("\n Total segments: %6d" % result["total-segments"])
    print("    Total miles: %10.3f" % result["total-miles"])
    print("    Total hours: %10.3f" % result["total-hours"])
    print("Total accidents: %15.8f" % result["total-expected-accidents"])

