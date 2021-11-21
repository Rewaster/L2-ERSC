# create_textgrid_mfa_simple.praat
# Written by E. Chodroff
# Adjusted for .txt prompts by D. Bergman
# Originally written in Oct 23 2018, Modified in June 2021

# This script takes as input a directory containing wav files and 
# outputs TextGrids with a single tier called "words" (for further splitting  
# and alignment) and a single interval with the text of the transcript.
# The first boundary is currently set at 200 ms from the start.
# The second and final boundary is currently set at 200 ms from the end.

### CHANGE ME!
# directory with wav files that need TextGrids
dir$ = "D:/thesis/cut/0003/"

# Directory with transcripts
dirpr$ = "D:/thesis/ali/txt/"

## Maybe change me
# insert initial boundary 100 ms from start of file
boundary_start = 0.100

# insert final boundary 100 ms from end of file
boundary_end = 0.100
##

Create Strings as file list: "files", dir$ + "*.wav"
nFiles = Get number of strings
Create Strings as file list: "prompts", dirpr$ + "*.txt"
nPrompts = Get number of strings

for i from 1 to nFiles
	selectObject: "Strings prompts"
	filename1$ = Get string: i
	test$ = dirpr$ + filename1$
	text$ = readFile$ (test$)
	selectObject: "Strings files"
	filename$ = Get string: i
	basename$ = filename$ - ".wav"
	Read from file: dir$ + basename$ + ".wav"
	dur = Get total duration
	To TextGrid: "words", ""
	Insert boundary: 1, boundary_start
	Insert boundary: 1, dur-boundary_end
     	Set interval text: 1, 2, text$
	Save as text file: dir$ + basename$ + ".TextGrid"
	select all
	minusObject: "Strings files"
	minusObject: "Strings prompts"
	Remove
endfor