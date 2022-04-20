from flask import Flask, request, render_template
import json

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("home_page.html", course="SI 507", semester="Winter 2022")


@app.route("/search", methods=["GET", "POST"])
def search():
    # create a search bar and a submit button
    # when the user clicks the submit button,
    # get the input from the search bar
    # and print the search term to the console
    # and return the search term to the user
    try:
        city = request.form["city"].split()
        state = request.form["state"]
        food_type = request.form["food_type"].lower()
        search_string = "-".join(city + [state])
    except:
        city = ""
        state = ""
        food_type = ""
        search_string = ""

    try:
        with open(f"cache/{search_string}.json", "r") as f:
            data = json.load(f)
            content = data[food_type]
    except:
        content = ""

    return render_template(
        "search.html",
        city=" ".join(city),
        state=state,
        food_type=food_type,
        search_str=search_string,
        restaurants=content,
    )


@app.route("/about")
def about():
    return render_template("about.html", course="SI 507", semester="Winter 2022")


if __name__ == "__main__":
    print(f"Starting Flask app {app.name}")
    app.run(debug=True)
