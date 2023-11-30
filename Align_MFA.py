import shutil, os
import sys

import pandas as pd
import numpy as np
# import statistics
# from matplotlib import pylab as plt
# import seaborn as sns

from ffPath import *


failDict = {}
fNames, fpaths, wavs = [], [], []


def construct_input(wavs):
    global fNames, fpaths, failDict
    for f in wavs:
        fName_ext = os.path.split(f)[-1]
        fName = fName_ext.split(".")[0]

        fpath = os.path.join(tempFolder, fName)
        failDict[fName.split('.')[0]] = False

        fNames.append(fName)
        fpaths.append(fpath)

        if not os.path.isdir(fpath):
            os.mkdir(fpath)
        txtF = os.path.join(fpath, f'{fName}.txt')
        if not os.path.isfile(txtF):
            shutil.copy(f, fpath)
            shutil.copy(trip, fpath)
            os.rename(os.path.join(fpath, 'trip.txt'), os.path.join(fpath, f'{fName}.txt'))
            
def MFA_Align(inputF, default_conf=True):
    global fNames, fpaths, failDict
    cmd_str = f"mfa align {inputF} {canDict} {canZip} {outputFolder} -j8 --clean"
    if not default_conf:
        cmd_str += f" --config_path {narrowBeam}"
    try:
        os.system(cmd_str)
    except Exception as e1:
        print(f"MFA exceptions {default_conf=}:\n{e1}")

    if default_conf:
        fpaths = [mvRename(p) for p in fpaths]
    failDict = check_failDict(failDict)

    try:
        mvFailDict(failDict, inputFolder, failWav, default_conf)
    except Exception as e2:
        print(f"mvFailDict {default_conf=}:\n{e2}")

def mvRename(p):
    newP = p.replace(tempFolder, inputFolder)
    if os.path.exists(p):
        shutil.move(p,newP)
    else:
        print(f"Not exist: {p}")
    return newP

def check_failDict(failDict):
    for root, dirs, files in os.walk(outputFolder, topdown=False):
        for name in files:
            if '.TextGrid' in name:
                failDict[name.split(".")[0]] = True
    return failDict

def mvFailDict(failDict, inputFolder, failWav, default_conf):
    for k, v in failDict.items():
        failloc = os.path.join(inputFolder, k)
        f_des = os.path.join(failWav, k)
        
        if default_conf and v == False:
            shutil.move(failloc, f_des)
        if not default_conf and v == True and os.path.exists(f_des):
            shutil.move(f_des, failloc)

    df = pd.DataFrame([failDict]).T
    df.to_csv("mfa_fail.csv")
    
if __name__ == "__main__":
    arg = sys.argv
    if len(arg) > 1:
        folder = os.path.join(cwd, arg[1])
        if os.path.exists(folder):
            for root, dirs, files in os.walk(folder, topdown=False):
                for name in files:
                    wavs.append(os.path.join(root, name))
                    # print(name)

        construct_input(wavs)
        MFA_Align(tempFolder)
        
        textGrid_TF = {True: 0, False: 0}
        for tf in [v for k, v in failDict.items()]:
            textGrid_TF[tf] += 1
        print(f"{textGrid_TF=}")

        # Retry failed wav with narrow beam
        if textGrid_TF[False] > 0:
            MFA_Align(failWav, default_conf=False)
            
    for f in [failWav, tempFolder]:
        if len(os.listdir(f)) == 0:
            shutil.rmtree(f)