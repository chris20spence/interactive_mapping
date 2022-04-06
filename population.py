import folium 
import pandas

html = """<h4>Volcano information:</h4>
Height: %s m
"""
#Defining map base & parameters 
map3 = folium.Map(location=[51.295022, -0.752492], 
                  zoom_start=3, 
                  tiles="CartoDB positron",
                  min_zoom = 2,
                  max_zoom = 18)  


fgp = folium.FeatureGroup(name="Population")

#reading population data from file, defining colours for data groups, applying hover tooltip to display data
fgp.add_child(folium.GeoJson(data=open("world.json", "r", 
                             encoding="utf-8-sig").read(), 
                             style_function= lambda x: {"fillColor":"green" if x["properties"]["POP2005"] < 10000000
                                                                            else "orange" if 10000000 <= x["properties"]["POP2005"] <20000000 
                                                                            else "red"},
                             tooltip = folium.GeoJsonTooltip(fields=('NAME', 'POP2005',),aliases=('Country','Population')), show = True))

#adding the feattures to the map base
map3.add_child(fgp)
map3.add_child(folium.LayerControl())

map3.save("Map3_Population_by_country.html")

