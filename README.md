# SI507_final
Final project, Restaurant Searching Engine!

- Install packages:
    - Please refer to the packages list below (requirements.txt)
    - Run the following command
        ```
        python3 -m pip install -r requirements.txt
        ```

- API key
    - Please create a ```secret.py``` file containing three variables
        - ```YELP_Client_ID = <your yelp client ID>```
        - ```YELP_API_KEY = <your yelp api key>```
        - ```GOOGLE_API_KEY = <your google api key>```
- Interaction
    - Please run the following command to launch the program
        ```
        python3 helloflask.py
        ```
    - Then open the webpage ``` 127.0.0.1:5000```
    - A home page with title ```SI 507 Final Project, Winter 2022``` will be opened. It contains three bullets in the contents and the footnote with creater’s name and email link. The three bullets in the webpage are described in the following
        - ```About```: a brief description of this project
        - ```Search```: a search page for user to enter the restaurant type (e.g. japanese, korean, and etc) in a city that an user wants to search. After entering that, the page will show the corresponding restaurants’ information on it. The data is either from the caches or newly requested from Yelp or Google API. If requested from API, it requires some time to processed.
        - ```Stats```: a statistic page for showing the average rating of each restaurant type in a city. Enter the city you want to see, then a average rating from Yelp and Google will be shown in both a table and a plot format.
        - ``Nearby search``: a page for searching the restaurants nearby a place.
