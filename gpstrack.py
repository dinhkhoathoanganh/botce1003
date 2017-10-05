from googlemaps import Client as GoogleMaps
import requests
import json
import re

import math

# API Call destinations and key
from credentialshhanh import *
from xl import *

#Template dictionary for canteen locations info

class google_maps:
	#Read file from excel to convert to dictionary in python
	def excel_to_list(file, ws_name):
		ws = xl.load_ws(xl.load_wb(file), ws_name)
		place_list = {}
		print(len(ws["A"]))
		for i in range(2,len(ws["A"])+1):
			print("#", i)
			canteen = xl.cell(ws, "A" + str(i))
			lat_lng = {"lat": float(xl.cor_content_col(ws, 1, i, "lat")),"lng": float(xl.cor_content_col(ws, 1, i, "lng"))}
			place_value = [xl.cor_content(ws,"A", "B", canteen), xl.cor_content(ws,"A", "C", canteen), lat_lng]
			place_list[xl.cell(ws, "A" + str(i))] = place_value
		# print(place_list) #checkpoint
		return place_list


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
		data = google_maps.fetch_data(search_payload, search_url)	

		place_id = data["results"][0]["place_id"]
		lat_lng = data["results"][0]["geometry"]["location"]
		# Default is to get the first result -- so when we can standardize the canteen locations name for the users	

		return (place_id, lat_lng)	

	#Find direction with googlemaps (default by driving - it is quite close to walking direction in NTU context, and this is more useful than walking search mode even when the user's location is very far away from the canteens)
	def direction(origin, destination):
		# Get direction
		search_payload = {"origin": "place_id:" + origin, "destination": "place_id:" + destination, "key": google_key}
		data = google_maps.fetch_data(search_payload, direction_url)	

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
	def sort_nearby_place(origin_lat_lng, file, ws_name):
		place_list = google_maps.excel_to_list(file, ws_name)

		distance_list = []
		for place in place_list.items():
			place_name = place[0]
			destination_lat_lng = place[1][2]		

			straight_distance = google_maps.haversine_distance(origin_lat_lng, destination_lat_lng)
			distance_list.append(straight_distance)	

		sorted_place_list = [j for i,j in sorted(zip(distance_list, place_list))]
		return sorted_place_list


def main(): #YOU CAN RUN THIS AND SEE...

	# #Program to sort the canteen list
	origin = input('enter your current location - origin: ')
	origin_id, origin_lat_lng = google_maps.place_id_results(origin)
	
	sorted_place_list = google_maps.sort_nearby_place(origin_lat_lng, "Canteen Restaurant List.xlsx", "placeid")

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