# Auto mask over water

## Apply thin mask according to surexposition
```
convert DJI_0514.JPG -fuzz 20% -transparent white -negate -alpha extract DJI_0514_maskn.JPG 
```

## Densify 1/2 mask using disk shape
```
convert DJI_0514_maskn.JPG -morphology Dilate Disk DJI_0514_dilated_disk.JPG
```

## Densify 2/2 using Octagon shape
```
convert DJI_0514_dilated_disk.JPG -morphology Dilate Octagon DJI_0514_dilated_disk_then_octagon.JPG
```

## Reverse image to match photogrammetry mask
```
convert -negate DJI_0514_dilated_disk_then_octagon.JPG DJI_0514_mask.PNG
```
### Automated bash script:
```
#!/bin/bash
for i in *.JPG;
  do 
    convert $i -fuzz 20% -transparent white -negate -alpha extract ${i%.JPG}_maskn.JPG
    convert ${i%.JPG}_maskn.JPG -morphology Dilate Disk ${i%.JPG}_dilated_disk.JPG
    convert ${i%.JPG}_dilated_disk.JPG -morphology Dilate Octagon ${i%.JPG}_dilated_disk_then_octagon.JPG
    convert -negate ${i%.JPG}_dilated_disk_then_octagon.JPG ${i%.JPG}_mask.PNG
    rm *maskn*
    rm *dilated*
done
```
