from lands import draw
from shapely.geometry import Polygon, LineString, Point, mapping
import fiona
import shapefile

__author__ = 'Stefan Feltmann'


def create_vector(x, y, temp_world):

    pass

def find_land_borders(world):

    def is_ocean(pos):
        x, y = pos
        return world.ocean[x][y]

    def is_not_ocean(pos):
        return not is_ocean(pos)

    y = 0
    x = 0

    borders = []
    known_points = []

    while y < world.height:
        while x < world.width:
            if is_not_ocean((x, y)) and (x, y) not in known_points:
                nx, ny = x, y
                border = []
                stack = []
                border.append((x, y))
                stack.append((x, y))
                known_points.append((x, y))
                while len(stack) > 0:
                    co_ords = world.tiles_around_factor(1, (nx, ny), radius=1, predicate=is_not_ocean)
                    for i in co_ords:
                        if i not in known_points:
                            border.append(i)
                            stack.append(i)
                            known_points.append(i)
                    nx, ny = stack.pop()
                borders.append(border)
                x, y = 0, 0
            else:
                x += 1
        y += 1
        x = 0
    return borders

def test_find(borders, world):
    world_name = world.name
    output_dir = "."
    ocean = [[True for x in xrange(world.width)] for y in xrange(world.height)]
    for landmass in borders:
        for i in landmass:
            x, y = i
            ocean[x][y] = False
    # Generate images
    filename = '%s/%s_ocean.png' % (output_dir, world_name)
    draw.draw_ocean(ocean, filename)
    filename = '%s/%s_ocean.png' % (output_dir, (world_name + "2"))
    draw.draw_ocean(world.ocean, filename)
    print("* ocean image generated in '%s'" % filename)


def make_polygons(borders):
    poly_borders = []
    lines = []
    points = []
    for landmass in borders:
        # print len(landmass)
        if len(landmass) > 3:
            new_polygon = Polygon(landmass)
            poly_borders.append(new_polygon)
        elif len(landmass) > 1:
            new_line = LineString(landmass)
            lines.append(new_line)
        else:
            new_point = Point(landmass)
            points.append(new_point)
    return poly_borders, points, lines


def create_gis_database(world, map_filename):
    borders = find_land_borders(world)
    poly_borders, points, lines = make_polygons(borders)

    poly_border_schema = {
        'geometry': 'Polygon',
        'properties': {'id': 'int'},
    }

    line_border_schema = {
        'geometry': 'Line',
        'properties': {'id': 'int'},
    }

    point_border_schema = {
        'geometry': 'Point',
        'properties': {'id': 'int'},
    }

    if len(poly_borders) > 0:
        with fiona.open(map_filename + "_poly_border.shp", 'w', 'ESRI Shapefile', poly_border_schema) as c:
            for i in xrange(len(poly_borders)):
                poly = poly_borders[i]
                ## If there are multiple geometries, put the "for" loop here
                c.write({
                    'geometry': mapping(poly),
                    'properties': {'id': i},
                })
            c.close()

    if len(lines) > 0:
        with fiona.open(map_filename + "_line_border.shp", 'w', 'ESRI Shapefile', line_border_schema) as c:
            for i in xrange(len(lines)):
                line = lines[i]
                ## If there are multiple geometries, put the "for" loop here
                c.write({
                    'geometry': mapping(line),
                    'properties': {'id': i},
                })
            c.close()

    if len(points) > 0:
        with fiona.open(map_filename + "_point_border.shp", 'w', 'ESRI Shapefile', point_border_schema) as c:
            for i in xrange(len(points)):
                point = points[i]
                ## If there are multiple geometries, put the "for" loop here
                c.write({
                    'geometry': mapping(point),
                    'properties': {'id': i},
                })
            c.close()

    print len(poly_borders)
    print len(points)
    print len(lines)
    # test_find(borders, world)