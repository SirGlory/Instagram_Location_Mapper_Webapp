from flask.views import MethodView
from flask import Flask, render_template, request
from flask_mobility import Mobility
from flask_mobility.decorators import mobilized
from flask_styleguide import Styleguide
from wtforms import Form, StringField, SubmitField
from mapgen import GenMap
from data_check import DataCheck

# Create app instance
app = Flask(__name__)
styleguide = Styleguide(app)
Mobility(app)

# Pages

class HomePage(MethodView):

    def get(self):
        handle_form = HandleForm()
        return render_template('home.html', handleform=handle_form)
    @mobilized(get)
    def get(self):
        handle_form = HandleForm()
        return render_template('home_mob.html', handleform=handle_form)


class MapPage(MethodView):
    # post input from home page
    def post(self):
        # draw inputs, get handle, scrape location addresses,

        handle_form = HandleForm(request.form)
        handle = str(handle_form.handle.data)
        DataCheck(handle).db_check()
        my_map = GenMap(handle=handle)
        my_map.gen_map()
        map_name=f"map_{handle}.html"
        return render_template(map_name)


class AboutPage(MethodView):

    def get(self):
        return render_template('about.html')

    @mobilized(get)
    def get(self):
        return render_template('about_mob.html')

# Form
class HandleForm(Form):
    handle = StringField("Enter handle: @", default="travel")
    button = SubmitField("Generate Map")
    button_about = SubmitField("Learn More")


# Routing
app.add_url_rule('/', view_func=HomePage.as_view('home_page'))
app.add_url_rule('/map_page', view_func=MapPage.as_view('map_page'))
app.add_url_rule('/about_page', view_func=AboutPage.as_view('about_page'))

# Run
if __name__ == '__main__':
    app.run(debug=True)
