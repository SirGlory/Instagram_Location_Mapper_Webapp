import sqlite3
from folium import Map, PolyLine, Marker, Popup
from folium.plugins import MarkerCluster

class GenMap:

    def __init__(self, handle):
        self.handle = handle


    def gen_map(self):
        # read database
        connection = sqlite3.connect("posts.db")
        cursor = connection.cursor()
        sql = f"""SELECT * FROM "{self.handle}" """
        cursor.execute(sql)
        result = cursor.fetchall()
        connection.close()

        # Generate map, cluster class and create empty coordinates list
        if self.handle == "4x4theboiz":
            my_map = Map(location=[-25.25, 21.75], zoom_start=5)
        else:
            my_map = Map(location=[0, 0], zoom_start=3)
        mc = MarkerCluster()
        coords = []


        # For each location convert address to coordinates, create popup and marker,
        # add to marker cluster
        for i in range(0, len(result), 1):

            popup_content = f"{result[i][0]} <br> " \
                            f"<a href={result[i][1]} > See Post"
            p = Popup(popup_content, max_width=400)
            mk = Marker([result[i][2], result[i][3]], p)
            mc.add_child(mk)
            lat_lon = (result[i][2], result[i][3])
            coords.append(lat_lon)

        # Add Polyline with coords
        if self.handle == "4x4theboiz":
            polyline = PolyLine(coords, color="red", weight=2, opacity=0.7)
            polyline.add_to(my_map)
        else:
            pass
        # Add Marker Cluster with mc
        my_map.add_child(mc)
        # Save the Map Instance Into a HTML file
        map_name = f"templates/map_{self.handle}.html"
        my_map.save(map_name)


if __name__ == "__main__":
    handle = "4x4theboiz"
    c = GenMap(handle)
    c.gen_map()
