from lands import draw

__author__ = 'Stefan Feltmann'


def create_vector(x, y, temp_world):

    pass

def find_land_borders(world):
    _ocean   = [[False for x in xrange(world.width)] for y in xrange(world.height)]
    # _borders = [[False for x in xrange(world.width)] for y in xrange(world.height)]
    for y in xrange(world.height):
        for x in xrange(world.width):
            if world.ocean[y][x]:
                _ocean[y][x] = True

    def my_is_ocean(pos):
        x, y = pos
        return world.ocean[x][y]

    def is_not_ocean(pos):
        return not my_is_ocean(pos)

    y = 0
    x = 0

    borders = []
    known_points = []

    while y < world.height:
        print "Y at " + str(y)
        while x < world.width:
            if is_not_ocean((x, y)) and (x, y) not in known_points:
                print "X at " + str(x)
                print "Land Mass #" + str(len(borders) + 1)
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
                # for i in border:
                #     nx, ny = i
                #     _ocean[nx][ny] = True
                #     temp_world.ocean[nx][ny] = True
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


def create_gis_database(world):
    borders = find_land_borders(world)
    print len(borders)
    print borders
    test_find(borders, world)