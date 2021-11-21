import os
import shutil

source_dir = "D:\\thesis\\ali\\0004"
prompt_dir = "D:\\thesis\\corpus\\transcripts_test"
target_dir = "D:\\thesis\\ali\\txt" 
i = 0
j = -1

source_files = []
prompt_files = []

for dirpath, dirnames, filenames in os.walk(source_dir):
    for file in filenames:
        if file.endswith(".wav"):
            source_files.append(os.path.join(dirpath, file))


for dirpath, dirnames, filenames in os.walk(prompt_dir):
    for file in filenames:
        if file.endswith(".txt"):
            prompt_files.append(os.path.join(dirpath, file))

ch = prompt_files[0]
chk = ch
print(chk)

for dirpath, dirnames, filenames in os.walk(prompt_dir):
    for file in filenames:
        wav_checked = source_files[i]
        wav_trimmed = wav_checked[-8:-4]
        j = j + 1
        txt_checked = prompt_files[j]
        txt_trimmed = txt_checked[-8:-4]
        if wav_trimmed == txt_trimmed:
            shutil.copy(prompt_files[j+1], target_dir)
            i = i + 1