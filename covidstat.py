import folium
import requests
from bs4 import BeautifulSoup
import pandas



r = requests.get('https://www.worldometers.info/coronavirus/#countries')

c = r.content

soup = BeautifulSoup(c,'html.parser')
data = soup.find('tbody')

rows = data.find_all('tr',{'style':''})

d = {}


for item in rows:
    tcases = item.find_all('td')[2].text
    d[item.find_all('td')[1].text] = int(tcases.replace(',',''))



def color_gen(tcases):
    if tcases < 1000:
        return 'blue'
    elif tcases < 5000:
        return 'green'
    elif tcases < 2500:
        return 'red'
    elif tcases > 50000:
        return 'yellow'
    elif tcases < 100000:
        return 'red'
    elif tcases < 150000:
        return 'orange'
    else:
        return 'red'
cdata = pandas.read_csv('countrydata.csv')

lat = list(cdata['latitude'])
print(lat)
lon = list(cdata['longitude'])

country = list(cdata['country'])


map = folium.Map(location = [41.69,91.09],zoom_level = 4,tiles='Stamen Terrain')

fg = folium.FeatureGroup(name = 'Countries')

for lt,ln,ct in zip(lat,lon,country):

    if ct in d.keys():
        fg.add_child(folium.CircleMarker(location = [lt,ln], popup=str(ct) + '\n' + str(d[ct]) + '  ' +'შემთხვევა',radius=10,fill_color = color_gen(d[ct]),color = 'gray',
                                         fill_opacity = 0.5))


map.add_child(fg)


map.save('CoronaMap.html')