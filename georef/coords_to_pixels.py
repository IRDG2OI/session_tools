from osgeo import gdal

driver = gdal.GetDriverByName('GTiff')
filename = "/run/media/sylvain/G2OI_1/IRD/MayotteFMR/MS/AEROPORT/Copy-of-Aerorport-Vol1-9-14-2022-dsm.tif" #path to raster
dataset = gdal.Open(filename)
band = dataset.GetRasterBand(1)

cols = dataset.RasterXSize
rows = dataset.RasterYSize

transform = dataset.GetGeoTransform()

xOrigin = transform[0]
yOrigin = transform[3]
pixelWidth = transform[1]
pixelHeight = -transform[5]

data = band.ReadAsArray(0, 0, cols, rows)

points_list = [ (
        530322.8458460423, 8582258.036070595
        ), (
        530317.0823187487, 8582258.38845603
        ), (
        530318.9869019467, 8582261.295442685
        ) ] #list of X,Y coordinates

for point in points_list:
    col = int((point[0] - xOrigin) / pixelWidth)
    row = int((yOrigin - point[1] ) / pixelHeight)

    print('-gcp', col, row, point[0], point[1] # pixels coords
         # data[col][row] ## raster value
         )
