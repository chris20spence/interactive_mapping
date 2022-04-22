import folium 
import pandas
import base64
from folium import IFrame
import cv2
from find_crds import df


html = """<h4>Holiday information:</h4>
Height: %s m
"""

#Defining map base & parameters 
map1 = folium.Map(location=[51.295022, -0.752492], 
                  zoom_start=3, 
                  tiles="CartoDB positron",
                  min_zoom = 2,
                  max_zoom = 18)  


#function for finding size of image to ensure popupsize is appropriate, adds scalar to avoid scroll bar 
def image_size(picname):
    im = cv2.imread(picname)
    borderadd = tuple([1.1*x for x in im.shape])
    return(borderadd)
    

#iterate through the Holiday_data.csv file, creating popups on each city crds, adding image for popup when clicked, adding the hover with text info
for index, row in df.iterrows(): 

    img_path = "images/"+str(df.loc[index, "Image Name"])+ ".jpg"

    lon_value = df.loc[index, "lon"]
    lat_value = df.loc[index, "lat"]

    #desc_html is the content for the hover message, City+Year, Accompanied by: & Fun fact: are on separate lines
    desc_html = f'<div style="white-space: normal">' + str(df.loc[index, "City"]) + " - " + str(df.loc[index, "Year"]) + '<br>' + "Accompanied by: " + str(df.loc[index, "Accompanied by:"]) + '<br>' + "Fun fact: " + str(df.loc[index, "Fun Fact:"]) + '</div>'
    hover_msg = folium.Tooltip(text=folium.Html(desc_html, script=True, width=300).render())

    encoded = base64.b64encode(open(img_path, 'rb').read())
    html = '<img src="data:image/png;base64,{}">'.format
    iframe_pic = IFrame(html(encoded.decode('UTF-8')), width=image_size(img_path)[1], height=image_size(img_path)[0])
    popup = folium.Popup(iframe_pic) #max_width=1060, parse_html=True)
    
    folium.Marker(location=[lat_value, lon_value], tooltip=hover_msg, popup=popup, icon=folium.Icon(color = 'red')).add_to(map1)

map1.save("Map1_Holiday_Map.html")
print("Map complete")
