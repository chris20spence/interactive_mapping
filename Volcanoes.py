import folium 
import pandas

data = pandas.read_csv("Volcanoes.txt")
lat = list(data["LAT"])
lon = list(data["LON"])
elev = list(data["ELEV"])

html = """<h4>Volcano information:</h4>
Height: %s m
"""

def colour_producer(elevation):
    if elevation < 1000:
        return "green"
    elif 100<= elevation < 3000:
        return "orange"
    else:
        return "red"

map2 = folium.Map(location=[40.758701, -111.876183], 
                  zoom_start=5, 
                  tiles="CartoDB positron",
                  min_zoom = 2,
                  max_zoom = 18)  

fgv = folium.FeatureGroup(name="Volcanoes")

for lt, ln, el in zip(lat, lon, elev):
    fgv.add_child(folium.CircleMarker(location=[lt, ln], popup=(folium.Popup(str(int(el))+"m in elevation", max_width=450, width=450, height=250)), parse_html=True, radius = 9, color= "gray", fill_color=colour_producer(el), fill_opacity=0.8))

map2.add_child(fgv)
map2.add_child(folium.LayerControl())

map2.save("Map2_Volcanoes_by_elevation.html")

