from flask.views import MethodView
from flask import Flask, render_template, request
from flask_styleguide import Styleguide
from folium import Map, Marker, Popup
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


class MapPage(MethodView):

    def post(self):
        handle_form = HandleForm(request.form)
        handle = str(handle_form.handle.data)
        locations = Scrape(handle).get_locations()
        mymap = Map(location=[-20, 20], zoom_start=5)

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
                geopoint.add_to(mymap)
                print(locationi.address)
            except:
                pass

        # Save the Map Instance Into a HTML file
        mymap.save("templates/map_locations.html")
        print("------------------------------------------")
        print("Map Created! Check your files for map_locations.html")
        return render_template('map_locations.html')


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
