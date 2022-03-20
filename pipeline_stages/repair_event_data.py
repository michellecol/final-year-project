import os
import numpy as np
import pandas as pd
import mne
from pipeline_stages.globals import *
mne.set_log_level('CRITICAL')

# for subject in subjects:
#     for trial in trials:
#         for task in tasks:
#             # Read in files.
#             file_name = "{}_{}_{}_(cleaned).bdf".format(subject, trial, task)
#             file_loc = os.path.join(folder_loc, str(subject), file_name)
#             raw = mne.io.read_raw_bdf(file_loc, preload=True)

            # Find and process events.
def repair_event_data(subject, trial, task, raw):
    event_file_name = "{}_{}_{}_(Corrected).evt".format(subject, trial, task)
    event_file_loc = os.path.join(folder_loc, str(subject), event_file_name)
    events_as_df = pd.read_csv(event_file_loc, delimiter="\t", index_col = False)
    
    rows_to_drop = []
    for row_index in range(len(events_as_df)):
        # If trigger number is 41, or unexpectedly long (i.e a date string),
        # or time data is recorded incorrectly (negative time)
        # drop this row
        if str(events_as_df.loc[row_index, "TriNo"]) == "41" or \
            len(str(events_as_df.loc[row_index, "TriNo"])) > 5 or \
            int(events_as_df.loc[row_index, 'Tmu         ']) < 0:
            rows_to_drop.append(row_index)

            
    events_as_df = events_as_df.drop(events_as_df.columns[3], axis=1).drop(rows_to_drop)
    events_as_df = events_as_df[events_as_df['TriNo'] != '-']
    events_as_df['TriNo'] = pd.to_numeric(events_as_df['TriNo'])
    events_as_df['Code'] = events_as_df['Code'].fillna(0)
    events_as_df['Tmu         '] = events_as_df['Tmu         '] / 1953.003030082584
    events_as_df = events_as_df.loc[:, ~events_as_df.columns.str.contains("^Unnamed")]

    event_file_name = "{}_{}_{}.eve".format(subject, trial, task)
    event_file_loc = os.path.join(folder_loc, str(subject), event_file_name)
    np.savetxt(event_file_loc, events_as_df.values.astype(int), delimiter='\t')

    events = mne.read_events(event_file_loc)
    for x in range(len(events)):
        if events[x][2] > 1 and events[x][2] < 10:
            events[x][2] -= 2
    raw.add_events(events, stim_channel='Status', replace=True)
    return raw


