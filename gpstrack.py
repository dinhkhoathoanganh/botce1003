from googlemaps import Client as GoogleMaps
import requests
import json
import re

import math

# API Call destinations and key
from credentialshhanh import *

#Template dictionary for canteen locations info
place_list = {"can B" : ["ChIJ-c0P3AoP2jERmgAasZYsPdM", "76 Nanyang Drive, N2.1, #02-03, Nanyang Technological University, Singapore, 637331",	{"lat": 1.346986, "lng":	103.680168}], "can 2": ["ChIJ_4T7q6EP2jEROVd_kctPf3Y",	"35 Students Walk, #01-01 NTU Canteen 2, Singapore 639548",	{"lat": 1.348431, "lng":	103.685482}]}

class google_maps:

	#Call API from googlemaps
	def fetch_data(search_payload, url):
	    search_req = requests.get(url, params=search_payload)
	    
	    print("#######", search_req) #checkpoint
	    data = search_req.json()
	    print(data) #checkpoint	

	    if data["status"] == "OK":      
	        return data	

	    elif data["status"] == "OVER_QUERY_LIMIT":
	        print("Exceed rate limit! Contact your admin")
	        exit()
	    
	    else:
	        print("Error!")
	        exit()	

	#Extract place ID, latitude and longtitude of the given location with googlemaps
	def place_id_results(query):
		# Get place ID
		search_payload = {"key":google_key, "query":query}
		search_req = requests.get(search_url, params=search_payload)
		data = fetch_data(search_payload, search_url)	

		place_id = data["results"][0]["place_id"]
		lat_lng = data["results"][0]["geometry"]["location"]
		# Default is to get the first result -- so when we can standardize the canteen locations name for the users	

		return (place_id, lat_lng)	

	#Find direction with googlemaps (default by driving - it is quite close to walking direction in NTU context, and this is more useful than walking search mode even when the user's location is very far away from the canteens)
	def direction(origin, destination):
		# Get direction
		search_payload = {"origin": "place_id:" + origin, "destination": "place_id:" + destination, "key": google_key}
		data = fetch_data(search_payload, direction_url)	

		# Call direction instructions extract function	

		return data	

	#Refine the direction instructions
	def direction_instructions(data):
		# Extract and print the direction instructions
		instructions = []
		for i in range (0, len (data['routes'][0]['legs'][0]['steps'])):
			j = data['routes'][0]['legs'][0]['steps'][i]['html_instructions']
			clean_j =  re.sub('<[^>]+>', '', j)
			instructions.append(clean_j)
		return instructions	
	
	#Calculate ROUTE distance with googlemaps
	def calculate_distance(data):
		#calculate distance between 2 places
		distance = data['routes'][0]['legs'][0]['distance']['text']
		return distance	

	#Calculate STRAIGHT LINE distance with formula calculation, this is to save the number of API calls to googlemaps (due to limited number of API calls)
	def haversine_distance(point1, point2):
	    """
	    # original formula from  http://www.movable-type.co.uk/scripts/latlong.html 
	    Haversine formula: 
	        a = sin²(Δφ/2) + cos φ1 ⋅ cos φ2 ⋅ sin²(Δλ/2)
	                        _   ____
	        c = 2 ⋅ atan2( √a, √(1−a) )
	        d = R ⋅ c	

	    where φ is latitude, λ is longitude, R is earth’s radius (mean radius = 6,371km);
	            note that angles need to be in radians to pass to trig functions!	

	    :p1:     (tup) lat,lon
	    :p2:     (tup) lat,lon
	    """
	    lat1, lng1 = list(point1.values())[0], list(point1.values())[1]
	    lat2, lng2 = list(point2.values())[0], list(point2.values())[1]	

	    R = 6371.0 # km - earths's radius	

	    # convert decimal degrees to radians 
	    lat1, lng1, lat2, lng2 = map(math.radians, [lat1, lng1, lat2, lng2])	

	    # haversine formula 
	    dlng = lng2 - lng1
	    dlat = lat2 - lat1	

	    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlng/2)**2
	    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
	    d = R * c
	    return d	

	#Sort the canteens in the order of increasing distance based on the user's location
	def sort_nearby_place(origin_lat_lng, place_list):
		distance_list = []
		for place in place_list.items():
			place_name = place[0]
			destination_lat_lng = place[1][2]		

			straight_distance = haversine_distance(origin_lat_lng, destination_lat_lng)
			distance_list.append(straight_distance)	

		sorted_place_list = [j for i,j in sorted(zip(distance_list, place_list))]
		return sorted_place_list


def main(): #YOU CAN RUN THIS AND SEE...

	# #Program to sort the canteen list
	origin = input('enter your current location - origin: ')
	origin_id, origin_lat_lng = place_id_results(origin)

	print(place_list)
	
	sorted_place_list = sort_nearby_place(origin_lat_lng, place_list)

	print("list of canteen from nearest to furthest: ", sorted_place_list)
	
	#################
	# #Program to Find direction
	# origin = input('enter your current location - origin: ')
	# origin_id, origin_lat_lng = place_id_results(origin)

	# destination = input('enter destination: ')
	# destination_id, destination_lat_lng = place_id_results(destination)


	# data = direction(origin_id, destination_id)
	# instructions = direction_instructions(data)
	# distance = calculate_distance(data)

	# print("Here are the instructions: ", instructions)
	# print("Estimated distance: ", distance)
if __name__ == "__main__":
    main()