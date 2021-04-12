# Imports
import requests
from bs4 import BeautifulSoup


class Scrape:

    def __init__(self, handle):
        self.handle = handle

    def get_locations(self):

        # Create Variables
        base_url = "https://www.picuki.com/profile/" + self.handle
        r = requests.get(base_url,
                         headers={
                             'User-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0'})
        c = r.content
        soup = BeautifulSoup(c, "html.parser")
        all_locs = soup.find_all("div", {"class": "photo-location"})
        all_links = soup.find_all("div", {"class": "photo"})
        locs = []
        links = []

        # Add unique locations to list
        for i in range(0, len(all_locs), 1):
            xx = all_locs[i].text.replace("\n", "")
            yy = all_links[i].find('a').get('href')
            if xx not in locs:
                locs.append(xx)
                links.append(yy)
            else:
                pass

        reversed_locs = locs[::-1]  # Revered location order. scraping puts newest first,
        reversed_links = links[::-1] # but to plot journey we would want oldest post as starting point
        return reversed_locs, reversed_links


if __name__ == "__main__":
    handle = str(input("Please enter handle of user: ") or '4x4theboiz')
    print(handle)
    point1 = Scrape(handle=handle)
    address = point1.get_locations()
    print(address[0])
    print(address[1])
