import pandas as pd

df = pd.read_csv(f'/Users/user/Desktop/folder/filename.csv', sep=',', index_col=[0]) # include path to output csv files

framerate = 30  # edit this number if your videos have a different framerate
totalvideoframes = df.shape[0]
firstindex = (df >= 1).idxmax()
maxindex = df.shape[0] - 1

df.loc['total_frames'] = df.sum(numeric_only=True, axis=0)
df.loc['behavior_duration(sec)'] = df.xs('total_frames', axis=0) / framerate
df.loc['percent_behavior'] = (df.xs('total_frames') / totalvideoframes) * 100
df.loc['behavior_frequency']=df.diff().eq(1).cumsum().max()
df.loc['latency_to first(sec)'] = firstindex / framerate

behframesum = df.xs('total_frames').sum()
df.loc['percent_double-labelled'] = (behframesum / maxindex) - 1

print(df)
df.to_csv('/Users/user/Desktop/folder/name.csv') # input save location and file name here
