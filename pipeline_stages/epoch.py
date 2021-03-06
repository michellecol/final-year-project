import os
import numpy as np
import mne
mne.set_log_level('CRITICAL')

# The following variables should contain the location of the EEG files, 
# as well as the subjects, and trials that are to have events corrected.
subjects = ["11"]
trials = ["1"]
tasks = ["VPA"]
folder_loc = f"D:\\"


for subject in subjects:
    for trial in trials:
        for task in tasks:
            file_name = "{}_{}_{}_(Cleaned).fif".format(subject, trial, task)
            file_loc = os.path.join(folder_loc, subject, file_name)
            raw = mne.io.read_raw_fif(file_loc, preload=True)
            
            events = mne.find_events(raw, stim_channel='Status')
            event_colors = {12:"purple", 14:"navy", 16:"blue", 18:"teal",
              13:"darkred", 15:"orange", 17: "deeppink", 19: "yellow", \
            65542: "grey", 128: "grey", 65537: "grey", 1: "grey" , \
             10: "green", 11: "red"}

            if task == "VS":
                picks = ["P7", "P8", "Pz"]
                epochs = mne.Epochs(raw, events, picks = picks)
                #epochs.plot(picks = picks, n_channels = 3, events = events, block = True, title = subject,event_color = event_colors)
                avg_epochs = epochs.average(picks = picks, method='mean', by_event_type=True)
               
                for evoke in avg_epochs:
                     evoke.plot(picks = picks, spatial_colors = True, show = True)

            if task == "VPA":
                picks = ["PO3", "PO4", "Pz"]
                epochs = mne.Epochs(raw, events, picks = picks)
                epochs.plot(picks = picks, n_channels = 3, events = events, block = True , title = str(subject), event_color = event_colors)
                avg_epochs = epochs.average(picks = picks, method='mean', by_event_type=True)
               
                for evoke in avg_epochs:
                     evoke.plot(picks = picks, window_title = str(subject), spatial_colors = True, show = True)

            if task == "SG":
                picks = ["PO3", "PO4", "Pz"]
                epochs = mne.Epochs(raw, events, picks = picks)
                epochs.plot(picks = picks, n_channels = 3, events = events, \
                block = True,  event_color = event_colors, title = subject)
                avg_epochs = epochs.average(picks = picks, method='mean', by_event_type=True)
               
                for evoke in avg_epochs:
                     evoke.plot(picks = picks, title = subject, spatial_colors = True, show = True)

