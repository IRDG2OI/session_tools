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
- https://app.element.io/#/room/#geoserver_geoserver:gitter.im/$pgM7xx7WRPCE5GNqfGGG2Yits3IF-yT7ajhDRXtpncM
- https://gis.stackexchange.com/questions/361277/geoserver-fails-to-read-a-jpeg-compressed-tiff-with-alpha-band

---

> _Created on 2023-03-31 by Sylvain Poulain_