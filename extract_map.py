# BSD 2-Clause License
#
# Copyright (c) 2024, Christoph Neuhauser
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import math
import sys
import numpy as np
from PIL import Image
import netCDF4


def save_image(output_filename, image_out):
    image_out.save(output_filename)
    pass


def main():
    args_dict = {
        'i': None,  # Input world map file path
        'o': None,  # Output cropped world map file path
        'd': None,  # NetCDF data set file path
    }

    # Parse the command line arguments.
    for i in range(1, len(sys.argv), 2):
        key = sys.argv[i][1:]
        value = sys.argv[i + 1]
        # Guess the correct type
        if isinstance(args_dict[key], int):
            args_dict[key] = int(value)
        elif isinstance(args_dict[key], float):
            args_dict[key] = float(value)
        elif isinstance(args_dict[key], bool):
            args_dict[key] = bool(value)
        elif isinstance(args_dict[key], str):
            args_dict[key] = value
        elif args_dict[key] == None:
            args_dict[key] = value
        else:
            print('Error: Unhandled type.', file=sys.stderr)
            args_dict[key] = value

    if args_dict['i'] == None:
        print('Error: Missing input world map file path.', file=sys.stderr)
        return
    if args_dict['o'] == None:
        print('Error: Missing output world map file path.', file=sys.stderr)
        return
    if args_dict['d'] == None:
        print('Error: Missing data set file path.', file=sys.stderr)
        return

    Image.MAX_IMAGE_PIXELS = None
    image_in = Image.open(args_dict['i'])
    w, h = image_in.size

    data_path = '/mnt/data/Flow/Amemiya/analysis_1000mem/0001/init_merge_xyz_20210730-060000.000.pe000000.nc'
    ncfile = netCDF4.Dataset(data_path, 'r')
    lats = ncfile['lat']
    lons = ncfile['lon']
    min_lat = np.min(lats)
    max_lat = np.max(lats)
    min_lon = np.min(lons)
    max_lon = np.max(lons)
    min_norm_x = min_lon / 360.0 + 0.5
    max_norm_x = max_lon / 360.0 + 0.5
    min_norm_y = 1.0 - (max_lat / 180.0 + 0.5)
    max_norm_y = 1.0 - (min_lat / 180.0 + 0.5)

    min_x = math.floor(min_norm_x * w)
    max_x = math.floor(max_norm_x * w)
    min_y = math.floor(min_norm_y * h)
    max_y = math.floor(max_norm_y * h)

    crop_box = (min_x, min_y, max_x, max_y)
    image_out = image_in.crop(crop_box)

    image_out.save(args_dict['o'])


if __name__ == '__main__':
    main()
