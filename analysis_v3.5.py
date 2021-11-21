import textgrid
import os
import matplotlib.pyplot as plt
from collections import Counter
import pandas as pd  
import matplotlib.ticker as mtick

# source directory for files to copy from (ending with 2 backslashes!)
source_dir = "D:\\thesis\\t3\\"

# target directory for files to copy to (ending with 2 backslashes!)
target_dir = "D:\\thesis\\t4\\"  

# list of subdirectories containing .wav files and textgrids (assumes each speaker has his own folder)
subfolders = next(os.walk(source_dir))[1]

# number of speakers analyzed 
speaker_number = len(subfolders)

# empty lists and variables
output_phoneme_error_list = []
arpabet_phoneme_list = []
output_sent_mist_list = []
all_mist_list = []
all_speaker_list = []
word_total_list = []
total_word_count = 0

def error_recorder(error, sentence_number, speaker_number, arg, target_directory):
    with open(target_directory + "\\records_speaker_%s.txt" %speaker_number, "a+", encoding='utf-16') as text_file:
                              text_file.write("Error: {0} \n".format(error))
                              text_file.write("Sentence number: {0} \n".format(sentence_number))
                              if type(arg) == bool:
                                  text_file.write("Boundaries not aligned! Program will not function without boundaries under each other having the same time. \n")
                              else:
                                  text_file.write("Something went wrong! Most probably annotation error. Please check and correct. \n")

def dict_and_graph(error_init, arpabet, target_directory, label):
    error = error_init['ARPABET Phonemes'].value_counts()
    error_len = range(len(error))
    error = pd.to_numeric(error, downcast='float')
    for k in error_len:
                    for j in range(len(arpabet)):
                        l1 = error.index.values[k]
                        l2 = list(arpabet)[j]
                        if l1 == l2:
                            error[l1] = float(error[l1]/arpabet[l1]*100)
    error_tr = error
    for v in range(len(error_tr)-1,0,-1):
        if label == 'Addition' and error_tr[v] < 1 or error_tr.index.values[v] == 'sp':
            error_tr = error_tr.drop(error_tr.index.values[v], axis = 0)
        elif label == 'Deletion' and error_tr[v] <= 1:
           error_tr = error_tr.drop(error_tr.index.values[v], axis = 0)
        elif label == 'Substitution' and error_tr[v] <= 5 or error_tr.index.values[v] == 'I':
            error_tr = error_tr.drop(error_tr.index.values[v], axis = 0)
        else:
            continue
    error_tr.sort_values(ascending=False).plot.bar(align='center', width=0.5, figsize=(14, 7))\
        .yaxis.set_major_formatter(mtick.PercentFormatter())
    plt.savefig(target_dir + "bar_plot_%s_error_all_speakers.jpg" %label, dpi = 500)
    plt.clf()
    error_all = error_init.groupby(['ARPABET Phonemes', 'Speaker']).size().unstack(fill_value=0)
    error_new = error_init['ARPABET Phonemes'].value_counts()
    for l in list(error_all.columns.values):
        for m in range(len(error_all.index)):
            for n in range(len(error_new)):
                l1 = error_all.index.values[m]
                l2 = error_new.index.values[n]
                if l1 == l2:
                    if error_all.loc[l1, l] != 0 and error_new[l1] != 0:
                        error_all.loc[l1, l] = error_all.loc[l1, l]/error_new[l1]*100
                    else:
                        continue
    error2 = error_all
    for m in error_len:
        for n in range(len(error2.index)-1,0,-1):
            if error2.index[n] == error.index.values[m]:
                if label == 'Addition' and error[m] < 1 or error.index.values[m] == 'sp':
                    error2 = error2.drop(error2.index.values[n], axis = 0)
                elif label == 'Deletion' and error[m] <= 1:
                    error2 = error2.drop(error2.index.values[n], axis = 0)
                elif label == 'Substitution' and error[m] <= 10 or error.index.values[m] == 'I':
                    error2 = error2.drop(error2.index.values[n], axis = 0)
                else:
                    continue
            else:
                continue
    error2.plot.bar(align='center', width=0.5, figsize=(14, 7)).yaxis.set_major_formatter(mtick.PercentFormatter())
    plt.savefig(target_dir + "bar_plot_%s_error_per_speaker.jpg" %label, dpi = 500)
    plt.clf()

