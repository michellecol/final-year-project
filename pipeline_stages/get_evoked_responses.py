import os
import numpy as np
import mne
mne.set_log_level('CRITICAL')

# The following variables should contain the location of the EEG files, 
# as well as the subjects, and trials that you wish to get evoked responses for.
folder_loc = ""
subjects = []
trials = []

#The task for evoked responses to be estimated for, as well as the appropriate window should be provided.
task = ""
window = []

for subject in subjects:
    for trial in trials:
        file_name = "{}-{} {} (cleaned).fif".format(subject, trial, task)
        file_loc = os.path.join(folder_loc, subject, file_name)
        raw = mne.io.read_raw_fif(file_loc, preload=True)
        events = mne.find_events(raw, stim_channel='Status')
        # If downsampling frequency is changed decim will need to change alse.
        # Decim is the integer result of dividing original frequency by downsampled frequency.
        epochs = mne.Epochs(raw, events, event_id=event_dict, tmin=window[0], tmax=window[1], 
                            preload=True, on_missing='ignore', decim=4)

        event_dict = {'studied pair': 1, 
              'false/congruent/correct': 12, 'false/congruent/incorrect': 13,
              'false/incongruent/correct': 14, 'false/incongruent/incorrect': 15,
              'true/congruent/correct': 16, 'true/congruent/incorrect': 17,
              'true/incongruent/correct': 18, 'true/incongruent/incorrect': 19}

        for item in event_dict:
            item_epochs = epochs[item]
            evoked_response = item_epochs.average()
            export_name = "{}-{} {} {}.csv".format(subject, trial, task, '_'.join(item.split('/')))
            export_loc = os.path.join(folder_loc, str(subject), export_name)
            evoked_response.to_data_frame().to_csv(export_loc)