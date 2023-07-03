# This script load npy files and downcast them to uint8.
#
# Usage:
# python downcast_uint8.py --input_path ./data/bar_frame_du.npy --output_path ./data/bar_frame_du_uint8.npy
import os 
import numpy as np

path_to_folder = os.path.dirname(os.path.abspath(__file__))

# We first loop across the npy files
for file_name in os.listdir(path_to_folder):
    if '.npy' in file_name:
        local_array = np.load(os.path.join(path_to_folder, file_name))

        # We downcast the array to uint8
        local_array = local_array.astype(np.uint8)

        # We save the array
        np.save(os.path.join(path_to_folder, file_name.replace('.npy', '_uint8.npy')), local_array)