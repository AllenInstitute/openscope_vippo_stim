## Installation

### Dependencies:

- Windows OS (see **Camstim package**)
- python 2.7
- psychopy 1.82.01
- camstim 0.2.4

### Installation with [Anaconda](https://docs.anaconda.com/anaconda/install/) or [Miniconda](https://docs.conda.io/en/latest/miniconda.html):

1. Navigate to repository and install conda environment.  
    `conda env create -f environment.yml`
2. Activate the environment.  
    `conda activate allen_stimulus`
3. Install the AIBS `camstim` package in the environment.  
    `pip install camstim/.`
4. Download required video clips from [movie_clips.zip](https://tigress-web.princeton.edu/~dmturner/allen_stimulus/movie_clips.zip)
   Extract into the `data` directory.
   
### Input Files

The software requires two sets of input files. There should be a set of text files present under `data/stimulus_orderings` that indicate the display order of video clips for different phases of the experiment. In addition, there should be a set of video clips (stored as raw .npy files). These clips must be downloaded and extracted into the data folder from [movie_clips.zip](https://tigress-web.princeton.edu/~dmturner/allen_stimulus/movie_clips.zip)

### Stimulus design

1. Pilot stimuli:
    + movie clip A: Left to right moving bar
        - Low speed : 10 sec X 2
        - Medium speed : 2 sec X 2
        - High speed : 0.6 sec X 2
    + movie clip B: Right to left moving bar
        - Low speed : 10 sec X 2
        - Medium speed : 2 sec X 2
        - High speed : 0.6 sec X 2
    + movie clip C: Up down moving bar
        - Low speed : 10 sec X 2
        - Medium speed : 2 sec X 2
        - High speed : 0.6 sec X 2
    + movie clip D: Rotating bar
        - Low speed : 10 sec X 2
        - Medium speed : 2 sec X 2
        - High speed : 0.6 sec X 2
    + movie clip E: Rich bar
        - Flickering bar : 2 sec X 2
        - Disco bar : 2sec X 2
        - Movie of rat mving through the screen : 2sec X 2


2. [Clips for stim generation](https://drive.google.com/drive/folders/14B9YlA_-adNRlzoag-XGWW37W226WOFP?usp=sharing)
3. 7/28/2023 clips with edits such that the bars of light do not vanish from the screen, unless desired
   https://drive.google.com/file/d/1vGJmQficb5YFm3sxAQGwbFOo5rVQzAwY/view?usp=sharing
4. The clips used on 7/28/2023 above had an issue related to warping and screen dimensions. Latest NPY files can be created by the matlab code attached "StimGenerationCode_July30.m". 540x960 npy files are created, but their active region is only the central 584x460. Seems to warp properly
   https://drive.google.com/file/d/1OKfV6Cp71OXX1ki9ZOLn18qhXxj44raN/view?usp=sharing
   
5. Nov 9 2023 - A new set of clips, based on 2 pilot mice #072 and 077. 2 new types of stimuli were added, coherent dot motion, and scrambled bar of light. The 5 earlier movie clips were replaced by only 2 clips but of 20seconds each, compared to 4 seconds earlier. The ordering of stimuli was changed on 11/9 such that there are effectively 2 blocks, and the order if stimuli is reversed in the second block. The data folder containing these latest .npy files should be downloaded from
      https://drive.google.com/file/d/1CYJjxVQ2mn0RfuqADjBIRASNc2m1QRvM/view?usp=drive_link

6. Jan 11 2024 - Minor modification in the set of clips for bars of light, additional movie based stimuli, based on 2 pilot mice #062-64 and 321. Block structure with reversed order retained as in above, Nov 9 version. Slow bar of light is now 3 times slower, ie 12 seconds per loop. Long-off vanishing at the edges bar of light removed, for time constraints, one-way naso-temporal and temporo-nasal both stimuli now included. For the movies, there is the Eagle swooping 20second clip which gave great prevalence of selectivity in the pilots, and its faster 10sec version is added. Current play_stim and attached files have 2 other variants of the same movie, with obstruction in space and 2 versions with the same movie flipped left to right and up to down. Stimuli were renamed, so that in the future version with 1 trial each kind presentation (montage/"movie grande"), the current order as specified should be used. The data folder containing these latest .npy files should be downloaded from 
   https://drive.google.com/drive/folders/1UAI7SUVaPplvTGs8zN9mCWaxcCGjh4rm?usp=drive_link

7. Feb 2 2024 - Major modification, based on the neural responses we saw in early production mice and pilot mice. Many neurons showed mean rate changes between stimuli, specially between bars of light vs Eagle movie. To rule out that this is an effect of long time-scale neural drift/ units moving with respect to the recording probe, we now have a new way of presenting stimuli, which is called "montage". A single montage is 252 seconds long and consists of 2 repeats of each of the stimuli from before, so if the earlier stimuli were A, B C... then a Montage is (AABBCC...). Flips and obstructions are repeated 1 time each in a montage, and this montage is shown again and again in many trials (AABB...Flip1Flip2...)(AABB...Flip1Flip2...)(). The data folder containing this singular .npy file should be downloaded from
   https://drive.google.com/drive/folders/1VAnePYN3UPFIk7BfutvXVbyv87NskeV0?usp=drive_link
   Update to the same stimuli on 8th Feb 2024 - The Montage is now padded on either side with blocks of stimuli (SAC-left right bar) and (Eagle movie), to enable direct comparison in same cells between block and montage. Maximum total trials which we can get would now be 24 instead of 27.
   
8. Feb 9 2024 - Minor modification from the 2nd Feb version. The montage is now changed to have types of bars of light and 7 variations of the movies (6 types of eagle movie and 1 squirrel movie from earlier comes back, as a comparison). The bars and movies are alternating. This montage is padded on either side with 2 blocks of stimuli, one block of SAC bar, one block of Eagle. The files for this version can be found at -
  https://drive.google.com/drive/folders/1KttRnoJVMc0YFBxXGMaQ49XzOmQx60zH?usp=sharing

9. Feb 13 2024 - Compared to #8 above, this is a minor modification because the earlier Montage file was too large. Now we have overall the same idea of a mixture of Montage and blocks, but the Eagle movie in the blocks is 10sec, fast version. In the montage, all Variants of the eagle movie only repeat 1 time, whereas the 10sec Fast Eagle movie, and 8 different types of bars of light, all repeat 2 times. N_Repeats should be 16 for correct run time of around 2h 12min. The Montage file is updated, and can be found at -
    https://drive.google.com/file/d/1X-SawMHG1LnZiDAOPClSkgJYybYOIarD/view?usp=sharing

        
