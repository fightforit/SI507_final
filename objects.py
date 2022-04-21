

from util import *
import yelp_api
import google_api
from datetime import datetime
import time


class Place:
    def __init__(self) -> None:
        """
        Initialize a Place object

            1. Restaurants infomation is stored as a tree using dictionary: {location: {food_type: [restaurant_info]}}
            2. Yelp: name, address, phone, lat, lng, rating, price, review
            3. Google: opening_hours, rating, price, reviews
        """
        # Some locations: "New York City, NY", "Miami, FL", "Los Angeles, CA", "Chicago, IL", "Houston, TX"
        self.locations = ["Ann Arbor, MI"]
        self.restaurants = {"Ann Arbor, MI": {"chinese": None, "italian": None, "american": None, "mexican": None, "japanese": None,
                                              "korean": None, "thai": None, "vietnamese": None, "french": None, "indian": None, "greek": None}}

    def set_restaurants(self) -> None:
        """
        Set the restaurants for each location and food type
        """
        # For each location, read cache json file and set the restaurants, if not exist, query yelp and google api
        for location in self.restaurants:
            filename = "-".join(location.replace(", ",
                                " ").split(" ")) + ".json"

            # check if the location exists
            try:  # if cache file exists, read it
                restaurant_info = read_json(f"cache/{filename}")
                self.restaurants[location] = restaurant_info
            except:  # if cache file does not exist, query yelp and google api
                for food_type in self.restaurants[location]:
                    self.update_restaurants_from_yelp(location, food_type)
                    self.update_restaurants_from_google(location, food_type)
                write_json(f"cache/{filename}", self.restaurants[location])

    def update_restaurants_from_yelp(self, location, food_type) -> None:
        """
        Update the restaurants for each location and food type

        Args:
            location: location of the restaurant
            food_type: food type of the restaurant

        Returns:
            None
        """
        # Call yelp api to query info and parse the response
        yelp_resp = yelp_api.query_api(food_type, location)
        self.restaurants[location][food_type] = yelp_api.parse_query(yelp_resp)

    def update_restaurants_from_google(self, location, food_type) -> None:
        """
        Update the restaurants for each location and food type

        Args:
            location: location of the restaurant
            food_type: food type of the restaurant

        Returns:
            None
        """
        for restaurant in self.restaurants[location][food_type]:
            # Find the restaurant using text search
            google_resp = google_api.find_text(
                restaurant["lat"], restaurant["lng"], restaurant["name"]+" "+restaurant["address"])

            if not google_resp["results"]:
                continue

            restaurant_id = google_resp["results"][0]["place_id"]
            restaurant_info = google_api.find_details(restaurant_id)

            # update the restaurant info
            restaurant["rating"]["Google"] = restaurant_info["result"]["rating"]
            try:
                restaurant["price"]["Google"] = restaurant_info["result"]["price_level"]
            except:
                restaurant["price"]["Google"] = None

            try:
                restaurant["opening_hours"] = restaurant_info["result"]["opening_hours"]["weekday_text"]
            except:
                restaurant["opening_hours"] = None

            for review in restaurant_info["result"]["reviews"]:
                parse_review = {
                    "time": datetime.fromtimestamp(review["time"]).strftime('%Y-%m-%d %H:%M:%S'),
                    "text": review["text"],
                    "rating": review["rating"]
                }
                restaurant["reviews"]["Google"].append(parse_review)
            # time delay to avoid google api limit
            time.sleep(1)

    def add_new_location(self, location) -> None:
        """
        Add a new location to the dictionary

        Args:
            location: location of the restaurant

        Returns:
            None
        """
        if location not in self.restaurants:
            self.restaurants[location] = {"chinese": None}
            # , "italian": None, "american": None, "mexican": None, "japanese": None,
            #                               "korean": None, "thai": None, "vietnamese": None, "french": None, "indian": None, "greek": None}
        # set up the restaurant info for the new location
        self.set_restaurants()

    def add_new_food_type(self, location, food_type) -> None:
        """
        Add a new food type to the dictionary

        Args:
            location: location of the restaurant
            food_type: food type of the restaurant

        Returns:
            None
        """
        # filename for a location in order to update with new food type
        filename = "-".join(location.replace(", ", " ").split(" ")) + ".json"

        print(filename)
        # check if the location exists
        self.add_new_location(location)

        # check if the food type exists
        if (not food_type in self.restaurants[location]) or (self.restaurants[location][food_type] is None):
            self.restaurants[location][food_type] = None
            self.update_restaurants_from_yelp(location, food_type)
            self.update_restaurants_from_google(location, food_type)
            print(f"update {filename}")
            write_json(f"cache/{filename}", self.restaurants[location])


def main():
    clear_cache()
    place = Place()
    place.set_restaurants()
    print("add new location")
    place.add_new_location("New York City, NY")
    print("add new food type")
    place.add_new_food_type("Ann Arbor, MI", "cuban")


if __name__ == "__main__":
    main()
