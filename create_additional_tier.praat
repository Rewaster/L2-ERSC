# create_textgrid_mfa_simple.praat
# Written by by D. Bergman
# Originally written in June 2021

# This script takes as input a directory containing TextGrid files and 
# outputs TextGrids with an additional tier called "comments" 
# (for pronunciation errors). It also checks if there are two tiers already, 
# as it is tuned to work with two other scripts for this thesis, and if the file
# already has 3 tiers, it doesn't do anything. Caution: it selects and removes all
# of the files currently selected at the end of each iteration, be careful with 
# other files that you might have open!

### CHANGE ME!
# directory with TextGrid files that need additional tier
dir$ = "D:/thesis/cut/0003/"
targetdir$ = "D:/thesis/cut/0003/to/"

Create Strings as file list: "prompts", dir$ + "*.TextGrid"
nPrompts = Get number of strings

for i from 1 to nPrompts
	selectObject: "Strings prompts"
	filename$ = Get string: i
	basename$ = filename$ - ".TextGrid"
	Read from file: dir$ + basename$ + ".TextGrid"
	check = Get number of tiers
	if check = 2
		Insert interval tier: 3, "comments"
	endif
	Save as text file: targetdir$ + basename$ + ".TextGrid"
	select all
	minusObject: "Strings prompts"
	Remove
endfor