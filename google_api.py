import requests
import json

# import the secret keys
from secret import *

# request api

###########################################################################################
# get place request


def find_place(place="Ann Arbor"):
    print(f"Finding {place} requests")
    base_url = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json"
    params = {
        "input": place,
        "inputtype": "textquery",
        "fields": "name,place_id,formatted_address,geometry",
        "key": GOOGLE_API_KEY,
    }
    response = requests.get(base_url, params=params)
    return response.json()


# parse place
def parse_place(place_json):
    places_info = place_json["candidates"]
    infos = []
    for place in places_info:
        info = {}
        info["name"] = place["name"]
        info["place_id"] = place["place_id"]
        info["formatted_address"] = place["formatted_address"]
        info["lat"] = place["geometry"]["location"]["lat"]
        info["lng"] = place["geometry"]["location"]["lng"]
        infos.append(info)
    return infos


###########################################################################################
# get nearby restaurant search request
def find_nearby(lat, lng, radius=1000):
    print(f"Finding nearby requests")
    base_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    params = {
        "location": f"{lat},{lng}",
        "radius": radius,
        "type": "restaurant",
        "key": GOOGLE_API_KEY,
    }
    response = requests.get(base_url, params=params)
    return response.json()


# parse nearby restaurant search
def parse_nearby(nearby_json, food_style="Null", food_type="Null"):
    nearby_info = nearby_json["results"]
    infos = []
    for place in nearby_info:
        info = {}
        info["name"] = place["name"]
        info["place_id"] = place["place_id"]
        try:
            info["opening_hours"] = place["opening_hours"]["open_now"]
        except:
            info["opening_hours"] = "Null"

        try:
            info["html"] = place['photos'][0]["html_attributions"][0]
        except:
            info["html"] = "Null"
        info["lat"] = place["geometry"]["location"]["lat"]
        info["lng"] = place["geometry"]["location"]["lng"]
        info["rating"] = place["rating"]
        info["user_ratings_total"] = place["user_ratings_total"]
        info["types"] = place["types"]
        info["food_style"] = food_style
        info["food_type"] = food_type
        # try to catch the address from vicinity if it exists, otherwise use formatted_address
        try:
            info["formatted_address"] = place["vicinity"]
        except:
            info["formatted_address"] = place["formatted_address"]
        # try to catch the price level if it exists, otherwise use 0
        try:
            info["price_level"] = place["price_level"]
        except:
            info["price_level"] = "Null"

        infos.append(info)
    return infos


###########################################################################################
# text search request
def find_text(lat, lng, query, radius=1000):
    print(f"Finding text requests")
    base_url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    params = {
        "location": f"{lat},{lng}",
        "radius": radius,
        "query": query,
        "key": GOOGLE_API_KEY,
    }
    response = requests.get(base_url, params=params)
    return response.json()


# parse text search
def parse_text(text_json, query=None, food_style="Null", food_type="Null"):
    if query:
        return parse_nearby(text_json, query, query)
    else:
        return parse_nearby(text_json, food_style, food_type)


###########################################################################################
# place details request
def find_details(place_id):
    print(f"Finding details requests")
    base_url = "https://maps.googleapis.com/maps/api/place/details/json"
    params = {
        "place_id": place_id,
        "fields": "name,rating,user_ratings_total,formatted_address,geometry,price_level,types,opening_hours,review,url",
        "key": GOOGLE_API_KEY,
    }
    response = requests.get(base_url, params=params)
    return response.json()


# parse place details
def parse_details(details_json, place_id):
    details_info = details_json["result"]
    info = {}
    info["name"] = details_info["name"]
    info["place_id"] = place_id
    info["rating"] = details_info["rating"]
    info["user_ratings_total"] = details_info["user_ratings_total"]
    info["formatted_address"] = details_info["formatted_address"]
    info["lat"] = details_info["geometry"]["location"]["lat"]
    info["lng"] = details_info["geometry"]["location"]["lng"]
    info["types"] = details_info["types"]
    try:
        info["price_level"] = details_info["price_level"]
    except:
        info["price_level"] = "Null"
    info["opening_hours"] = details_info["opening_hours"]
    info["reviews"] = details_info["reviews"]
    info["url"] = details_info["url"]
    return info
