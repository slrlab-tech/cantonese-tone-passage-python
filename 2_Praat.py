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
# failWav = checkFolder(cwd, 'failWav')

trip = os.path.join(matDir, "trip.txt")
canDict = os.path.join(matDir, "cantonese_pronunciation.dict")
canZip = os.path.join(matDir, "cantonese_model.zip")

toneCSVDir = checkFolder(rootDir, 'ToneCSV')
praatPre = os.path.join(matDir, "Praat.exe")
tonePraat = os.path.join(matDir, "measuretones_colab.praat")

import getopt
options = "gt:"
long_options = ["Gender=", "textGrid="]

if __name__ == "__main__":

    arguments, values = getopt.getopt(sys.argv[1:], options, long_options)

    if len(arguments) >= 1:
        for k, v in arguments:
            if k in ("-g", "--Gender"):
                if v == 'M':
                    minP, maxP = 50, 500
                elif v == 'F':
                    minP, maxP = 100, 600

            if k in ("-t", "--textGrid"):
                from pathlib import Path
                path = Path(rootDir)
                overrideFolder = os.path.join(path.parent.absolute(), v)
                print(f"{overrideFolder=}")
            
                for root, dirs, files in os.walk(overrideFolder, topdown=False):
                    for name in files:
                        if '.TextGrid' in name:
                            fNames.append(name)
                print(f"override {len(fNames)} textGrid")


    if len(arguments) >= 1:
        for root, dirs, files in os.walk(outputFolder, topdown=False):
            for name in files:
                if '.TextGrid' in name and arguments[0][1] in name:
                    if name not in fNames:
                        fNames.append(name)

        start = time.time()
        Parallel(n_jobs=-1)(delayed(runPraat)(f) for f in fNames)
        end = time.time()
        print(end - start)
