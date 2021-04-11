from folium import Marker  # For Inheritance


class Geopoint(Marker):  # For Inheritance - added (Marker)

    def __init__(self, latitude, longitude):
        super().__init__(location=[latitude, longitude])  # For Inheritance
        self.latitude = latitude
        self.longitude = longitude

    def closest_parallel(self):
        return round(self.latitude)


if __name__ == "__main__":
    tokyo = Geopoint(latitude = 35.7 , longitude = 139.7)
    print(tokyo.closest_parallel())