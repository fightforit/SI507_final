import objects as objs
import yelp_api
import google_api
import util as ut
import secrets


def main():
    # set up the place object
    place = objs.Place()
    place.set_restaurants()

    # add new location
    print("add new location")
    place.add_new_location("New York City, NY")

    # add new food type
    print("add new food type")
    place.add_new_food_type("Ann Arbor, MI", "cuban")

    # add new food type
    print("add new location")
    place.add_new_location("Chicago, IL")


if __name__ == '__main__':
    main()
