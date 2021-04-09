from flask.views import MethodView
from flask import Flask, render_template, request
from flask_styleguide import Styleguide
from folium import Map, PolyLine
from wtforms import Form, StringField, SubmitField
from coords import Coords
from scrape import Scrape

# Create app instance
app = Flask(__name__)
styleguide = Styleguide(app)

#Pages
class HomePage(MethodView):

    def get(self):
        handle_form = HandleForm()
        return render_template('home.html', handleform=handle_form)


class MapPage(MethodView):
    # post input from home page
    def post(self):
        # draw inputs, get handle, scrape location addresses,
        # create map and marker cluster instances, generate coordinates
        handle_form = HandleForm(request.form)
        handle = str(handle_form.handle.data)
        locations = Scrape(handle).get_locations()
        my_map = Map(location=[-22.5, 24], zoom_start=4)
        coordinates = Coords(locations)

        # Add Polyline
        polyline = PolyLine(coordinates.get_coords()[1], color="red", weight=2, opacity=0.7)
        polyline.add_to(my_map)        
        # Add Marker Cluster
        my_map.add_child(coordinates.get_coords()[0])
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