def make_autopct(values):
    def my_autopct(pct):
        total = sum(values)
        val = int(round(pct*total/100.0))
        return '{p:.2f}%  ({v:d})'.format(p=pct,v=val)
    return my_autopct

def data_export(errors, words, sentences, target_dir, all_arpabet_phon, arpabet_phon, speaker_id, speaker_folders):
    orig_phoneme = []
    err = []
    err_type = []
    labels = ['Addition','Deletion','Distortion','Substitution']
    search_labels = ['a','d','dis','s']
    for i in range(len(errors)):
        e = errors[i]
        e = e.replace(" ", "").split(",")
        orig_phoneme.append(e[0])
        err.append(e[1])
        err_type.append(e[2])
    data = {'Original Phoneme':orig_phoneme, 'ARPABET Phonemes':arpabet_phon, 'Error':err, 'Type of Error':err_type, 'Word': words, 'Sentence number': sentences, 'Speaker': speaker_id}
    df = pd.DataFrame(data)
    df_pie = df['Type of Error'].value_counts()
    #explsion
    df_pie.plot.pie(figsize=(7, 7), labels = ['Substitution','Distortion','Deletion','Addition'], startangle=90).set_ylabel('')
    #draw circle
    centre_circle = plt.Circle((0,0),0.6,fc='white')
    fig = plt.gcf()
    fig.gca().add_artist(centre_circle)
    plt.tight_layout()
    my_circle=plt.Circle( (0,0), 0.6, color='white')
    p=plt.gcf()
    p.gca().add_artist(my_circle)
    plt.savefig(target_dir + "pie_chart_all_error_all_speakers.jpg", dpi = 500)
    plt.clf()
    for i in range(len(search_labels)):
        a = df.loc[df['Type of Error'] == search_labels[i]]
        b = a['Speaker'].value_counts()
        b.plot.pie(figsize=(5, 5)).set_ylabel('')
        my_circle=plt.Circle((0,0), 0.6, color='white')
        p=plt.gcf()
        p.gca().add_artist(my_circle)
        plt.savefig(target_dir + "pie_chart_%s_error_all_speakers.jpg" %labels[i], dpi = 500)
        plt.clf()
        if search_labels[i] != 's' and search_labels[i] != 'dis':
            dict_and_graph(a, all_arpabet_phon, target_dir, labels[i])
        else:
            if search_labels[i] == 'dis':
                f = df.loc[df['Type of Error'] == search_labels[i]]
            elif search_labels[i] == 's':
                bigdata = pd.concat([f, df.loc[df['Type of Error'] == search_labels[i]]])
                dict_and_graph(bigdata, all_arpabet_phon, target_dir, labels[i]) 
    #a.groupby(['Type of Error', 'ARPABET Phoneme'])['Type of Error'].count()
    print(df)
    df.to_csv(target_dir + "\\error_breakdown_table_speaker.csv", encoding='utf-16', index=False)
    return df

