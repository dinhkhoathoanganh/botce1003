from googlemaps import Client as GoogleMaps
from oauth2client.service_account import ServiceAccountCredentials
import requests
import json
import re

# API Call destinations and key
google_key = 'AIzaSyBkAho_-0yi5so--8rCdfISpDa-Npu5_pk'
search_url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
details_url = "https://maps.googleapis.com/maps/api/place/details/json"
direction_url = "https://maps.googleapis.com/maps/api/directions/json" 

def place_id_results(query):
	# Get place ID
	search_payload = {"key":google_key, "query":query}
	search_req = requests.get(search_url, params=search_payload)
	search_json = search_req.json()

	# Default is to get the first result -- so when we can standardize the canteen locations name for the users
	place_id = search_json["results"][0]["place_id"]

	return place_id

def direction(origin, destination):
	# Get direction
	search_payload = {"origin": "place_id:" + origin, "destination": "place_id:" + destination, "key": google_key}
	search_req = requests.get(direction_url, params=search_payload)
	search_json = search_req.json()
	# Call direction instructions extract function
	direction_instructions(search_json)

def direction_instructions(search_json):
	# Extract and print the direction instructions
	for i in range (0, len (search_json['routes'][0]['legs'][0]['steps'])):
		j = search_json['routes'][0]['legs'][0]['steps'][i]['html_instructions']
		clean_j =  re.sub('<[^>]+>', '', j)
		print (clean_j)

def main():

	# Get origins and destinations
	origin = input('enter origin: ')
	origin_id = place_id_results(origin)
	destination = input('enter destination: ')
	destination_id = place_id_results(destination)
	
	# Find direction
	instructions = direction(origin_id, destination_id)
	print("Done!")

main()