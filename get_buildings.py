from pyrosm import OSM
import pandas as pd


def get_roofshape(dict):
    if 'roof:shape' in dict.keys():
        return dict['roof:shape']
    else:
        return ("")


def get_df():
    # osm = OSM("bremen.osm.pbf")
    print('loading data')
    osm = OSM("bremen.osm.pbf")
    # osm = OSM('data/buildings/bremen-buildings-only.osm.pbf')

    print('get buildings')
    buildings = osm.get_buildings()
    df = pd.DataFrame(buildings)
    df['roof_shape'] = df.apply(lambda row: get_roofshape('tags'), axis=1)

    drop_list = ['addr:country', 'addr:full', 'addr:housename', 'email',
                 'name', 'opening_hours', 'operator', 'phone', 'ref', 'url', 'website', 'internet_access', 'wikipedia']

    df = df.drop(drop_list, axis=1)
    print(df.columns)
    print(df.loc[100, :].values.tolist())
    print(df.head(100).to_csv("test.csv"))

    # x = get_roofshape({"roof:shape":"flat","type":"supermarket"})
    # print(x)


if __name__ == '__main__':
    get_df()
