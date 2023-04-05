# Geotiff with alpha band and jpeg compression

Geoserver doesn't support Geotiff with alpha band and jpeg compression made with GDAL. (Needs funding to be done)

## Example which is prone to fail : 
```bash
gdal_translate -co COMPRESS=JPEG -co JPEG_QUALITY=75 in.tif out.tif
```

## Workaround: use a mask
```bash
gdal_translate -co COMPRESS=JPEG -co JPEG_QUALITY=75 -b 1 -b 2 -b 3 -mask 4 -co PHOTOMETRIC=YCBCR --config GDAL_TIFF_INTERNAL_MASK YES in.tif out.tif
```

### References:
- https://matrix.to/#/!eRmmLjsPElFqHofPCc:gitter.im/$mi0z4UDau4p6UfKjj5i85UMkCuk8kRBJ65C4-XsK30s?via=gitter.im&via=matrix.org&via=hive-mind.network
- https://gis.stackexchange.com/questions/361277/geoserver-fails-to-read-a-jpeg-compressed-tiff-with-alpha-band

---

> _Created on 2023-03-31 by Sylvain Poulain_
