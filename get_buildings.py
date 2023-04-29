from pyrosm import OSM
import pandas as pd
from get_power import get_power


def get_roofshape(dict):
    if isinstance(dict, str):
        return ""
    elif 'roof:shape' in dict.keys():
        return dict['roof:shape']
    else:
        return ""


def get_roofarea(x):
    # Placeholder Function that takes geometry and turns it to roof area:
    return 0


def get_df():
    # import .pbf buildings as df
    print('loading data')
    # osm = OSM("data/buildings/bremen.osm.pbf")
    osm = OSM('data/buildings/germany.osm.pbf')

    print('get buildings')
    buildings = osm.get_buildings()
    df = pd.DataFrame(buildings)

    # Drop certain columns and rows without streetnumber
    drop_list = ['addr:country', 'addr:full', 'addr:housename', 'email',
                 'name', 'opening_hours', 'operator', 'phone', 'ref', 'url', 'website', 'internet_access', 'wikipedia']

    df = df.drop(drop_list, axis=1)
    df = df[df['addr:housenumber'].str.strip().astype(bool)]

    # Add column with roof area and shape
    df['roof_shape'] = df.apply(lambda row: get_roofshape('tags'), axis=1)
    df['roof_area'] = df.apply(lambda row: get_roofarea('geometry'), axis=1)

    # Export
    print(df.columns)
    # print(df.loc[100, :].values.tolist())
    # print(df.head(100).to_csv("test.csv"))
    print(df.to_csv("test_all_germany.csv"))

    return df


if __name__ == '__main__':
    get_df()
