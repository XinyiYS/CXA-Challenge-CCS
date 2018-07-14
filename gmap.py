import googlemaps
from datetime import datetime
import config


import matplotlib
matplotlib.use('TkAgg')
from matplotlib import pyplot as plt
from io import StringIO
from io import BytesIO
from PIL import Image
import urllib

def show_map_pic():
    url = "http://maps.googleapis.com/maps/api/staticmap?center=12.955232,77.579923&size=600x600&zoom=17&sensor=false"
    buffer = BytesIO(urllib.request.urlopen(url).read())
    image = Image.open(buffer)
    plt.imshow(image)
    plt.show()


def get_gmap_direction():

    gmaps = googlemaps.Client(key=config.google_config['API_key'])

    # Geocoding an address
    geocode_result = gmaps.geocode('1600 Amphitheatre Parkway, Mountain View, CA')

    # Look up an address with reverse geocoding
    reverse_geocode_result = gmaps.reverse_geocode((40.714224, -73.961452))

    # Request directions via public transit
    now = datetime.now()
    directions_result = gmaps.directions("Sydney Town Hall",
                                         "Parramatta, NSW",
                                         mode="transit",
                                         departure_time=now)
    return directions_result


import gmaps
from ipywidgets.embed import embed_minimal_html

def get_traffic_html():
    gmaps.configure(api_key=config.google_config['API_key'])

    # Map centered on London
    fig = gmaps.figure(center=(51.5, -0.2), zoom_level=11)
    # fig.add_layer(gmaps.bicycling_layer())
    fig.add_layer(gmaps.traffic_layer())
    print(help(fig))
    # embed_minimal_html('export.html', views=[fig])
    return None



from gmplot import gmplot
# # Place map
gmap = gmplot.GoogleMapPlotter(37.766956, -122.438481, 13)

# Polygon
golden_gate_park_lats, golden_gate_park_lons = zip(*[
    (37.771269, -122.511015),
    (37.773495, -122.464830),
    (37.774797, -122.454538),
    (37.771988, -122.454018),
    (37.773646, -122.440979),
    (37.772742, -122.440797),
    (37.771096, -122.453889),
    (37.768669, -122.453518),
    (37.766227, -122.460213),
    (37.764028, -122.510347),
    (37.771269, -122.511015)
    ])
gmap.plot(golden_gate_park_lats, golden_gate_park_lons, 'cornflowerblue', edge_width=10)

# Scatter points
top_attraction_lats, top_attraction_lons = zip(*[
    (37.769901, -122.498331),
    (37.768645, -122.475328),
    (37.771478, -122.468677),
    (37.769867, -122.466102),
    (37.767187, -122.467496),
    (37.770104, -122.470436)
    ])
gmap.scatter(top_attraction_lats, top_attraction_lons, '#3B0B39', size=40, marker=False)

# Marker
hidden_gem_lat, hidden_gem_lon = 37.770776, -122.461689
gmap.marker(hidden_gem_lat, hidden_gem_lon, 'cornflowerblue')

# Draw
gmap.draw("my_map.html")

import gmplot as gmplot

gmap = gmplot.GoogleMapPlotter.from_geocode("San Francisco")
gmap.draw("san.html")
