# pyWebODM: process photogrammetry data with OpenDroneMap

Main goal: batch process from NextCloud
Description: Data are stored in folder with one convention: 
    `<project_name>/DCIM`
    where <project_name> is a name you could set according to your preferences


## Settings:

- Edit `sample_settings.py` to match your server and credentials
- Save as `settings.py`


## Usage:

`python process_webodm.py /path/to/my/images/DCIM/`


# Batch process (in bash):

```
for project in /path/to/my/session* ;
  do python process_webodm.py ${project}/DCIM/ ;
done
```