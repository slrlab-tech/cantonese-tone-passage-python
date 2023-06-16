# import shutil
import os
import sys

# import pandas as pd
# import statistics
# import numpy as np
# from matplotlib import pylab as plt
# import seaborn as sns
from joblib import Parallel, delayed

import time

def checkFolder(p, f):
    Dir = os.path.join(p, f)
    if not os.path.isdir(Dir):
        os.mkdir(Dir)
    return Dir

def runPraat(f):
    # f = fNames[i]
    outputTG = os.path.join(outputFolder, f.split(".")[0], f)
    inputWav = outputTG.replace(
        'outputFolder', 'inputFolder').replace('TextGrid', 'wav')
    
    print(name, os.path.exists(inputWav), os.path.exists(outputTG))

    toneCSV = os.path.join(toneCSVDir, f.split(".")[0])
    toneCSVs.append(toneCSV)
    # print(f'{inputWav=}, {outputTG=}, {toneCSV=}')

    PitchMin, PitchMax = minP, maxP
    os.system(
        f'"{praatPre}" --run {tonePraat} {inputWav} {outputTG} {toneCSV} {PitchMin} {PitchMax}')
        
cwd = os.getcwd()
fNames, fpaths, toneCSVs, plts, wavs = [], [], [], [], []

print(f'{cwd=}')
rootDir = checkFolder(cwd, 'ToneAnalysis')
inputFolder = checkFolder(rootDir, 'inputFolder')
outputFolder = checkFolder(rootDir, 'outputFolder')
tempFolder = checkFolder(rootDir, 'tempFolder')
tonePlotDir = os.path.join(rootDir, 'Plot')

matDir = checkFolder(cwd, 'materials')
failWav = checkFolder(cwd, 'failWav')

trip = os.path.join(matDir, "trip.txt")
canDict = os.path.join(matDir, "cantonese_pronunciation.dict")
canZip = os.path.join(matDir, "cantonese_model.zip")

toneCSVDir = checkFolder(rootDir, 'ToneCSV')
praatPre = os.path.join(matDir, "Praat.exe")
tonePraat = os.path.join(matDir, "measuretones_colab.praat")


if __name__ == "__main__":

    arg = sys.argv
    if len(arg) > 1:
        if arg[1] == 'M':
            minP, maxP = 50, 500
        elif arg[1] == 'F':
            minP, maxP = 100, 600

        for root, dirs, files in os.walk(outputFolder, topdown=False):
            for name in files:
                if '.TextGrid' in name and arg[1] in name:
                    fNames.append(name)

        start = time.time()
        Parallel(n_jobs=-1)(delayed(runPraat)(f) for f in fNames)
        end = time.time()
        print(end - start)
