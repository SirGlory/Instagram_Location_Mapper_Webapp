from flask.views import MethodView
from flask import Flask, render_template, request
from flask_styleguide import Styleguide
from folium import Map, Marker, Popup
from folium.plugins import MarkerCluster
from wtforms import Form, StringField, SubmitField
from geo import Geopoint
from geopy.geocoders import Nominatim
from scrape import Scrape

# Create app instance
app = Flask(__name__)
styleguide = Styleguide(app)

class HomePage(MethodView):

    def get(self):
        handle_form = HandleForm()
        return render_template('home.html', handleform=handle_form)

#Pages
class MapPage(MethodView):
    # posts input from home page
    def post(self):
        # draw inputs, get hanflem scrape location addresses,
        # create map and marker custer instances
        handle_form = HandleForm(request.form)
        handle = str(handle_form.handle.data)
        locations = Scrape(handle).get_locations()
        my_map = Map(location=[-22.5, 24], zoom_start=4)
        mc = MarkerCluster()
        
       # For each location convert address to coordinates, create poup and marker,
       # add to marker cluster
        for i in range(0, len(locations), 1):
            # Convert address to coordinates
            locator = Nominatim(user_agent="myGeocoder")
            try:
                locationi = locator.geocode(locations[i])
                lat = locationi.latitude
                lon = locationi.longitude
                p = Popup(locations[i],max_width=400)
                mk = Marker([lat, lon],p)
                mc.add_child(mk)
            except:
                pass
            
        # Add marker cluster
        my_map.add_child(mc)
        # Save the Map Instance Into a HTML file
        my_map.save("templates/map_locations.html")
        print("------------------------------------------")
        print("Map Created! Check your files for map_locations.html")
        return render_template('map_locations.html')


class AboutPage(MethodView):

    def get(self):
        return render_template('about.html')

# Form
class HandleForm(Form):
    handle = StringField("Enter handle: @", default="4x4theboiz")
    button = SubmitField("Generate Map")
    button_about = SubmitField("Learn More")

# Routing
app.add_url_rule('/',
                 view_func=HomePage.as_view('home_page'))
app.add_url_rule('/map_page',
                 view_func=MapPage.as_view('map_page'))
app.add_url_rule('/about_page',
                 view_func=AboutPage.as_view('about_page'))

# Run
if __name__ == '__main__':
    app.run()
