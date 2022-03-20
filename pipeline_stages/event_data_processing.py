import os
import mne
from pipeline_stages.globals import *
mne.set_log_level('CRITICAL')

# The following variables should contain the location of the EEG files, 
# as well as the subjects, and trials that are to have events corrected.

def relabel_VPA_events(events):
    for x in range(len(events) - 1):
        #F/C/C
        if events[x][2] == 4 and events[x+1][2] == 10:
            events[x][2] = 12
        #F/C/I
        elif events[x][2] == 4 and events[x+1][2] == 11:
            events[x][2] = 13
        #F/I/C
        elif events[x][2] == 5 and events[x+1][2] == 10:
            events[x][2] = 14
        #F/I/I
        elif events[x][2] == 5 and events[x+1][2] == 11:
            events[x][2] = 15
        #T/C/C
        elif events[x][2] == 6 and events[x+1][2] == 10:
            events[x][2] = 16
        #T/C/I
        elif events[x][2] == 6 and events[x+1][2] == 11:
            events[x][2] = 17
        #T/I/C
        elif events[x][2] == 7 and events[x+1][2] == 10:
            events[x][2] = 18
        #T/I/I
        elif events[x][2] == 7 and events[x+1][2] == 11:
            events[x][2] = 19


def relabel_VS_events(events):
    for x in range(len(events) - 1):
        #FLEFT/C
        if events[x][2] == 1 and events[x+1][2] == 10:
            events[x][2] = 12
        #FLEFT/I
        elif events[x][2] == 1 and events[x+1][2] == 11:
            events[x][2] = 13
        #LEFT/C
        elif events[x][2] == 2 and events[x+1][2] == 10:
            events[x][2] = 14
        #LEFT/I
        elif events[x][2] == 2 and events[x+1][2] == 11:
            events[x][2] = 15
        #RIGHT/C
        elif events[x][2] == 3 and events[x+1][2] == 10:
            events[x][2] = 16
        #RIGHT/I
        elif events[x][2] == 3 and events[x+1][2] == 11:
            events[x][2] = 17
        #FRIGHT/C
        elif events[x][2] == 4 and events[x+1][2] == 10:
            events[x][2] = 18
        #FRIGHT/I
        elif events[x][2] == 4 and events[x+1][2] == 11:
            events[x][2] = 19

def relabel_SG_events(events):
    for x in range(len(events) - 1):
        #NRSL/C
        if events[x][2] == 1 and events[x+1][2] == 10:
            events[x][2] = 12
        #NRSL/I
        elif events[x][2] == 1 and events[x+1][2] == 11:
            events[x][2] = 13
        #RSL/C
        elif events[x][2] == 2 or events[x][2] == 3 or events[x][2] == 4 and events[x+1][2] == 10:
            events[x][2] = 14
        #RSL/I
        elif events[x][2] == 2 or events[x][2] == 3 or events[x][2] == 4  and events[x+1][2] == 11:
            events[x][2] = 15
        #NRNL/C
        elif events[x][2] == 5 and events[x+1][2] == 10:
            events[x][2] = 16
        #NRNL/I
        elif events[x][2] == 5 and events[x+1][2] == 11:
            events[x][2] = 17
        #RNL/C
        elif events[x][2] == 6 or events[x][2] == 7 or events[x][2] == 8 and events[x+1][2] == 10:
            events[x][2] = 18
        #RNL/I
        elif events[x][2] == 6 or events[x][2] == 7 or events[x][2] == 8 and events[x+1][2] == 11:
            events[x][2] = 19
        

def event_data_processing(raw, task):
    events = mne.find_events(raw, stim_channel='Status')

    if task == "VPA":
        relabel_VPA_events(events)
    elif task == "VS":
        relabel_VS_events(events)
    elif task == "SG":
        relabel_SG_events(events)
        
    raw.add_events(events, stim_channel='Status', replace=True)
    return raw
