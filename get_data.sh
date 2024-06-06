#!/bin/sh

rm -rf data
wget https://microsimulationtasha.blob.core.windows.net/population-synthesis/data.zip
unzip data.zip
rm data.zip
