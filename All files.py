
# imports
import os.path
import tkinter.filedialog as filedialog
import glob
import pandas as pd

# prompts user to input framerate
framerate = int(input('Enter the framerate of the video recordings (the DeepEthogram GUI tells you this)'))

# prompts user to manually input behaviors exactly as they appear in their deepethogram output CSVs
behaviors = ['background']
behavior_number = int(input('Enter the number of behaviors not including background,'
                            ' exactly as they appear on the output csv'))
for i in range(0, behavior_number):
    print('Behavior {}:'.format(i+1))
    added_behavior = input()
    behaviors.append(added_behavior)
print('Your behaviors being analyzed are: \n',behaviors)

# prompts user to point to data folder
print('Please select folder containing all output csv files from DeepEthogram')

file_path = filedialog.askdirectory()
pattern = os.path.join(file_path, '*.csv')
files = glob.glob(pattern)

# prompts user to point to save/output folder
print('Please select the folder you want your tabulated files saved in')

save_path = save_path = filedialog.askdirectory()

# creates dataframe for file names
filename = pd.DataFrame(columns=['Filename'])
filename['Filename'] = pd.Series([file for file in files]).reset_index(drop=True)

# creates dataframes from output CSVs and runs behavioral functions on dataframes 
dfs = []
for index, file in enumerate(files):
    df = pd.read_csv(file, sep=',', index_col=[0])

    totalvideoframes = df.shape[0]
    firstindex = (df >= 1).idxmax()
    maxindex = df.shape[0] - 1

    df.loc['total_frames'] = df.sum(numeric_only=True, axis=0)
    df.loc['behavior_duration(sec)'] = df.xs('total_frames', axis=0) / framerate
    df.loc['percent_behavior'] = (df.xs('total_frames') / totalvideoframes) * 100
    df.loc['behavior_frequency'] = df.diff().eq(1).cumsum().max()
    df.loc['latency_to_first(sec)'] = firstindex / framerate

    behframesum = df.xs('total_frames').sum()
    df.loc['percent_double-labelled'] = "-"
    df.iloc[-1, 0] = (behframesum / maxindex) - 1

    print(df)

    dfs.append(df)

# joins all dataframes and creates new ones by function variable, adds filenames
dfs = pd.concat(dfs)

total_frames = dfs[dfs.index == 'total_frames'][behaviors]
total_frames_indexed = filename.join(total_frames.set_index(filename.index))

behavior_durations = dfs[dfs.index == 'behavior_duration(sec)'][behaviors]
behavior_durations_indexed = filename.join(behavior_durations.set_index(filename.index))

percent_behavior = dfs[dfs.index == 'percent_behavior'][behaviors]
percent_behavior_indexed = filename.join(percent_behavior.set_index(filename.index))

behavior_frequency = dfs[dfs.index == 'behavior_frequency'][behaviors]
behavior_frequency_indexed = filename.join(behavior_frequency.set_index(filename.index))

latency_to_first = dfs[dfs.index == 'latency_to_first(sec)'][behaviors]
latency_to_first_indexed = filename.join(latency_to_first.set_index(filename.index))

double_labelling = dfs[dfs.index == 'percent_double-labelled'][behaviors]
double_labelling_indexed = filename.join(double_labelling.set_index(filename.index))

print(total_frames_indexed)
print(behavior_durations_indexed)
print(percent_behavior_indexed)
print(behavior_frequency_indexed)
print(latency_to_first_indexed)
print(double_labelling_indexed)

# saves to csv
total_frames_indexed.to_csv(save_path + '/total_frames.csv')
behavior_durations_indexed.to_csv(save_path + '/ehavior_durations.csv')
percent_behavior_indexed.to_csv(save_path + '/percent_behavior.csv')
behavior_frequency_indexed.to_csv(save_path + '/behavior_frequency.csv')
latency_to_first_indexed.to_csv(save_path + '/latency_to_first.csv')
double_labelling_indexed.to_csv(save_path + '/percent_double_labelled.csv')
