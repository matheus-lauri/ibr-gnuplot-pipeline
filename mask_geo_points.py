import json
from shapely.geometry import shape, Point
from shapely.ops import unary_union
from shapely.prepared import prep

def load_land_polygon(path):
    with open(path, encoding='utf-8') as f:
        geojson = json.load(f)
    land_shapes = [
        shape(feature['geometry'])
        for feature in geojson['features']
        if feature['properties'].get('CONTINENT') != 'Antarctica'
    ]
    return prep(unary_union(land_shapes))

def filter_land_points(input_path, output_path, land):
    with open(input_path, encoding='utf-8') as f_in, open(output_path, 'w', encoding='utf-8') as f_out:
        for line in f_in:
            stripped = line.strip()
            if not stripped or stripped.startswith('#'):
                f_out.write(line)
                continue
            lon_str, lat_str = stripped.split()[:2]
            if land.contains(Point(float(lon_str), float(lat_str))):
                f_out.write(line)

if __name__ == '__main__':
    land = load_land_polygon('ne_50m_admin_0_countries.geojson')
    filter_land_points('source_geo_heatmap.dat', 'source_geo_heatmap_land.dat', land)
    print("Arquivo 'source_geo_heatmap_land.dat' gerado com sucesso.")
