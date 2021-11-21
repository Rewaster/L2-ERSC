from google.cloud import speech_v1 as speech
import os
import io
import string
import shutil

source_dir = ""
target_dir = "" 
ref_dir = ""
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]=".json"

# list of subdirectories containing .wav files and textgrids (assumes each speaker has his own folder)
subfolders = next(os.walk(source_dir))[1]

# number of speakers analyzed 
speaker_number = len(subfolders)

config = dict(
    language_code="en-US",
    enable_automatic_punctuation=False,
    model="video"
)

word_count = 0
amount_of_sentences = 0
wer_total = []
word_total = []

# all credit to https://holianh.github.io/portfolio/Cach-tinh-WER/ for the WER calculator
def wer(ref, hyp ,debug=False):
    r = ref.split()
    h = hyp.split()
    #costs will holds the costs, like in the Levenshtein distance algorithm
    costs = [[0 for inner in range(len(h)+1)] for outer in range(len(r)+1)]
    # backtrace will hold the operations we've done.
    # so we could later backtrace, like the WER algorithm requires us to.
    backtrace = [[0 for inner in range(len(h)+1)] for outer in range(len(r)+1)]

    OP_OK = 0
    OP_SUB = 1
    OP_INS = 2
    OP_DEL = 3

    DEL_PENALTY=1 # Tact
    INS_PENALTY=1 # Tact
    SUB_PENALTY=1 # Tact
    # First column represents the case where we achieve zero
    # hypothesis words by deleting all reference words.
    for i in range(1, len(r)+1):
        costs[i][0] = DEL_PENALTY*i
        backtrace[i][0] = OP_DEL

    # First row represents the case where we achieve the hypothesis
    # by inserting all hypothesis words into a zero-length reference.
    for j in range(1, len(h) + 1):
        costs[0][j] = INS_PENALTY * j
        backtrace[0][j] = OP_INS

    # computation
    for i in range(1, len(r)+1):
        for j in range(1, len(h)+1):
            if r[i-1] == h[j-1]:
                costs[i][j] = costs[i-1][j-1]
                backtrace[i][j] = OP_OK
            else:
                substitutionCost = costs[i-1][j-1] + SUB_PENALTY # penalty is always 1
                insertionCost    = costs[i][j-1] + INS_PENALTY   # penalty is always 1
                deletionCost     = costs[i-1][j] + DEL_PENALTY   # penalty is always 1

                costs[i][j] = min(substitutionCost, insertionCost, deletionCost)
                if costs[i][j] == substitutionCost:
                    backtrace[i][j] = OP_SUB
                elif costs[i][j] == insertionCost:
                    backtrace[i][j] = OP_INS
                else:
                    backtrace[i][j] = OP_DEL

    # back trace though the best route:
    i = len(r)
    j = len(h)
    numSub = 0
    numDel = 0
    numIns = 0
    numCor = 0
    if debug:
        print("OP\tREF\tHYP")
        lines = []
    while i > 0 or j > 0:
        if backtrace[i][j] == OP_OK:
            numCor += 1
            i-=1
            j-=1
            if debug:
                lines.append("OK\t" + r[i]+"\t"+h[j])
        elif backtrace[i][j] == OP_SUB:
            numSub +=1
            i-=1
            j-=1
            if debug:
                lines.append("SUB\t" + r[i]+"\t"+h[j])
        elif backtrace[i][j] == OP_INS:
            numIns += 1
            j-=1
            if debug:
                lines.append("INS\t" + "****" + "\t" + h[j])
        elif backtrace[i][j] == OP_DEL:
            numDel += 1
            i-=1
            if debug:
                lines.append("DEL\t" + r[i]+"\t"+"****")
    if debug:
        lines = reversed(lines)
        for line in lines:
            print(line)
        print("Ncor " + str(numCor))
        print("Nsub " + str(numSub))
        print("Ndel " + str(numDel))
        print("Nins " + str(numIns))
    return (numSub + numDel + numIns) / (float) (len(r))
    wer_result = round( (numSub + numDel + numIns) / (float) (len(r)), 3)
    return {'WER':wer_result, 'Cor':numCor, 'Sub':numSub, 'Ins':numIns, 'Del':numDel}

def speech_to_text(config, audio):
    client = speech.SpeechClient()
    response = client.recognize(config=config, audio=audio)
    transcript = print_sentences(response)
    return transcript

def print_sentences(response):
    for result in response.results:
        best_alternative = result.alternatives[0]
        transcript = best_alternative.transcript
        print("Sentence:",transcript)
        return transcript
        
if speaker_number == 0:
    speaker_number += 1
for j in range(speaker_number):
    wer_speaker = 0
    if not subfolders:
        speaker_folder = source_dir
    else:
        f = subfolders[j]
        speaker_folder = source_dir + str(f) + "\\"
    for dirpath, dirnames, filenames in os.walk(speaker_folder):
        for file in filenames:
            if file.endswith(".wav"):
                audio_path = speaker_folder + file
                amount_of_sentences += 1
                x = ".".join(file.split(".")[:-1])
                sentence_number = x[-4:]
                # my prompts are one number ahead of sentence number, adjust next line if necessary
                prompt_num = str(int(sentence_number)+1).zfill(4)
                with open(ref_dir + "prompt%s.txt" %prompt_num) as fp: 
                    s = fp.readline()
                    ref = s.translate(str.maketrans('', '', string.punctuation))
                    ref = ref.lower()
                    ref_len = len(ref.split())
                    word_count += ref_len
                with io.open(audio_path, "rb") as f:
                    content = f.read()
                    audio = {"content": content}
                    hyp = speech_to_text(config, audio)
                if not hyp:
                    with open(target_dir + "records_missing.txt", "a+", encoding='utf-16') as text_file:
                        text_file.write("Sentence missing: {0} \n".format(file))
                    shutil.copy(speaker_folder + file, target_dir)
                    print("Missed sentence #%s, copied to target folder" %sentence_number)
                else:
                    wer_speaker += wer(ref, hyp.lower(), debug=False)
                    with open(target_dir + "word_error_rate.txt", "a+", encoding='utf-16') as text_file:
                        text_file.write("Original sentence:%s\n" %ref)
                        text_file.write("Speech to Text sentence:%s\n" %hyp)
                        text_file.write("Word error rate for sentence {stn} is {err}\n".format(stn = amount_of_sentences, err = wer(ref, hyp.lower(), debug=False)))
    print("Word error rate for speaker {sp} is {err}".format(sp = j+1, err = wer_speaker/amount_of_sentences))
    with open(target_dir + "word_error_rate_total.txt", "a+", encoding='utf-16') as text_file:
        text_file.write("Word error rate for speaker {sp} is {err}\n".format(sp = j+1, err = wer_speaker/amount_of_sentences))
    amount_of_sentences = 0
    wer_total.append(wer_speaker)
    word_total.append(word_count)

    

            