for j in range(speaker_number):
    # empty lists for collecting files and errors
    source_files = []  
    sent_mist_list = []
    phoneme_error_list = []
    word_list = []
    mist_list = []
    speaker_list = []
    word_count = 0
    s = 0
    a = 0
    d = 0
    f = subfolders[j]
    n = j + 1
    path_to_target_dir = target_dir + str(f)
    # walk through directory tree and find TextGrid files only
    for dirpath, dirnames, filenames in os.walk(source_dir + str(f)):
        for file in filenames:
            if file.endswith(".TextGrid"):
                source_files.append(os.path.join(file))
    # counting files to go through when recording everything needed
    i = len(source_files)
    # going through every file
    for files in range(i):
        # using textgrid to open every file
       tg = textgrid.TextGrid.fromFile(source_dir + f + '\\' + source_files[files])
       # looking at the total intervals on phones and words tier
       phones = len(tg[1])
       words = len(tg[0])
       for word in range(words):
                    if tg[0][word] != "" and tg[0][word] != "sil" and tg[0][word] != "sp" and tg[0][word] != "spn":
                        word_count = word_count + 1
       for p in range(phones):
           arpabet_phoneme = tg[1][p].mark
           if arpabet_phoneme != "" and arpabet_phoneme != "sil" and arpabet_phoneme != "sp" and arpabet_phoneme != "spn":
               if arpabet_phoneme[-1:] == '0' or arpabet_phoneme[-1:] == '1' or arpabet_phoneme[-1:] == '2':
                   arpabet_phoneme = arpabet_phoneme[:-1]
                   arpabet_phoneme_list.append(arpabet_phoneme)
               else:
                   arpabet_phoneme_list.append(arpabet_phoneme)
        # looking at the total intervals on mistakes tier
       mist = len(tg[2])
       # specifying the variable for each file name in order for the text in the results file to look readable
       k = source_files[files]
       # removing zero padding and extra letters to just get a sentence number
       # this might be useful for analysis of the most difficult sentences, works with my template of sentences which is speaker number + item + zero-padded sentence number.Textgrid
       k = ".".join(k.split(".")[:-1])
       # The following two lines assume that the number of the sentence is zero-padded, 4-digit number, change if needed
       k = k[-4:]
       k = k.lstrip("0")
       # checking if directory exists, if not, creating it with the same folder names as the speakers
       isExist = os.path.exists(path_to_target_dir)
       if not isExist:
          # Create a new directory because it does not exist 
          os.makedirs(path_to_target_dir)
          print("The new directory %s is created!" %path_to_target_dir)
       for trv in range(mist):
           # two failsafes to check whether or not all boundaries are aligned (if they are not, they might not be recorded as errors in this script)
           word_boundary = False
           phoneme_boundary = False
           # getting the text for each interval on the comments tier
           m = tg[2][trv]
           mr = m.mark
           # if it's not silent or just noise, we look at which mistake does it have recorded and increase the corresponding value
           if mr != "" and mr != "sil" and mr != "sp" and mr != "spn":
               # recording all words with mistakes that are there
               for wm in range(words):
                   if tg[0][wm].minTime <= m.minTime and tg[0][wm].maxTime >= m.maxTime:
                       word_list.append(tg[0][wm].mark)
                       word_boundary = True
                       break
               if not word_boundary:
                       error_recorder(mr, k, n, word_boundary, path_to_target_dir)
               # recording sentence number and the errors into their own respective lists
               sent_mist_list.append(k)
               mist_list.append(mr)
               # Counting the amount of times the error has been spotted, adding the phoneme with the same boundaries to the list for further analysis and graph creation
               if mr[len(mr)-1] == "s" or mr[len(mr)-1] == "a" or mr[len(mr)-1] == "d" or mr[-4:] == "dis":
                   for l in range(phones):
                       if tg[1][l].minTime == m.minTime and tg[1][l].maxTime == m.maxTime:
                           ddc_phoneme = tg[1][l].mark
                           if ddc_phoneme[-1:] == '0' or ddc_phoneme[-1:] == '1' or ddc_phoneme[-1:] == '2':
                               ddc_phoneme = ddc_phoneme[:-1]
                               phoneme_error_list.append(ddc_phoneme)
                               speaker_list.append(f)
                               phoneme_boundary = True
                           else:
                               phoneme_error_list.append(ddc_phoneme)
                               speaker_list.append(f)
                               phoneme_boundary = True 
                   if not phoneme_boundary:
                       error_recorder(mr, k, n, phoneme_boundary, path_to_target_dir)
               # if it doesn't correspond to any label that we found, a text file is created to record an error, sentence number and a small notice
               else:
                   error_recorder(mr, k, n, 1, path_to_target_dir)
    # Outputing lists that contain total amount of every type of error (output_sub, output_add, output_del)
    # phonemes that were pronounced wrong during the manual annotation (output_phon_mist_list_sub, output_phon_mist_list_add, output_phon_mist_list_del),
    # a total list of words with mistakes to count which words were the hardest to pronounce (word_total list), total list of mistakes (output_sent_mist_list),
    # and a total count of words for every speaker in total (if all speakers read the same amount of words, could be replaced by a simple multiplication by amount of speakers)
    output_phoneme_error_list = output_phoneme_error_list + phoneme_error_list
    output_sent_mist_list = output_sent_mist_list + sent_mist_list
    word_total_list = word_total_list + word_list
    total_word_count = total_word_count + word_count
    all_mist_list = all_mist_list + mist_list
    all_speaker_list = all_speaker_list + speaker_list
a = data_export(all_mist_list, word_total_list, output_sent_mist_list, target_dir, Counter(arpabet_phoneme_list), output_phoneme_error_list, all_speaker_list, speaker_number)