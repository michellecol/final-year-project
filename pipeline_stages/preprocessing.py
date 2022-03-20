import os
import numpy as np
import mne
from mne.preprocessing import ICA
from pipeline_stages.globals import *
mne.set_log_level('CRITICAL')

# The following variables should contain the location of the EEG files, 
# as well as the subjects, trials, and tasks that are to be cleaned.

def set_meta_data(raw):
    raw.set_channel_types({'EXG1': 'misc','EXG2':'misc','EXG3':'misc','EXG4':'misc',
                        'EXG5':'eog','EXG6': 'eog','EXG7':'misc','EXG8':'misc'})
    try:
        raw.drop_channels(['GSR1', 'GSR2', 'Erg1', 'Erg2', 'Resp', 'Plet', 'Temp'])
    except:
        pass
    raw.set_montage('standard_1020')
# print(raw.ch_names)

def downsample(raw):
    current_sfreq = raw.info['sfreq']
    desired_sfreq = 256
    decim = np.round(current_sfreq / desired_sfreq).astype(int)
    obtained_sfreq = current_sfreq / decim
    lowpass_freq = obtained_sfreq / 3.
    raw.filter(l_freq=None, h_freq=lowpass_freq)

def remove_ocular_noise(raw):
    ica = ICA(n_components=0.95, random_state=97)
    ica.fit(raw)
    ica.exclude = []
    eog_indices, eog_scores = ica.find_bads_eog(raw)
    ica.exclude = eog_indices
    ica.apply(raw)


def preprocessing(raw):
    set_meta_data(raw)
    downsample(raw)
    raw.filter(l_freq=0.5, h_freq=None)
    raw.notch_filter(freqs=[50])
    remove_ocular_noise(raw)
    return raw


