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
   5. A new set of clips, based on 2 pilot mice #072 and 077. 2 new types of stimuli were added, coherent dot motion, and scrambled bar of light. The 5 earlier movie clips were replaced by only 2 clips but of 20seconds each, compared to 4 seconds earlier. The ordering of stimuli was changed on 11/9 such that there are effectively 2 blocks, and the order if stimuli is reversed in the second block. The data folder containing these latest .npy files should be downloaded from
      https://drive.google.com/file/d/1CYJjxVQ2mn0RfuqADjBIRASNc2m1QRvM/view?usp=drive_link
      
   
        
