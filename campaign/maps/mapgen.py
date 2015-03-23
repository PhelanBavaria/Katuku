

import yaml


process_order = ['fill_all']



def empty_map(width, height):
    print(width, height)
    _map = {}
    for y in range(height):
        for x in range(width):
            _map[(x, y)] = None
    return _map

def load(mapname):
    content = yaml.load(open('content/maps/' + mapname + '.yml').read())
    _map = empty_map(*content['size'])
    for key in process_order:
        try:
            _map = functions[key](_map, content[key])
        except KeyError:
            continue
    return _map

def fill_all(_map, tile_type):
    for key, value in _map.items():
        if value == None:
            _map[key] = tile_type
    return _map


functions = {
    'fill_all': fill_all
}
