from flask.views import MethodView
from flask import Flask, render_template, request
from flask_styleguide import Styleguide
from wtforms import Form, StringField, SubmitField
from mapgen import GenMap
from scrape import Scrape

# Create app instance
app = Flask(__name__)
styleguide = Styleguide(app)


# Pages
class HomePage(MethodView):

    def get(self):
        handle_form = HandleForm()
        return render_template('home.html', handleform=handle_form)


class MapPage(MethodView):
    # post input from home page
    def post(self):
        # draw inputs, get handle, scrape location addresses,
        # create map and marker cluster instances
        handle_form = HandleForm(request.form)
        handle = str(handle_form.handle.data)
        locations = Scrape(handle)

        my_map = GenMap(locations=locations.get_locations())
        my_map.gen_map()
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
app.add_url_rule('/', view_func=HomePage.as_view('home_page'))
app.add_url_rule('/map_page', view_func=MapPage.as_view('map_page'))
app.add_url_rule('/about_page', view_func=AboutPage.as_view('about_page'))

# Run
if __name__ == '__main__':
    app.run()
