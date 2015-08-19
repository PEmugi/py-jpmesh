# coding: utf-8

import math

# const 
HEIGHT1 = 40.0 / 60.0
WIDTH1 =  1.0
HEIGHT2 = HEIGHT1 / 8.0
WIDTH2 = WIDTH1 / 8.0
HEIGHT3 = HEIGHT2 / 10.0
WIDTH3 = WIDTH2 / 10.0

class JPMesh:

    def __init__(self, code):
        self.code = code
        self.min_lon, self.min_lat = meshcode2lonlat(self.code)
        if len(code) == 4:
            self.level = 1
        elif len(code) == 6:
            self.level = 2
        elif len(code) == 8:
            self.level = 3
        else:
            self.level = len(code) - 8 + 3

    def get_code(self, level=None):
        if level == 1:
            return self.code[:4]
        elif level == 2:
            return self.code[:6]
        elif level == 3:
            return self.code[:8]
        elif level > self.level:
            return self.code[:8+level-3]
        else:
            return self.code

    def get_extent(self):
        if self.level == 1:
            width = WIDTH1
            height = HEIGHT1
        elif self.level == 2:
            width = WIDTH2
            height = HEIGHT2
        elif self.level == 3:
            width = WIDTH3
            height = HEIGHT3
        else:
            width = WIDTH3 / pow(2.0, self.level - 3.0)
            height = HEIGHT3 / pow(2.0, self.level - 3.0)

        return self.min_lon, self.min_lat, self.min_lon + width, self.min_lat + height


def mesh_by_area(extent, level=1):
    if level == 1:
        width = WIDTH1
        height = HEIGHT1
    elif level == 2:
        width = WIDTH2
        height = HEIGHT2
    elif level == 3:
        width = WIDTH3
        height = HEIGHT3
    else:
        width = WIDTH3 / pow(2.0, level - 3.0)
        height = HEIGHT3 / pow(2.0, level - 3.0)

    x_count = int((extent[2] - extent[0]) / width) + 1
    y_count = int((extent[3] - extent[1]) / height) + 1

    lon = extent[0]
    lat = extent[1]
    for i in range(y_count):
        lon = extent[0]
        for j in range(x_count):
            yield get_mesh(lon, lat, level)
            lon += width
        lat += height

def get_mesh(lon, lat, level=1):
    mesh_coordinate = lonlat2meshcode(lon, lat)
    code = map(str, mesh_coordinate[:2*level])
    mesh = JPMesh("".join(code))

    if level > 3:
        xc = lon - mesh.min_lon
        yc = lat - mesh.min_lat

        tile_length = pow(2, level - 3)

        x_index = int(xc / (WIDTH3 / pow(2.0, level - 3.0)))
        y_index = int(yc / (HEIGHT3 / pow(2.0, level - 3.0)))

        for i in range(3, level):
            digit = 1

            m = tile_length / 2
            
            if x_index >= m:
                digit += 1

            if y_index >= m:
                digit += 1
                digit += 1

            code.append(str(digit))

            x_index = x_index % m
            y_index = y_index % m

            tile_length = m
            
        mesh = JPMesh("".join(code))

    return mesh

    
def lonlat2meshcode(lon, lat):
    x1 = lon - 100
    y1 = lat * 1.5
    x1c, y1c = map(int, (x1, y1))

    x2 = (x1 - x1c) / WIDTH2
    y2 = (y1 - y1c) / (HEIGHT2 * 1.5)
    x2c, y2c = map(int, (x2, y2))

    x3 = (x2 - x2c) * WIDTH2 / WIDTH3
    y3 = (y2 - y2c) * (HEIGHT2 * 1.5) / (HEIGHT3 * 1.5)
    x3c, y3c = map(int, (x3, y3))

    return y1c, x1c, y2c, x2c, y3c, x3c

def meshcode2lonlat(code):
    code = code if isinstance(code, str) else str(code)
    y1 = int(code[:2])
    x1 = int(code[2:4]) 

    lon = x1 + 100.0
    lat = y1 / 1.5

    if len(code) > 4:
        y2 = int(code[4])
        x2 = int(code[5])
        lon += x2 * WIDTH2
        lat += y2 * HEIGHT2

    if len(code) > 6:
        y3 = int(code[6])
        x3 = int(code[7])
        lon += x3 * WIDTH3
        lat += y3 * HEIGHT3

    if len(code) > 8:
        for i in range(8, len(code)):
            c = int(code[i])
            x = (c - 1) % 2
            y = int(c / 3)
            lon += x * (WIDTH3 / pow(2.0,  i - 7))
            lat += y * (HEIGHT3 / pow(2.0, i - 7))
            
    return lon, lat
    

    
