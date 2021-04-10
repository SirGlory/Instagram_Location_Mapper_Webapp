from folium import Map, PolyLine, Marker, Popup
from folium.plugins import MarkerCluster
from geopy.geocoders import Nominatim


class GenMap:

    def __init__(self, locations):
        self.locations = locations
        print(locations)

    def gen_map(self):
        # Generate map, cluster class and create empty coordinates list
        my_map = Map(location=[-22.5, 24], zoom_start=4)
        mc = MarkerCluster()
        coords = []

        # For each location convert address to coordinates, create popup and marker,
        # add to marker cluster
        for i in range(0, len(self.locations), 1):
            # Convert address to coordinates
            locator = Nominatim(user_agent="myGeocoder")
            try:
                locationi = locator.geocode(self.locations[i])
                lat = locationi.latitude
                lon = locationi.longitude
                lat_lon = (lat, lon)
                p = Popup(self.locations[i], max_width=400)
                mk = Marker([lat, lon], p)
                mc.add_child(mk)
                coords.append(lat_lon)
            except:
                pass

        # Add Polyline with coords
        polyline = PolyLine(coords, color="red", weight=2, opacity=0.7)
        polyline.add_to(my_map)
        # Add Marker Cluster with mc
        my_map.add_child(mc)
        # Save the Map Instance Into a HTML file
        my_map.save("templates/map_locations.html")
        print("------------------------------------------")
        print("Map Created! Check your files for templates/map_locations.html")


if __name__ == "__main__":
    c = GenMap(['Midrand, Gauteng'])
    c.gen_map()