# rename
# preprocess
# repair
# process
# epoch
from pipeline_stages.event_data_processing import event_data_processing
from pipeline_stages.globals import *
import mne
import os

from pipeline_stages.preprocessing import *
from pipeline_stages.repair_event_data import *

for subject in subjects:
        for trial in trials:
            for task in tasks:
                print("Now pipelining subject: " + subject + ", trial: " + trial + ", task: " + task)
                file_name = "{}_{}_{}.bdf".format(subject, trial, task)
                file_loc = os.path.join(folder_loc, subject, file_name)
                raw = mne.io.read_raw_bdf(file_loc, preload=True)
                raw = preprocessing(raw)
                if subject in to_be_repaired:
                    try:
                        raw = repair_event_data(subject, trial, task, raw)
                    except FileNotFoundError as e:
                        print(e)

                raw = event_data_processing(raw, task)
                 