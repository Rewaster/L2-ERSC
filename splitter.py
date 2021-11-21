filepath = 'D:/thesis/PROMPTS.txt' # Unedited prompt
with open(filepath) as fp: 
    line = fp.readline() # Take the lines in succession
    cnt = 0 # Maybe return one instead of zero if doesn't work
    while line:
        print("Line {}: {}".format(cnt, line.strip())) # Just for visibility that works, can be omitted
        clean_line = line.strip()
        size = len(clean_line)
        mod_line = (clean_line[16:size - 3]) # Cleaning up the original prompt's formatting mess
        print(mod_line) # Boasting about it
        clean_prompt = open("D:/thesis/corpus/transcripts/full_prompt.txt", "a")
        clean_prompt.write(mod_line + "\n") # Again and again
        cnt_padded = str(cnt).zfill(4) # Padding with zeroes, Praat sorts as text otherwise
        f = open("D:/thesis/corpus/transcripts_test/prompt%s.txt" %cnt_padded, "w+") # format doesn't work here for some reason, sticked to classics
        f.write(mod_line)
        line = fp.readline() # Saving everything to file and checking
        cnt += 1
