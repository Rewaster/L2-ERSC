import os
import shutil
import random
# number of speakers
speaker_number = 4
j = 0
i = 0
# source directory for files to copy from
source_dir = "D:\\thesis\\test\\000"
prompt_dir = "D:\\thesis\\test\\tr"

# target directory for files to copy to
target_dir = "D:\\thesis\\test\\to\\000"  
prompt_target_dir = "D:\\thesis\\test\\to\\tr" 

 # empty list for collecting files
source_files = []   
prompt_files = [] 

# walk through directory tree and find files only
for i in range(speaker_number):
    for dirpath, dirnames, filenames in os.walk(source_dir + str(i+1)):
        for file in filenames:
            if file.endswith(".wav"):
                source_files.append(os.path.join(dirpath, file))

for dirpath, dirnames, filenames in os.walk(prompt_dir):
    for file in filenames:
        if file.endswith(".txt"):
            prompt_files.append(os.path.join(dirpath, file))

# select 150 files randomly  
a = 150             
choices = random.sample(range(0, 1131), a)
print(choices)

# copy files to target directory
for i in range(speaker_number):
    j = j + 1131
    for files in range(a):
        file = files + (j * i)
        shutil.copy(source_files[choices[file]], target_dir)
        shutil.copy(prompt_files[choices[files]], prompt_target_dir)