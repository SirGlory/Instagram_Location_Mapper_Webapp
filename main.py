from flask.views import MethodView
from flask import Flask, render_template, request
from flask_styleguide import Styleguide
from folium import Map, Marker, Popup
from wtforms import Form, StringField, SubmitField
from geo import Geopoint
from geopy.geocoders import Nominatim
from scrape import Scrape
import os

# Create app instance
app = Flask(__name__)
styleguide = Styleguide(app)

class HomePage(MethodView):


    def get(self):
        handle_form = HandleForm()
        return render_template('home.html', handleform=handle_form)


class MapPage(MethodView):

    def post(self):
        handle_form = HandleForm(request.form)
        handle = str(handle_form.handle.data)
        locations = Scrape(handle).get_locations()
        my_map = Map(location=[-20, 20], zoom_start=5)
        map_name = f"templates\map_{handle}.html"
        map_name_return = f"map_{handle}.html"

        # Delete any old occurrences with same name
        if os.path.exists(map_name):
            print(f"{map_name}, file deleted!")
            os.remove(map_name)
        else:
            print(f"{map_name} does not exist")
            
        for i in range(0, len(locations), 1):
            # Convert address to coordinates
            locator = Nominatim(user_agent="myGeocoder")
            try:
                locationi = locator.geocode(locations[i])
                lat = locationi.latitude
                lon = locationi.longitude
                # Geopoint Instance
                geopoint = Geopoint(latitude=lat, longitude=lon)
                popup = Popup(locations[i], max_width=400)
                popup.add_to(geopoint)
                geopoint.add_to(my_map)
                print(locationi.address)
            except:
                pass

        # Save the Map Instance Into a HTML file
        my_map.save(map_name)
        print(map_name_return)
        print("------------------------------------------")
        print(f"Map Created! Check your files for {map_name}")
        return render_template(map_name_return, handle=handle, handleform=handle_form)


class AboutPage(MethodView):

    def get(self):
        return render_template('about.html')


class HandleForm(Form):
    handle = StringField("Enter handle: @", default="4x4theboiz")
    button = SubmitField("Generate Map")
    button_about = SubmitField("Learn More")


app.add_url_rule('/',
                 view_func=HomePage.as_view('home_page'))
app.add_url_rule('/map_page',
                 view_func=MapPage.as_view('map_page'))
app.add_url_rule('/about_page',
                 view_func=AboutPage.as_view('about_page'))

if __name__ == '__main__':
    app.run()


