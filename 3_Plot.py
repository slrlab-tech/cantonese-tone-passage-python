# import shutil
import os
import sys

import pandas as pd
import statistics
import numpy as np
from matplotlib import pylab as plt
import seaborn as sns

def checkFolder(p, f):
    Dir = os.path.join(p, f)
    if not os.path.isdir(Dir):
        os.mkdir(Dir)
    return Dir

def RTone():
    if not os.path.isdir(tonePlotDir):
        os.mkdir(tonePlotDir)
    for i, csvF in enumerate(toneCSVs):
        c = csvF
        t = os.path.basename(csvF).split(".")[0]
        p = c.replace('ToneCSV', 'Plot').replace('csv', 'png')
        # print(c, p)

        df = pd.read_csv(c, sep=r',', skipinitialspace=True)
        df['prevTone'] = df['prevTone'].apply(
            lambda x: "pause" if x == "T" else x)
        df['nextTone'] = df['nextTone'].apply(
            lambda x: "pause" if x == "T" else x)
        df.dropna(subset=['prevTone'], inplace=True)

        df = pd.wide_to_long(
            df, ["F0"], i="token_number", j="Timepoint", sep='-')
        df.reset_index(inplace=True)
        df = df.loc[df['F0'] != '--undefined--']
        df = df.loc[df['Timepoint'] > 10]
        df = df.loc[df['Timepoint'] < 90]
        df.reset_index(level=0, drop=True, inplace=True)

        df['F0'] = df['F0'].astype('float64')
        df['meanF0'] = statistics.mean(df['F0'])
        df['medianF0'] = statistics.median(df['F0'])
        df = df.assign(F0st=lambda x: 12 *
                       np.log(x.F0 / x.meanF0) / np.log(2))

        fig = plt.figure()
        df_tone = df.groupby(['Timepoint', 'toneNumber']).agg(
            {'F0st': np.average}).unstack()
        
        x = df_tone.index.values
        for i in range(6):
            y = df_tone['F0st'][f'T{i+1}'].to_numpy()
            sns.regplot(x=x, y=y, lowess=True, scatter=False)

            # plt.plot(x, y)

        plt.title(t)
        plt.legend(loc=(1.04, 0.5), labels=[f'T{i+1}' for i in range(6)])
        plt.tight_layout()
        plt.savefig(p)

        if len(toneCSVs) <=20:
            plts.append(plt)
            
    if len(toneCSVs) <=20:
        for pltx in plts:
            pltx.show(block = False)

fDict = {}

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

if __name__ == "__main__":

    for root, dirs, files in os.walk(toneCSVDir, topdown=False):
        for name in files:
            if '.csv' in name:
                toneCSVs.append(os.path.join(root, name))
    RTone()
