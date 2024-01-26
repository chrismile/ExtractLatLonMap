# ExtractLatLonMap

Automated world map image cropping tool written in Python3 for use with [PCViewer](https://github.com/wavestoweather/PCViewer).

It loads a world map image and a NetCDF data set storing two variables `lat` and `lon`, and exports a cropped world map
showing only the range of latitudes and longitudes of the data grid.


## Prerequisites

This program has a few dependencies, which can for example be installed via conda with this command:

```sh
conda install anaconda::numpy anaconda::pillow conda-forge::netcdf4
```

Also, a world map image needs to be obtained from which the map should be cropped.
An example is the data provided by [Natural Earth](https://www.naturalearthdata.com/) available under public domain, e.g.:
https://www.naturalearthdata.com/http//www.naturalearthdata.com/download/10m/raster/HYP_HR_SR_OB_DR.zip


## Usage

How to call:

```sh
python3 extract_map.py -i <INPUT_FILENAME> -o <OUTPUT_FILENAME> -d <DATASET_FILE>
```

Example:

```sh
python3 extract_map.py -i HYP_HR_SR_OB_DR.tif -o cropped_map.png -d dataset.nc
```

Currently, `-i` and `-o` support any image format supported by the library PIL, while `-d` only supports NetCDF files.
The NetCDF data set file must contain two variables `lat` and `lon` specifying the latitude and longitude values of the
stored data points.
