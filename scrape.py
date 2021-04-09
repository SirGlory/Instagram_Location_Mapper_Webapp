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
        all = soup.find_all("span", {"class": "icon-globe-alt"})
        l = []

        # Add unique locations to list
        for i in range(0,len(all),1):
            xx = all[i].text

            if xx not in l:
                l.append(xx)
            else:
                pass
            
        reversed_l = l[::-1]
        print(l)
        print(base_url)
        return reversed_l # Revered location order. scraping puts newest frist,
        #return l         # but to plot journey we would want oldest post as starting point
        


if __name__ == "__main__":
    handle = str(input("Please enter handle of user: ") or '4x4theboiz')
    print(handle)
    point1 = Scrape(handle=handle)
    address = point1.get_locations()
    print(address)
