
import argparse
import json
import pprint
import requests
import sys
import urllib
from secrets import *
import time

try:
    # For Python 3.0 and later
    from urllib.error import HTTPError
    from urllib.parse import quote
    from urllib.parse import urlencode
except ImportError:
    # Fall back to Python 2's urllib2 and urllib
    from urllib2 import HTTPError
    from urllib import quote
    from urllib import urlencode

# Base url
API_HOST = 'https://api.yelp.com'
SEARCH_PATH = '/v3/businesses/search'
BUSINESS_PATH = '/v3/businesses/'  # Business ID will come after slash.

# Defaults for our simple example.
DEFAULT_TERM = 'dinner'
DEFAULT_LOCATION = 'Naples, FL'
SEARCH_LIMIT = 10


def request(host, path, api_key, url_params=None):
    """Given your API_KEY, send a GET request to the API.
    Args:
        host (str): The domain host of the API.
        path (str): The path of the API after the domain.
        API_KEY (str): Your API Key.
        url_params (dict): An optional set of query parameters in the request.
    Returns:
        dict: The JSON response from the request.
    Raises:
        HTTPError: An error occurs from the HTTP request.
    """
    url_params = url_params or {}
    url = '{0}{1}'.format(host, quote(path.encode('utf8')))
    headers = {
        'Authorization': 'Bearer %s' % api_key,
    }

    print(u'Querying {0} ...'.format(url))

    response = requests.request('GET', url, headers=headers, params=url_params)

    return response.json()


def search(api_key, term, location):
    """Query the Search API by a search term and location.
    Args:
        term (str): The search term passed to the API.
        location (str): The search location passed to the API.
    Returns:
        dict: The JSON response from the request.
    """

    url_params = {
        'term': term.replace(' ', '+'),
        'location': location.replace(' ', '+'),
        'limit': SEARCH_LIMIT
    }
    return request(API_HOST, SEARCH_PATH, api_key, url_params=url_params)


def get_business(api_key, business_id):
    """Query the Business API by a business ID.
    Args:
        business_id (str): The ID of the business to query.
    Returns:
        dict: The JSON response from the request.
    """
    business_path = BUSINESS_PATH + business_id

    return request(API_HOST, business_path, api_key)


def get_reviews(api_key, business_id):
    """Query the Business API by a business ID.
    Args:
        business_id (str): The ID of the business to query.
    Returns:
        dict: The JSON response from the request.
    """
    business_path = BUSINESS_PATH + business_id + "/reviews"

    return request(API_HOST, business_path, api_key)


def query_api(term, location):
    """Queries the API by the input values from the user.
    Args:
        term (str): The search term to query.
        location (str): The location of the business to query.
    """
    response = search(YELP_API_KEY, term, location)

    businesses = response.get('businesses')

    if not businesses:
        print(u'No businesses for {0} in {1} found.'.format(term, location))
        return

    return businesses


def parse_reviews(reviews):
    review_list = []
    if reviews:
        for review in reviews["reviews"]:
            parse_review = {
                "time": review["time_created"],
                "text": review["text"],
                "rating": review["rating"]
            }
            review_list.append(parse_review)
    else:
        print("No reviews found")
    return review_list


def parse_query(info_json):
    """Parses the JSON response from the API.
    Args:
        info_json (dict): The JSON response from the request.
        parse_info (str): Parsed information

    Returns:
        None
    """
    # restaunts infomations:
    # from yelp -> name, address, phone, lat, lng
    # from google -> opening hours
    # from both -> rating, price, reviews

    parse_result = []
    if isinstance(info_json, list):  # multiple results found
        for result in info_json:
            parse_info = {
                "name": result["name"],
                "address": ", ".join(result["location"]["display_address"]),
                "phone": result["display_phone"],
                "lat": result["coordinates"]["latitude"],
                "lng": result["coordinates"]["longitude"],
                "rating": {"Yelp": result["rating"], "Google": None},
                "reviews": {"Yelp": parse_reviews(get_reviews(YELP_API_KEY, result["id"])),
                            "Google": []}
            }
            try:
                parse_info["price"] = {"Yelp": result["price"], "Google": None}
            except:
                parse_info["price"] = {"Yelp": None, "Google": None}
            parse_result.append(parse_info)
            time.sleep(1)  # sleep for 1 second to avoid query limit
    elif isinstance(info_json, dict):  # single result found
        parse_info = {
            "name": info_json["name"],
            "address": ", ".join(info_json["location"]["display_address"]),
            "phone": info_json["display_phone"],
            "lat": info_json["coordinates"]["latitude"],
            "lng": info_json["coordinates"]["longitude"],
            "rating": {"Yelp": info_json["rating"], "Google": None},
            "reviews": {"Yelp": parse_reviews(get_reviews(YELP_API_KEY, info_json["id"])),
                        "Google": []}
        }
        try:
            parse_info["price"] = {"Yelp": info_json["price"], "Google": None}
        except:
            parse_info["price"] = {"Yelp": None, "Google": None}
        parse_result.append(parse_info)

    return parse_result


def main():
    query_api("pizza", DEFAULT_LOCATION)


if __name__ == '__main__':
    main()
