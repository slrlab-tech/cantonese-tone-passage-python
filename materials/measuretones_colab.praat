# form Enter your speaker info and pitch settings
#   comment Enter speaker and episode information:
#   sentence File_name Test

#   comment Set pitch range:
#   natural Pitch_min 75
#   natural Pitch_max 500

#   comment Adjust advanced pitch settings if necessary:
#   positive Silence_threshold 0.03
#   positive Voicing_threshold 0.45
#   positive Octave_cost 0.01
#   positive Octave_jump_cost 0.35
#   positive Voiced_cost 0.14

#   comment Number of points to measure during tone (don't change):
#   natural Measurement_points 20 (= Every 5%)

#   comment Check box if TextGrid is not in format: 1. Word, 2. Phoneme
#   boolean Select_TG_tiers 0
#  endform


form Test command line calls
    sentence WavFile /content/cantonese-tone-passage/sample/Northwind_Sun.wav
    sentence TgFile /content/cantonese-tone-passage/output/Northwind_Sun.TextGrid
    sentence File_name = Northwind_Sun
    natural Pitch_min 75
    natural Pitch_max 500
endform

if wavFile$ = ""
  wavFile$ = "/content/cantonese-tone-passage/sample/Northwind_Sun.wav"
endif
if tgFile$ = ""
  tgFile$ = "/content/cantonese-tone-passage/output/Northwind_Sun.TextGrid"
endif
if file_name$ = ""
  file_name$ ="Northwind_Sun"
endif

# appendInfoLine: wavFile$, tgFile$, file_name$, pitch_min, pitch_max

silence_threshold = 0.03
voicing_threshold = 0.45
octave_cost = 0.01
octave_jump_cost = 0.35
voiced_cost = 0.14

measurement_points = 20

file_name_nospaces$ = replace$(file_name$, " ", "", 0)
output_file$ = file_name_nospaces$ + ".csv"
writeFile: output_file$

# if select_TG_tiers == 1
#   beginPause: "Select TextGrid Tiers"
#     # positive: "phrase_tier", 1
#     positive: "word_tier", 1
#     positive: "phon_tier", 2
#     # positive: "point_tier", 4
#   endPause: "Cancel", "OK", 2, 1
# else
  # phrase_tier = 1
  word_tier = 1
  phon_tier = 2
  # point_tier = 4
# endif

# Get the name of the files
# wavFile$ = chooseReadFile$: "Open your sound file"
if wavFile$ <> ""
    wav = Open long sound file: wavFile$
endif

# tgFile$ = chooseReadFile$: "Open your TextGrid file"
if tgFile$ <> ""
    tg = Read from file: tgFile$
endif

# # Get number of segments from TextGrid
selectObject: tg
nInt = Get number of intervals: phon_tier

token_number = 0
# clearinfo

appendFile: output_file$, "token_number,wordLabel,vowelLabel,toneNumber,toneStart,toneDuration," 
for t from 0 to measurement_points
  appendFile: output_file$, "F0-", t * 100/measurement_points, ","
endfor
appendFile: output_file$, "F1,F2,F3,"
appendFile: output_file$, "syllType,onset,coda,prevTone,nextTone", newline$

