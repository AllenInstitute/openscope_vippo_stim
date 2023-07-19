import psychopy.visual
import camstim
from camstim import Stimulus, SweepStim, Foraging, Window, Warp, MovieStim
import os
import yaml
import numpy as np
from psychopy import monitors
import argparse
import logging
def make_movie_stimulus(movie_paths, window, repeats):
    """Generate a Stimulus that plays a series of movie clips in a specified order."""

    # Convert the order into a list of display sequence tuples. There should be one display sequence list per movie
    # clip. Each display sequence list contains a set of tuples of the form (start_second, stop_second). Theses tuples
    # define the start and stop time for when to play the clip and are determined by the order vector
    display_sequences = []
    current_time = 0.0
    stims = []
    counter = 0
    
    for local_path in movie_paths:
        local_movie = np.load(local_path)
        array_size = local_movie.shape

        # Note here that the end time is calculated by dividing the array size by frame 
        # rate (60 fps) and adding it to the current time. 
        end_time = current_time + array_size[0]*repeats[counter] / 60.0

        # You can change the runs parameter to change the number of times the movie clip is played.
        s = MovieStim(movie_path=local_path,
                        window=window,
                        frame_length=1.0 / 60.0,
                        size=(1920, 1080),
                        start_time=0.0,
                        stop_time=None,
                        flip_v=True, runs=repeats[counter])
        s.set_display_sequence([(current_time, end_time)])

        # Added to facilitate creating the NWB files
        s.stim_path = local_path

        counter = counter + 1
        stims.append(s)
        current_time = end_time

    # Note that pre_blank_sec and post_blank_sec are set to 0.0 by default.
    # You can change these parameters to add a blank period before and after the movie clip. 
    stim = SweepStim(window,
                     stimuli=stims,
                     # pre_blank_sec=1,
                     # post_blank_sec=1,
                     params={},
                     )

    # add in foraging so we can track wheel, potentially give rewards, etc
    f = Foraging(window = window,
                    auto_update = False,
                    params= {}
                    )
    
    stim.add_item(f, "foraging")

    return stim

if __name__ == "__main__":
    parser = argparse.ArgumentParser("mtrain")
    parser.add_argument("json_path", nargs="?", type=str, default="")

    args, _ = parser.parse_known_args() # <- this ensures that we ignore other arguments that might be needed by camstim
    
    # print args
    if args.json_path == "":
        logging.warning("No json path provided, using default parameters. THIS IS NOT THE EXPECTED BEHAVIOR FOR PRODUCTION RUNS")
        json_params = {}
    else:
        with open(args.json_path, 'r') as f:
            # we use the yaml package here because the json package loads as unicode, which prevents using the keys as parameters later
            json_params = yaml.load(f)
            logging.info("Loaded json parameters from mtrain")
            # end of mtrain part

    # Copied monitor and window setup from:
    # https://github.com/AllenInstitute/openscope-glo-stim/blob/main/test-scripts/cohort-1-test-12min-drifting.py

    dist = 15.0
    wid = 52.0

    # mtrain should be providing : a path to a network folder or a local folder with the entire repo pulled
    SESSION_PARAMS_movie_folder = json_params.get('movie_folder', os.path.abspath("data"))
    
    # An integer representing the day of the experiment. Defaults to Day 0.
    SESSION_PARAMS_day = json_params.get('day', 0)

    # mtrain should be providing : Gamma1.Luminance50
    monitor_name = json_params.get('monitor_name', "testMonitor")

    # Paths to the movie clip files to load.
    # We construct the paths to the movie clips based on the SESSION_PARAMS_movie_folder
    repeats_array = [100,20,100,100,50,100,100,50,50,50,50]
    movie_clip_files = ['LRRL_2_thin_bar.np', 'LRRL_10_thick_bar.npy',
                        'right_left_speed_2.0.npy', 'LRRL_2_thick_bar.npy',
                       'UDDU_2_thin_bar.npy','ERCR.npy','div_3.npy','curl_cw.npy','curl_acw.npy',
                       'CLRRL_2_green_green.npy','CLRRL_2_disco_disco.npy']
    movie_clip_files = [os.path.join(SESSION_PARAMS_movie_folder, f) for f in movie_clip_files]

    for clip_path in movie_clip_files:
        if not os.path.exists(clip_path):
            raise ValueError("Movie clip file not found: {}. Make sure ".format(clip_path) +
                            "to download and place them in the data folder.")

    # create a monitor
    if monitor_name == 'testMonitor':
        monitor = monitors.Monitor(monitor_name, distance=dist, width=wid)
    else:
        monitor = monitor_name
        
    # Create display window
    window = Window(fullscr=True, # Will return an error due to default size. Ignore.
                    monitor=monitor,  # Will be set to a gamma calibrated profile by MPE
                    screen=0,
                    warp=Warp.Spherical
                    )

    ss = make_movie_stimulus(movie_clip_files, window ,repeats_array)

    ss.run()