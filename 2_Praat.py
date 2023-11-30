from ffPath import *

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
    
    if overrideFolder != "":
        outputTG = os.path.join(overrideFolder, f)

    # print(f, os.path.exists(inputWav), os.path.exists(outputTG))

    toneCSV = os.path.join(toneCSVDir, f.split(".")[0])
    toneCSVs.append(toneCSV)
    # print(f'{inputWav=}, {outputTG=}, {toneCSV=}')

    PitchMin, PitchMax = minP, maxP
    os.system(
        f'"{praatPre}" --run {tonePraat} {inputWav} {outputTG} {toneCSV} {PitchMin} {PitchMax}')
        
options = "g:t:"
long_options = ["Gender=", "textGrid="]

def find_textgrid(folder, kw=''):
    fNames = []
    for root, dirs, files in os.walk(folder, topdown=False):
        for name in files:
            
            cond = True
            if kw != '':
                cond = kw in name

            if '.TextGrid' in name and cond:
                if name not in fNames:
                    fNames.append(name)
    return fNames


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
                path = Path(rootDir)
                overrideFolder = os.path.join(path.parent.absolute(), v)
                print(f"{overrideFolder=}")
            
                fNames = find_textgrid(overrideFolder, kw=arguments[0][1])
                print(f"override {len(fNames)} textGrid")
    # override_only = any(["-o" in k for k, v in arguments])

    if overrideFolder != "":
        toneCSVDir = checkFolder(overrideFolder, 'ToneCSV')
    else:
        toneCSVDir = checkFolder(rootDir, 'ToneCSV')

    if len(arguments) >= 1:
        if overrideFolder == "":
            fNames = find_textgrid(outputFolder, kw=arguments[0][1]) + fNames
        print(f"Total TextGrid = {len(fNames)}")
        print(fNames)

        start = time.time()
        Parallel(n_jobs=-1)(delayed(runPraat)(fNames[i]) for i in tqdm(range(len(fNames))))
        end = time.time()
        print(end - start)
