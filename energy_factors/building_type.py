
# DO NOT use, do not know where to get data if commercial or not
def get_buildingtype(dict_):
    if isinstance(dict_, dict):
        type = dict_.get('roof:shape')
        return type
    else:
        return None