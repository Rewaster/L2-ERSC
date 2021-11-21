import soundfile
import os
import shutil

source_dir = "D:\\thesis\\ali\\0004"
target_dir = "D:\\thesis\\ali\\to\\" 
source_files = []


for dirpath, dirnames, filenames in os.walk(source_dir):
    for file in filenames:
        if file.endswith(".wav"):
            source_files.append(os.path.join(dirpath, file))

for i in range(150):
    data, samplerate = soundfile.read(source_files[i])
    tm = source_files[i]
    nm = tm[-16:-4]
    soundfile.write(target_dir + nm + '.wav', data, samplerate, subtype='PCM_16')