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

    failDict = {}
    for f in wavs:
        fName = os.path.split(f)[-1]
        fpath = os.path.join(tempFolder, fName.split('.')[0])
        failDict[fName.split('.')[0]] = False

        fNames.append(fName)
        fpaths.append(fpath)

        if not os.path.isdir(fpath):
            os.mkdir(fpath)
        txtF = os.path.join(fpath, f'{fName.split(".")[0]}.txt')
        if not os.path.isfile(txtF):
            shutil.copy(f, fpath)
            shutil.copy(trip, fpath)
            os.rename(os.path.join(fpath, 'trip.txt'), os.path.join(
                fpath, f'{fName.split(".")[0]}.txt'))
        
    try:
        # os.system(f"{condaBat} activate aligner")
        os.system(
            f"mfa align {tempFolder} {canDict} {canZip} {outputFolder} -j8 --clean")
        def mvRename(p):
            newP = p.replace('tempFolder', 'inputFolder')
            shutil.move(p,newP)
            return newP
        fpaths = [mvRename(p) for p in fpaths]
        # shutil.rmtree(tempFolder)

        # print("fnames is", fNames)
        
        failDict = check_failDict(failDict)

        # print("fpaths is", fpaths)

    except Exception as ex:
        print(ex)

    finally:
        for k, v in failDict.items():
            if v == False:
                failloc = os.path.join(inputFolder, k)
                f_des = os.path.join(failWav, k)
                print(failloc)
                print(f_des)
                shutil.move(failloc, f_des)

        try:
            os.system(
                f"mfa align {failWav} {canDict} {canZip} {outputFolder} -j8 --clean --config_path {narrowBeam}")
        except Exception as ex:
            print(ex)

        finally:
            failDict = check_failDict(failDict)
                 
            for k, v in failDict.items():
                if v == True:
                    f_des = os.path.join(failWav, k)
                    failloc = os.path.join(inputFolder, k)
                    shutil.move(f_des, failloc)

            df = pd.DataFrame([failDict]).T
            df.to_csv("mfa_fail.csv")

def check_failDict(failDict):
    for root, dirs, files in os.walk(outputFolder, topdown=False):
        for name in files:
            if '.TextGrid' in name:
                failDict[name.split(".")[0]] = True
    return failDict

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
narrowBeam = os.path.join(matDir, "narrowBeam.yaml")


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
