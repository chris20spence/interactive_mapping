import folium 
import pandas
import base64
from folium import IFrame
import cv2
from find_crds import df

#print(find_crds.get_crds("Paris"))

html = """<h4>Holiday information:</h4>
Height: %s m
"""
#Defining map base & parameters 
map1 = folium.Map(location=[51.295022, -0.752492], 
                  zoom_start=3, 
                  tiles="CartoDB positron",
                  min_zoom = 2,
                  max_zoom = 18)  


fgp = folium.FeatureGroup(name="Holiday")

#reading population data from file, defining colours for data groups, applying hover tooltip to display data
fgp.add_child(folium.GeoJson(data=open("world.json", "r", 
                             encoding="utf-8-sig").read(), 
                             style_function= lambda x: {"fillColor":"green" if x["properties"]["POP2005"] < 10000000
                                                                            else "orange" if 10000000 <= x["properties"]["POP2005"] <20000000 
                                                                            else "red"},
                             tooltip = folium.GeoJsonTooltip(fields=('NAME', 'POP2005',),aliases=('Country','Population')), show = True))


#function for finding size of image to ensure hoversize is appropriate, adds scalar to avoid scroll bar 
def image_size(picname):
    im = cv2.imread(picname)
    borderadd = tuple([1.1*x for x in im.shape])
    return(borderadd)
    
#Add image hover for all the places in Holiday_data.csv

for index, row in df.iterrows(): 
    img_path = "images/"+str(df.loc[index, "Image Name"])+ ".jpg"
    lon_value = df.loc[index, "lon"]
    lat_value = df.loc[index, "lat"]
    encoded = base64.b64encode(open(img_path, 'rb').read())
    html = '<img src="data:image/png;base64,{}">'.format
    iframe = IFrame(html(encoded.decode('UTF-8')), width=image_size(img_path)[1], height=image_size(img_path)[0])
    popup = folium.Popup(iframe) #max_width=1060, parse_html=True)
    folium.Marker(location=[lat_value, lon_value], tooltip=html, popup = popup, 
    icon=folium.Icon(color = 'red')).add_to(map1)

#adding the feattures to the map base
map1.add_child(fgp)
map1.add_child(folium.LayerControl())

map1.save("Map1_Holiday_Map.html")
print("Map complete")
