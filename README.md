# Music Classification by Genre


## Packages:
Python 3.6+, SciPy, LibROSA , Numpy, Matplotlib, seaborn, dotenv, pydot

## Installation:
```
# Install Python 3.6 or greater
$ sudo apt-get install python3.6

# Setup environment
$ ./setup_env.sh
```

## Test:
```
# Run unit tests
$ python3 -m unit_test.py
```

## Dataset:
### Brief
* The dataset for this project was taken from Free Music Archive (FMA): https://github.com/mdeff/fma
* The dataset consists of thousands of songs and excellent metadata that includes pre-computed features

### Details:
* The datset consists of 8000 songs in 8 genres taken from the following dataset: [fma_small.zip](https://os.unil.cloud.switch.ch/fma/fma_small.zip) - size is 7.2 GB
* The metadata is in csv files which contains various information about the songs such as artist, genre, and record date
* Pre-computed features are part of the metadata like MFCC, ZCR, Tonnetz, etc.
* Details about the FMA dataset can be found in the official [paper](https://arxiv.org/pdf/1612.01840.pdf)
* The dataset can be downloaded here: 
* The metadata for all tracks can be downloaded here: [fma_metadata.zip](https://os.unil.cloud.switch.ch/fma/fma_metadata.zip) - size is 342 MB