for x to nInt
  selectObject: tg
  # Get segment labels for each interval
  segLabel$ = Get label of interval: phon_tier, x

  # Check if the label contains a number 1-6. If so, it's a Cantonese vowel
  if index_regex (segLabel$, "[1-6]") <> 0

    # Remove tone number from vowel label
    vowelLabel$ = replace_regex$ (segLabel$, "[0-6]", "", 1)

    # Get tone number by removing alpha chars
    toneNumber$ = replace_regex$ (segLabel$, "[A-z]", "", 0)

    # Increase token counter
    token_number = token_number + 1

    # Get start and end times of word on tier 2
    vowelStart = Get start time of interval: phon_tier, x
    vowelEnd = Get end time of interval: phon_tier, x

    # Get number of breath group and starting time
    # phraseInt = Get interval at time: phrase_tier, vowelStart + 0.01
    # phraseStart = Get start time of interval: phrase_tier, phraseInt

    # Get start and end times of word on tier 1
    wordInt = Get interval at time: word_tier, vowelStart + 0.01
    wordLabel$ = Get label of interval: word_tier, wordInt

    wordStart = Get start time of interval: word_tier, wordInt
    wordEnd = Get end time of interval: word_tier, wordInt
	if wordInt <= 1
		wordInt = 2
	endif
    # Get tone numbers for previous and following words; will print as "T" if word has no tone number
    prevWordLabel$ = Get label of interval: word_tier, wordInt - 1
    prevTone$ = replace_regex$ (prevWordLabel$, "[a-zA-Z:punct:]", "", 0)
    nextWordLabel$ = Get label of interval: word_tier, wordInt + 1
    nextTone$ = replace_regex$ (nextWordLabel$, "[a-zA-Z:punct:]", "", 0)

    # Check whether preceding and following intervals are in the same word
    # If so, get labels for onset and coda
    precSeg = Get end time of interval: phon_tier, x - 1
    precSegWord = Get interval at time: word_tier, precSeg - 0.01
    if precSegWord == wordInt
      onset$ = Get label of interval: phon_tier, x - 1
    else
      onset$ = ""
    endif

    nextSeg = Get start time of interval: phon_tier, x + 1
    nextSegWord = Get interval at time: word_tier, nextSeg + 0.01
    if nextSegWord == wordInt
      coda$ = Get label of interval: phon_tier, x + 1
      syllType$ = "closed"
    else
      coda$ = ""
      syllType$ = "open"
    endif

    # Include onset in tone measurement if the onset is voiced
    if onset$ == "m" or onset$ == "n" or onset$ == "ng" or onset$ == "w" or onset$ == "l" or onset$ == "j"
      toneStart = wordStart
    else
      toneStart = vowelStart
    endif

    # Don't include voiceless codas in tone measurement
    if coda$ == "p" or coda$ == "t" or coda$ == "k"
      toneEnd = vowelEnd
    else
      toneEnd = wordEnd
    endif

    # Calculate duration of voiced portion of syllable
    toneDuration = toneEnd - toneStart
    # Calculate X% of toneDuration based on number of points
    toneInterval = toneDuration / measurement_points

    vowelDuration = vowelEnd - vowelStart
    vowelMidpoint = (vowelEnd + vowelStart)/2

    # Calculate distance from start of utterance
    # utterancePos = toneStart - phraseStart
    
    # if x/nInt > 0.2475
    #   if x/nInt < 0.2525
    #     appendInfo: " ###---25---### "
    #   endif
    # endif
    # if x/nInt > 0.4975
    #   if x/nInt < 0.5025
    #     appendInfo: " ###---50---### "
    #   endif
    # endif
    # if x/nInt > 0.7475
    #   if x/nInt < 0.7525
    #     appendInfo: " ###---75---### "
    #   endif
    # endif

    # Only measure tones longer than 100 ms
    if toneDuration > 0.1

      # Print current token + vowel for reference
      # appendInfoLine: token_number, tab$, wordLabel$

      # Start printing metadata
      appendFile: output_file$, token_number, ","
      appendFile: output_file$, wordLabel$, ",", vowelLabel$, ",", "T", toneNumber$, ","
      appendFile: output_file$, toneStart, ",", toneDuration, ","

      # Get F0 measurements
      selectObject: wav

      wavchunk = Extract part: wordStart, wordEnd, "yes"
      pitch = To Pitch (ac): 0, pitch_min, 15, "no", silence_threshold, voicing_threshold, octave_cost, octave_jump_cost, voiced_cost, pitch_max

      for t from 0 to measurement_points
      	# Get times for start (0%), 10%, 20%, etc. to 100%
      	msmtTime = toneStart + (t * toneInterval)

      	# Select Pitch object and measure it at the time we want
      	selectObject: pitch
      	f0 = Get value at time: msmtTime, "Hertz", "Linear"
      	appendFile: output_file$, f0, ","
      endfor

      removeObject: pitch
      removeObject: wavchunk
      
      # Get F1, F2, F3 measurements
      selectObject: wav
      wavchunk = Extract part: vowelStart, vowelEnd, "yes"
      formant = To Formant (burg)... 0 5 5000 0.025 50

      selectObject: formant
      f1 = Get value at time... 1 vowelMidpoint Hertz Linear
      f2 = Get value at time... 2 vowelMidpoint Hertz Linear
      f3 = Get value at time... 3 vowelMidpoint Hertz Linear
      appendFile: output_file$, f1, ",", f2, ",", f3, ","

      removeObject: formant
      removeObject: wavchunk


      # write other infos
      appendFile: output_file$, syllType$, ",", onset$, ",", coda$, ","
      appendFile: output_file$, "T", prevTone$, ",", "T", nextTone$

      appendFile: output_file$, newline$

    endif

  endif
    
endfor

removeObject: tg
removeObject: wav

# appendInfoLine: "Finished!"
