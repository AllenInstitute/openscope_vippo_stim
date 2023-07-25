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


"""
runs optotagging code for ecephys pipeline experiments
by joshs@alleninstitute.org, corbettb@alleninstitute.org, chrism@alleninstitute.org, jeromel@alleninstitute.org

(c) 2018 Allen Institute for Brain Science
"""
import datetime
import pickle as pkl
from copy import deepcopy

def run_optotagging(levels, conditions, waveforms, isis, sampleRate = 10000.):

    from toolbox.IO.nidaq import AnalogOutput
    from toolbox.IO.nidaq import DigitalOutput

    sweep_on = np.array([0,0,1,0,0,0,0,0], dtype=np.uint8)
    stim_on = np.array([0,0,1,1,0,0,0,0], dtype=np.uint8)
    stim_off = np.array([0,0,1,0,0,0,0,0], dtype=np.uint8)
    sweep_off = np.array([0,0,0,0,0,0,0,0], dtype=np.uint8)

    ao = AnalogOutput('Dev1', channels=[1])
    ao.cfg_sample_clock(sampleRate)

    do = DigitalOutput('Dev1', 2)

    do.start()
    ao.start()

    do.write(sweep_on)
    time.sleep(5)

    for i, level in enumerate(levels):

        print(level)

        data = waveforms[conditions[i]]

        do.write(stim_on)
        ao.write(data * level)
        do.write(stim_off)
        time.sleep(isis[i])

    do.write(sweep_off)
    do.clear()
    ao.clear()

def generatePulseTrain(pulseWidth, pulseInterval, numRepeats, riseTime, sampleRate = 10000.):

    data = np.zeros((int(sampleRate),), dtype=np.float64)
   # rise_samples =

    rise_and_fall = (((1 - np.cos(np.arange(sampleRate*riseTime/1000., dtype=np.float64)*2*np.pi/10))+1)-1)/2
    half_length = int(rise_and_fall.size / 2)
    rise = rise_and_fall[:half_length]
    fall = rise_and_fall[half_length:]

    peak_samples = int(sampleRate*(pulseWidth-riseTime*2)/1000)
    peak = np.ones((peak_samples,))

    pulse = np.concatenate((rise, \
                           peak, \
                           fall))

    interval = int(pulseInterval*sampleRate/1000.)

    for i in range(0, numRepeats):
        data[i*interval:i*interval+pulse.size] = pulse

    return data

def optotagging(mouse_id, operation_mode='experiment', level_list = [1.15, 1.28, 1.345], output_dir = 'C:/ProgramData/camstim/output/'):

    sampleRate = 10000

    # 1 s cosine ramp:
    data_cosine = (((1 - np.cos(np.arange(sampleRate, dtype=np.float64)
                                * 2*np.pi/sampleRate)) + 1) - 1)/2  # create raised cosine waveform

    # 1 ms cosine ramp:
    rise_and_fall = (
        ((1 - np.cos(np.arange(sampleRate*0.001, dtype=np.float64)*2*np.pi/10))+1)-1)/2
    half_length = int(rise_and_fall.size / 2)

    # pulses with cosine ramp:
    pulse_2ms = np.concatenate((rise_and_fall[:half_length], np.ones(
        (int(sampleRate*0.001),)), rise_and_fall[half_length:]))
    pulse_5ms = np.concatenate((rise_and_fall[:half_length], np.ones(
        (int(sampleRate*0.004),)), rise_and_fall[half_length:]))
    pulse_10ms = np.concatenate((rise_and_fall[:half_length], np.ones(
        (int(sampleRate*0.009),)), rise_and_fall[half_length:]))

    data_2ms_10Hz = np.zeros((sampleRate,), dtype=np.float64)

    for i in range(0, 10):
        interval = int(sampleRate / 10)
        data_2ms_10Hz[i*interval:i*interval+pulse_2ms.size] = pulse_2ms

    data_5ms = np.zeros((sampleRate,), dtype=np.float64)
    data_5ms[:pulse_5ms.size] = pulse_5ms

    data_10ms = np.zeros((sampleRate,), dtype=np.float64)
    data_10ms[:pulse_10ms.size] = pulse_10ms

    data_10s = np.zeros((sampleRate*10,), dtype=np.float64)
    data_10s[:-2] = 1

    ##### THESE STIMULI ADDED FOR OPENSCOPE GLO PROJECT #####
    data_10ms_5Hz = generatePulseTrain(10, 200, 5, 1) # 1 second of 5Hz pulse train. Each pulse is 10 ms wide
    data_6ms_40Hz = generatePulseTrain(6, 25, 40, 1)  # 1 second of 40 Hz pulse train. Each pulse is 6 ms wide
    #########################################################

    # for experiment

    isi = 1.5
    isi_rand = 0.5
    numRepeats = 50

    condition_list = [3, 4, 5]
    waveforms = [data_2ms_10Hz, data_5ms, data_10ms, data_cosine, data_10ms_5Hz, data_6ms_40Hz]

    opto_levels = np.array(level_list*numRepeats*len(condition_list)) #     BLUE
    opto_conditions = condition_list*numRepeats*len(level_list)
    opto_conditions = np.sort(opto_conditions)
    opto_isis = np.random.random(opto_levels.shape) * isi_rand + isi

    p = np.random.permutation(len(opto_levels))

    # implement shuffle?
    opto_levels = opto_levels[p]
    opto_conditions = opto_conditions[p]

    # for testing

    if operation_mode=='test_levels':
        isi = 2.0
        isi_rand = 0.0

        numRepeats = 2

        condition_list = [0]
        waveforms = [data_10s, data_10s]

        opto_levels = np.array(level_list*numRepeats*len(condition_list)) #     BLUE
        opto_conditions = condition_list*numRepeats*len(level_list)
        opto_conditions = np.sort(opto_conditions)
        opto_isis = np.random.random(opto_levels.shape) * isi_rand + isi

    elif operation_mode=='pretest':
        numRepeats = 1

        condition_list = [0]
        data_2s = data_10s[-sampleRate*2:]
        waveforms = [data_2s]

        opto_levels = np.array(level_list*numRepeats*len(condition_list)) #     BLUE
        opto_conditions = condition_list*numRepeats*len(level_list)
        opto_conditions = np.sort(opto_conditions)
        opto_isis = [1]*len(opto_conditions)
    #

    outputDirectory = output_dir
    fileDate = str(datetime.datetime.now()).replace(':', '').replace(
        '.', '').replace('-', '').replace(' ', '')[2:14]
    fileName = os.path.join(outputDirectory, fileDate + '_'+mouse_id + '.opto.pkl')

    print('saving info to: ' + fileName)
    fl = open(fileName, 'wb')
    output = {}

    output['opto_levels'] = opto_levels
    output['opto_conditions'] = opto_conditions
    output['opto_ISIs'] = opto_isis
    output['opto_waveforms'] = waveforms

    pkl.dump(output, fl)
    fl.close()
    print('saved.')

    #
    run_optotagging(opto_levels, opto_conditions,
                    waveforms, opto_isis, float(sampleRate))
