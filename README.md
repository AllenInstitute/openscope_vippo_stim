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