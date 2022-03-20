import os
from pipeline_stages.globals import *

def rename_raw_data():
    
    for folder in os.listdir(folder_loc):
        #print(folder_loc + folder)
        if folder in blacklist_folders:
            continue
        for file in os.listdir(folder_loc + folder):
            subject = folder
            #print(os.path.join(folder_loc, folder, file))
            #This takes each file and assigns its trial as 1 or 2, 
            # depending on whether or not the string "Exp2b" is in the original name
            if ".bdf".lower() not in file.lower():
                continue

            if "Exp2b".lower() in file.lower():
                trial = "2"
            else:
                trial = "1"

            if "VPA".lower() in file.lower():
                task = "VPA"

            elif "Spatial".lower() in file.lower():
                task = "SG"

            elif "Visual Search".lower() in file.lower():
                task = "VS"

            elif "finger".lower() in file.lower():
                continue

            elif "eyes".lower() in file.lower():
                continue
            else:
                print("Did not find task for " + file)
                continue

            old_filename = os.path.join(folder_loc, folder, file)
            new_filename = f"D:\\{subject}\\{subject}_{trial}_{task}.bdf"
            print("Renaming " + old_filename + " to: " + new_filename )

        # os.rename(old_filename, new_filename)




