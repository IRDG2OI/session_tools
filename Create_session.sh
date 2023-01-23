#!/bin/bash
######################################
# SCRIPT TO AUTOMATE FOLDER CREATION #
# Author: Sylvain POULAIN            #
# Released: September 2022           #
# Last update: 2022-09-09            #
######################################

# Set up your session:
SESSION_PATH=../DATA
YEAR=2022
MONTH=10
DAY=25
LOCATION=aldabra-arm01
PLATFORM=Mavic2Pro
BEGIN_SESSION=32
END_SESSION=33
######################################

for sess in $(seq ${BEGIN_SESSION} ${END_SESSION});
    do 
    FOLDER_NAME=uav_${YEAR}_${MONTH}_${DAY}_${LOCATION}_${PLATFORM}_${sess}
    echo "Folder structure creation:
        ${FOLDER_NAME}"
    mkdir -p ${SESSION_PATH}/${FOLDER_NAME}/DCIM
    echo "DCIM Folder created"
    mkdir -p ${SESSION_PATH}/${FOLDER_NAME}/GPS
    echo "GPS Folder created"
    mkdir -p ${SESSION_PATH}/${FOLDER_NAME}/METADATA
    echo "Metadata Folder created";
done
