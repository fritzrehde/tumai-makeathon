from pyrosm import OSM
import pandas as pd

# osm = OSM("bremen.osm.pbf")
print('loading data')
# osm = OSM("bremen-buildings-only.osm.pbf")
osm = OSM("bremen.osm.pbf")

print('get buildings')
buildings = osm.get_buildings()
df = pd.DataFrame(buildings)

drop_list = ['addr:country', 'addr:full', 'addr:housename', 'email',
       'name', 'opening_hours', 'operator', 'phone', 'ref', 'url', 'website', 'internet_access', 'wikipedia']

df = df.drop(drop_list, axis=1)
print(df.columns)
print(df.loc[100, :].values.tolist())
print(df.head(100).to_csv("test.csv"))
