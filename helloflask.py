from flask import Flask, request, render_template
import json
from util import *
import objects as objs
app = Flask(__name__)

place = objs.Place()
place.set_restaurants()


@app.route("/")
def index():
    return render_template("home_page.html", course="SI 507", semester="Winter 2022")


@app.route("/search", methods=["GET", "POST"])
def search():

    try:
        city = request.form["city"]
        state = request.form["state"]
        food_type = request.form["food_type"].lower()
        search_string = ", ".join([city, state])
    except:
        city = ""
        state = ""
        food_type = ""
        search_string = ""

    try:
        if search_string == "":
            raise Exception

        place.add_new_location(search_string)
        place.add_new_food_type(search_string, food_type)

        print(place.restaurants.keys())
        print(search_string)
        print(food_type)
        print(place.restaurants[search_string].keys())

        content = place.restaurants[search_string][food_type]

    except:
        content = ""

    return render_template(
        "search.html",
        city=city,
        state=state,
        food_type=food_type,
        search_str=search_string,
        restaurants=content,
    )


@app.route("/stats", methods=["GET", "POST"])
def stats():
    try:
        city = request.form["city"]
        state = request.form["state"]
        search_string = ", ".join([city, state])
    except:
        city = ""
        state = ""
        search_string = ""

    try:
        place.add_new_location(search_string)

        stats_food_type = [["Food Type", "Yelp Rating", "Google Rating"]]
        for food_type in place.restaurants[search_string]:
            yelp_rating = 0
            google_rating = 0
            for restaurant in place.restaurants[search_string][food_type]:
                yelp_rating += restaurant["rating"]["Yelp"]
                google_rating += restaurant["rating"]["Google"]
            stats_food_type.append(
                [food_type,
                    round(yelp_rating /
                          len(place.restaurants[search_string][food_type]), 2),
                    round(google_rating / len(place.restaurants[search_string][food_type]), 2)])
    except:
        content = ""

    return render_template(
        "stats.html",
        city=" ".join(city),
        state=state,
        stats_food=stats_food_type,
    )


@app.route("/about")
def about():
    return render_template("about.html", course="SI 507", semester="Winter 2022")


if __name__ == "__main__":
    print(f"Starting Flask app {app.name}")
    app.run(debug=True)
