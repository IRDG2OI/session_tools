#########################################
###  Batch Ardupilot Mission Planner  ###
###    ".poly" files to GIS format    ###
#########################################


library(sf)
library(sp)
library(rgdal)

# All files in this directory and all subfolders with file ending .poly will be converted to geopackage and kml.
# It is assumed that the .poly file has a comment lines using #.
# Coordinates of the polygon are in Lat Long and in WGS84 format. Space as separator
setwd("/home/sylvain/Documents/IRD/Monaco/mission_planner_prelim_traj/")

lof <- list.files(path=".", recursive=T, pattern=".\\.poly")

for (i in 1:length(lof)) {
  dir <- dirname(lof[i])
  fname <- basename(lof[i])
  gpkgname <- strsplit(lof[i], "_")[[1]][1]
  fnameWithoutEnding <- strsplit(fname, "\\.")[[1]][1]
  
  loc <- read.csv(file=lof[i], header=F, sep=" ", comment.char="#")
  pol <- st_sfc(
    #st_polygon(
    st_multilinestring(
      list(
      cbind(c(loc$V2), c(loc$V1)
      )
    )
    )
  , crs = 4326)
  st_write(pol, dsn=paste0(dir, "/", gpkgname, ".gpkg"),
           fnameWithoutEnding, append = TRUE)
  st_write(pol, dsn=paste0(dir, "/", fnameWithoutEnding, ".kml"),
           fnameWithoutEnding, append = TRUE)
  }

