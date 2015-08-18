# coding: utf-8

class Mesh(object):
    def __init__(self, code):
        self.code = code

class JPMesh1(Mesh):
    pass

class JPMesh2(Mesh):
    pass

class JPMesh3(Mesh):
    pass

class JPMeshS(Mesh):
    pass


def generate_mesh()
    pass

def lonlat2mesh1(lon, lat):
    x = (int(lon) - 100)
    y = int(lat * 1.5)

    return x, y

def lonlat2mesh2(lon, lat):
    x1, y1 = lonlat2mesh1(lon, lat)
    x2s = lon - x1
    y2s = lat * 1.5 - 

