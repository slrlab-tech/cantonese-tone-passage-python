
import shutil
import os
import sys

import pandas as pd
# import statistics
# import numpy as np
# from matplotlib import pylab as plt
# import seaborn as sns

def checkFolder(p, f):
    Dir = os.path.join(p, f)
    if not os.path.isdir(Dir):
        os.mkdir(Dir)
    return Dir

def UploadAction(wavs):
    fNames, fpaths, plts = [], [], []

    failDict, failloc = {}, {}
    for i, f in enumerate(wavs):
        fName = os.path.split(f)[-1]
        failDict[fName.split(".")[0]] = False
        failloc[fName.split(".")[0]] = f

        for root, dirs, files in os.walk(outputFolder, topdown=False):
            for name in files:
                if '.TextGrid' in name:
                    failDict[name.split(".")[0]] = True
                    
        df = pd.DataFrame([failDict]).T
        df.to_csv("mfa_fail.csv")

    for k, v in failDict.items():
        if v == False:
            des = os.path.join(failWav, os.path.basename(failloc[k]))
            shutil.copy(failloc[k], des)
        
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
        folder = os.path.join(cwd, arg[1])
        if os.path.exists(folder):
            for root, dirs, files in os.walk(folder, topdown=False):
                for name in files:
                    wavs.append(os.path.join(root, name))
                    # print(name)
        UploadAction(wavs)