"""
end of optotagging section
"""

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
                                        fps=fps)
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

def create_receptive_field_mapping(window, number_runs = 15):
    x = np.arange(-40,45,10)
    y = np.arange(-40,45,10)
    position = []
    for i in x:
        for j in y:
            position.append([i,j])

    stimulus = Stimulus(visual.GratingStim(window,
                        units='deg',
                        size=20,
                        mask="circle",
                        texRes=256,
                        sf=0.1,
                        ),
        sweep_params={
                'Pos':(position, 0),
                'Contrast': ([0.8], 4),
                'TF': ([4.0], 1),
                'SF': ([0.08], 2),
                'Ori': ([0,45,90], 3),
                },
        sweep_length=0.25,
        start_time=0.0,
        blank_length=0.0,
        blank_sweeps=0,
        runs=number_runs,
        shuffle=True,
        save_sweep_table=True,
        )
    stimulus.stim_path = r"C:\\not_a_stim_script\\receptive_field_block.stim"

    return stimulus

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
        if 'green' in local_path or 'disco' in local_path or 'natmovie' in local_path:
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

    return stims, end_time

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
    
    # An integer representing the number of repeats. This is used to determine the number of times each movie clip is played.
    # final number of repeats is the product of the n_repeats and the repeats_array
    # At production, this should be 10
    N_REPEATS = json_params.get('n_repeats', 5)
    ADD_RF = json_params.get('add_rf', True)
    number_runs_rf = json_params.get('number_runs_rf', 1) # 8 is the number of repeats for prod(8min).

    # mtrain should be providing : Gamma1.Luminance50
    monitor_name = json_params.get('monitor_name', "testMonitor")
    opto_disabled = json_params.get('disable_opto', True)

    # Paths to the movie clip files to load.
    # We construct the paths to the movie clips based on the SESSION_PARAMS_movie_folder
    repeats_array = N_REPEATS*np.array([2,1,1,1,1,2,2,1,2,2,1,2,1,1,1,1,1])
    movie_clip_files = ['LRRL_2_thin_bar.npy', 'LRRL_10_thin_bar.npy',
                    'left_right_speed_2.0.npy', 'LRRL_2_thick_bar.npy','LRRL_2_thin_bar_flippedContrast.npy',
                    'UDDU_2_thin_bar.npy','ERCR.npy','div_3.npy',
                    'curl_cw_July20.npy','curl_acw_July20.npy',
                    'CLRRL_2_green_green.npy','CLRRL_2_disco_disco.npy',
                    'natmovie_EagleSwooping1_480x270.npy','natmovie_EagleSwooping2_480x270.npy',
                    'natmovie_Squirreland3Mice_480x270.npy','natmovie_CricketsOnARock_480x270.npy','natmovie_BlackSnakeSlithering_480x270.npy']
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

    stims, end_time = make_movie_stimulus(movie_clip_files, window, repeats_array)

    if ADD_RF:
        gabors_rf_20  = create_receptive_field_mapping(window, number_runs_rf)
        gabors_rf_20_ds = [(end_time, end_time+60*number_runs_rf)]
        gabors_rf_20.set_display_sequence(gabors_rf_20_ds)
        stims.append(gabors_rf_20)    
        
        end_time = end_time+60*number_runs_rf

    logging.info("Stimulus end at : %f min", (end_time)/60)

    # Note that pre_blank_sec and post_blank_sec are set to 0.0 by default.
    # You can change these parameters to add a blank period before and after the movie clip. 
    ss = SweepStim(window,
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
    
    ss.add_item(f, "foraging")

    # run it
    try:
        ss.run()
    except SystemExit:
        print("We prevent camstim exiting the script to complete optotagging")

    if not(opto_disabled):
        from camstim.misc import get_config
        from camstim.zro import agent
        opto_params = deepcopy(json_params.get("opto_params"))
        opto_params["mouse_id"] = json_params["mouse_id"]
        opto_params["output_dir"] = agent.OUTPUT_DIR
        #Read opto levels from stim.cfg file
        config_path = agent.CAMSTIM_CONFIG_PATH
        stim_cfg_opto_params = get_config(
            'Optogenetics',
            path=config_path,
        )
        opto_params["level_list"] = stim_cfg_opto_params["level_list"]

        optotagging(**opto_params)