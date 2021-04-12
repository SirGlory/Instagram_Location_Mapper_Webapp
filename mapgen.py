from folium import Map, PolyLine, Marker, Popup
from folium.plugins import MarkerCluster
from geopy.geocoders import Nominatim


class GenMap:

    def __init__(self, locations, links):
        self.links = links
        self.locations = locations


    def gen_map(self):
        # Generate map, cluster class and create empty coordinates list
        my_map = Map(location=[-25, 21.5], zoom_start=5)
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
                
                popup_content = f"{self.locations[i]} <br> " \
                                f"<a href={self.links[i]} > See Post"
                p = Popup(popup_content, max_width=400)
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


if __name__ == "__main__":
    c = GenMap(['Midrand, Gauteng'], 'https://www.picuki.com/media/2548099983087509980')
    c.gen_map()
