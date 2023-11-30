from ffPath import *

def RTone(i, csvF):
    c = os.path.basename(csvF)
    t = c.split(".")[0]
    p = csvF.replace('ToneCSV', 'Plot').replace('csv', 'png')
    # print(csvF, p)

    if overrideFolder != "":
        old_t = os.path.join(tonePlotDir, f"{t}.png")
        Plot_old = p.replace("Plot", "Plot_old")
        shutil.copy(old_t, Plot_old)
    df = pd.read_csv(csvF, sep=r',', skipinitialspace=True, encoding='unicode_escape')
    if 'prevTone' not in df:
        import codecs
        from io import StringIO
        x = codecs.open(csvF, "r", "utf-16").read()
        df = pd.read_csv(StringIO(x), sep=r',', skipinitialspace=True)

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
    
    plt.close()

    if len(toneCSVs) <=20:
        plts.append(plt)


options = "t:"
long_options = ["textGrid="]


if __name__ == "__main__":

    arguments, values = getopt.getopt(sys.argv[1:], options, long_options)

    if len(arguments) >= 1:
        for k, v in arguments:
            if k in ("-t", "--textGrid"):
                path = Path(rootDir)
                overrideFolder = os.path.join(path.parent.absolute(), v)
                toneCSVDir = os.path.join(overrideFolder, "ToneCSV")
                checkFolder(overrideFolder, 'Plot')
                checkFolder(overrideFolder, 'Plot_old')
    
    for root, dirs, files in os.walk(toneCSVDir, topdown=False):
        for name in files:
            if '.csv' in name:
                toneCSVs.append(os.path.join(root, name))
    
    
    Parallel(n_jobs=-1)(delayed(RTone)(i, toneCSVs[i]) for i in tqdm(range(len(toneCSVs))))

    if len(toneCSVs) <=20:
        for pltx in plts:
            pltx.show(block = False)
            