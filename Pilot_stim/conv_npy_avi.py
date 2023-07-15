import os
import numpy as np
import imageio

def convert_npy_to_avi(input_folder, output_folder, fps):
    npy_files = [f for f in os.listdir(input_folder) if f.endswith('.npy')]

    for npy_file in npy_files:
        input_file = os.path.join(input_folder, npy_file)
        output_file = os.path.splitext(npy_file)[0] + '.avi'
        output_file = os.path.join(output_folder, output_file)

        video = np.load(input_file)
        height, width = video.shape[1], video.shape[2]
        frames = video.shape[0]
        writer = imageio.get_writer(output_file, fps=fps)

        for i in range(frames):
            frame = video[i]
            writer.append_data(frame)

        writer.close()

# Example usage
input_folder = 'Movies'
output_folder = 'Movies'
fps = 60
convert_npy_to_avi(input_folder, output_folder, fps)