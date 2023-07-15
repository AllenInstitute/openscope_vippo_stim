import psychopy.visual
import camstim
from camstim import Stimulus, SweepStim, Foraging, Window, Warp, MovieStim
import os
import yaml
import numpy as np
from psychopy import monitors
import argparse
import logging
from camstim.misc import ImageStimNumpyuByte
from psychopy import visual
import pyglet
GL = pyglet.gl

class ColorImageStimNumpyuByte(ImageStimNumpyuByte):

    '''Subclass of ImageStim which allows fast updates of numpy ubyte images,
       bypassing all internal PsychoPy format conversions.
    '''

    def __init__(self,
                 win,
                 image=None,
                 mask=None,
                 units="",
                 pos=(0.0, 0.0),
                 size=None,
                 ori=0.0,
                 color=(1.0, 1.0, 1.0),
                 colorSpace='rgb',
                 contrast=1.0,
                 opacity=1.0,
                 depth=0,
                 interpolate=False,
                 flipHoriz=False,
                 flipVert=False,
                 texRes=128,
                 name='',
                 autoLog=True,
                 maskParams=None):
        
        if image is None or type(image) != np.ndarray:
            raise ValueError(
                'ImageStimNumpyuByte must be numpy.ubyte ndarray (0-255)')

        self.interpolate = interpolate

        # convert incoming Uint to RGB trio only during initialization to keep PsychoPy happy
        # else, error is: ERROR   numpy arrays used as textures should be in
        # the range -1(black):1(white)
        data = np.zeros((image.shape[0], image.shape[1], 3), np.float32)
        # (0 to 255) -> (-1 to +1)
        fimage = image.astype(np.float32) / 255 * 2.0 - 1.0
        data[:, :, 0] = fimage[: , :, 0]#R
        data[:, :, 1] = fimage[: , :, 1]#R
        data[:, :, 2] = fimage[: , :, 2]#R

        visual.ImageStim.__init__(self,
                                  win,
                                  image=data,
                                  mask=mask,
                                  units=units,
                                  pos=pos,
                                  size=size,
                                  ori=ori,
                                  contrast=contrast,
                                  opacity=opacity,
                                  depth=depth,
                                  interpolate=interpolate,
                                  flipHoriz=flipHoriz,
                                  flipVert=flipVert,
                                  texRes=texRes,
                                  name=name, autoLog=autoLog,
                                  maskParams=maskParams)

        self.setImage = self.setReplaceImage
        self.setImage(image)

    def setReplaceImage(self, tex):
            '''
            Use this function instead of 'setImage' to bypass format conversions
            and increase movie playback rates.
            '''
            #intensity = tex.astype(numpy.ubyte)
            intensity = tex
            internalFormat = GL.GL_RGB
            pixFormat = GL.GL_RGB
            dataType = GL.GL_UNSIGNED_BYTE
            # data = numpy.ones((intensity.shape[0],intensity.shape[1],3),numpy.ubyte)#initialise data array as a float
            # data[:,:,0] = intensity#R
            # data[:,:,1] = intensity#G
            # data[:,:,2] = intensity#B
            data = intensity
            texture = tex.ctypes  # serialise
            try:
                tid = self._texID  # psychopy renamed this at some point.
            except AttributeError:
                tid = self.texID
            GL.glEnable(GL.GL_TEXTURE_2D)
            GL.glBindTexture(GL.GL_TEXTURE_2D, tid)
            # makes the texture map wrap (this is actually default anyway)
            if self.interpolate:
                interpolation = GL.GL_LINEAR
            else:
                interpolation = GL.GL_NEAREST
            GL.glTexParameteri(GL.GL_TEXTURE_2D,
                            GL.GL_TEXTURE_WRAP_S, GL.GL_REPEAT)
            GL.glTexParameteri(GL.GL_TEXTURE_2D,
                            GL.GL_TEXTURE_MAG_FILTER, interpolation)
            GL.glTexParameteri(GL.GL_TEXTURE_2D,
                            GL.GL_TEXTURE_MIN_FILTER, interpolation)
            GL.glTexImage2D(GL.GL_TEXTURE_2D, 0, internalFormat,
                            # [JRG] for non-square, want data.shape[1], data.shape[0]
                            data.shape[1], data.shape[0], 0,
                            pixFormat, dataType, texture)
            pass
    
class ColorMovieStim(MovieStim):
    """
    A movie stimulus designed for playing Numpy uint8 movies of arbitrary
        size/resolution.
    """
    def __init__(self,
                 movie_path,
                 window,
                 frame_length,
                 size=(640,480),
                 pos=(0,0),
                 start_time=0.0,
                 stop_time=None,
                 blank_length=0,
                 blank_sweeps=0,
                 runs=1,
                 shuffle=False,
                 fps=60.0,
                 flip_v=False,
                 flip_h=False,
                 interpolate=False,
                 ):

        self.movie_path = movie_path
        self.frame_length = frame_length

        movie_data = self.load_movie(movie_path)

        psychopy_stimulus = ColorImageStimNumpyuByte(window,
                                                image=movie_data[0],
                                                size=size,
                                                pos=pos,
                                                units='pix',
                                                flipVert=flip_v,
                                                flipHoriz=flip_h,
                                                interpolate=interpolate)
        sweep_params = {
            'ReplaceImage': (movie_data, 0),
        }
        super(MovieStim, self).__init__(psychopy_stimulus,
                                        sweep_params,
                                        sweep_length=frame_length,
                                        start_time=start_time,
                                        stop_time=stop_time,
                                        blank_length=blank_length,
                                        blank_sweeps=blank_sweeps,
                                        runs=runs,
                                        shuffle=shuffle,
                                        fps=fps,
                                        save_sweep_table=False)
    def load_movie(self, path):
        """
        Loads a movie from a specified path.  Currently only supports .npy files.
        """
        if path[-3:] == "npy":
            return self.load_numpy_movie(path)
        else:
            raise IOError("Incorrect movie file type.")

    def load_numpy_movie(self, path):
        """
        Loads a numpy movie.  Ensures that it is read as a contiguous array and
            three dimensional.
        """
        self.movie_local_path = self._local_copy(path)
        movie_data = np.ascontiguousarray(np.load(self.movie_local_path))

        # check shape/type
        if not movie_data.dtype in [np.uint8, np.ubyte]:
            raise ValueError("Movie must be dtype numpy.uint8")

        return movie_data

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
        print("Loading {}".format(local_path))
        local_movie = np.load(local_path)
        array_size = local_movie.shape

        # Note here that the end time is calculated by dividing the array size by frame 
        # rate (60 fps) and adding it to the current time. 
        end_time = current_time + array_size[0]*repeats[counter] / 60.0

        # You can change the runs parameter to change the number of times the movie clip is played.
        # We use the MoieStim class to create the stimulus except we use the ColorMovieStim class
        # instead of the MovieStim class for the last 2 movies.
        if 'green' in local_path or 'disco' in local_path:
            s = ColorMovieStim(movie_path=local_path,
                        window=window,
                        frame_length=1.0 / 60.0,
                        size=(1920, 1080),
                        start_time=0.0,
                        stop_time=None,
                        flip_v=True, runs=repeats[counter])
        else:
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
    repeats_array = [1,1,1,1,1,1,1,1,1,1]#[100,20,100,100,50,100,100,50]#,50,100]
    movie_clip_files = ['LRRL_2_thin_bar.npy', 'LRRL_10_thick_bar.npy',
                        'right_left_speed_2.0.npy', 'LRRL_2_thick_bar.npy',
                       'UDDU_2_thin_bar.npy','ERCR.npy','div_3.npy',
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