import sys, os
from pathlib import Path

import pandas as pd
import statistics
import numpy as np
from matplotlib import pylab as plt
import seaborn as sns

import getopt

from joblib import Parallel, delayed
import time
from tqdm import tqdm


def checkFolder(p, f):
    Dir = os.path.join(p, f)
    if not os.path.isdir(Dir):
        os.mkdir(Dir)
    return Dir

cwd = os.getcwd()
print(f'{cwd=}')
rootDir = checkFolder(cwd, 'ToneAnalysis')
inputFolder = checkFolder(rootDir, 'inputFolder')
outputFolder = checkFolder(rootDir, 'outputFolder')
tempFolder = checkFolder(rootDir, 'tempFolder')
tonePlotDir = os.path.join(rootDir, 'Plot')
overrideFolder = ""

matDir = checkFolder(cwd, 'materials')
failWav = checkFolder(cwd, 'failWav')

trip = os.path.join(matDir, "trip.txt")
canDict = os.path.join(matDir, "cantonese_pronunciation.dict")
canZip = os.path.join(matDir, "cantonese_model.zip")

toneCSVDir = checkFolder(rootDir, 'ToneCSV')
praatPre = os.path.join(matDir, "Praat.exe")
tonePraat = os.path.join(matDir, "measuretones_colab.praat")
narrowBeam = os.path.join(matDir, "narrowBeam.yaml")

failDict, fDict = {}, {}
fNames, fpaths, toneCSVs, plts, wavs = [], [], [], [], []
