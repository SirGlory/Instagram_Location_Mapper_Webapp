from folium.plugins import MarkerCluster
from geopy.geocoders import Nominatim
from folium import Marker, Popup


class Coords:

    def __init__(self, locations):
        self.locations = locations

    def get_coords(self):
        mc = MarkerCluster()
        coords = []

        # For each location convert address to coordinates, create poup and marker,
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
        return mc, coords
