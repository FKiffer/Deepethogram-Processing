# Deepethogram-Processing
Simple scripts to quickly process the output files from deepethogram with the most common behavioral measures: total frames containing behavior, total time per behavior, percent behavior per trial, frequency of behavior, latency to first instance of behavior and percent double labelled frames for a quick, trial-based accuracy metric.

One File at a Time.py is to be used.. you guessed it, on a single file at a time. This appends all behavioral measures to the bottom of the output csv and saves a new file.

All files.py is to be used in a folder conatining all output csv files. It wrangles output csv files, generates a new dataframe for each type of behavioral measure per csv and wrangles and tabulates data on a behavioral metric basis, saving a new csv for each measure with trials/filename indexed. 
When ran, this prompts the user to:
1. Input framerate of video recordings (make sure this is consistent)
2. Input the number of behaviors deepethogram predicted
3. Write down said behaviors exactly and in the same order as they appear on output files
4. Point to the folder containing all output (prediction/inference) csv files considered for analyses
5. Point to the folder you wish the new tabulated csv files to be saved in 
It's a good idea to create an empty folder to save the new output csv files in. Alternatively, the user can copy and paste values from the command prompt as they wish.

Validated in python 3.9 🐍
