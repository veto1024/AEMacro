#!/usr/bin/python

#################################################################
#
#	AJE Automated English and British Macro script with 
#	compare file generation and customizable rules. The script
#	asks for the file that the user wants to work with,
#	asks if they want the BE macro to be run as well, and 
#	if they want a compare file generated.
#
#	Note: Generating a compare file requires latexdiff to be
#	able to be run via command line (which should be the case
#	under normal TeX installations).
#
#
#	Version 0.1 (10/28/2014) - Main program: Jonathan Roveto
#
#       Revisions:
#
#       0.2 (11/2/2014) - Jonathan Roveto
#
#       Improved menu and included the ability to make edits
#       automatically applied. Further integrate Word macro changes
#       into this script. Modified customdict.txt to make note of
#       edits being automatically applied.
#
#       0.3 (11/12/2014) - Jonathan Roveto
#
#       Made the program prettier (beauty is subjective!)
#       The BE Macro should be fully integrated at this point.
#
#       0.4 (12/22/2014) - Jonathan Roveto
#
#       Included a few more standard edits
#       Added a few edits to the BE macro that fixes errors
#       such as size -> sise and horizon -> horison
#       Fully integrated pdflatex comparison file generator
#
#       1.0 (1/11/2015) - Jonathan Roveto
#
#       Full release!
#
#       Improved error handling and redefinition of comparison
#       stuff as a separate function. Fingers crossed!
#
#       A problem has been found whereby edits of the form
#       Eq.( -> Eq. (  crash the program. Possibly remedy with
#       regular expressions?
#
#       TODO:  Will the preamble be an issue?
#               
#               
#       
#       
#
#
#################################################################

import glob
import os
import re
import sys
import AJE

if __name__=="__main__":
	os.system('clear')
	flag=0

	#
	# Looks until the proper file is found (i.e., the person enters
	# the correct ID!
	#

	while (flag==0):
		os.system('clear')
		flag=AJE.FileFind(flag)

	#
	# In the next few lines, the files are opened, and the rules are
	# processed.
	#

	texfile=open(AJE.filename,'r+')
	newfile=open((AJE.filename.split('.')[0]+'_edited.'+'tex'),'w+')


	AJE.ProcessRules()

	# 
	# With the files open and rule list ready, the program goes
	# line by line performing edits.
	#
	with texfile as openfile:
		for line in openfile:
			newfile.write(str(AJE.AEMacro(line)))

	# 
	# This should tell the computer to run the latexdiff command and generate a
	# compare file with a _compare tag.
	#

	texfile.close()
	newfile.close()

	AJE.DiffFile()

	if AJE.options[0]==1: print 'Macro complete! God Save the Queen!'
	else: print 'Macro complete! The Queen was not consulted'

	print ''
	print 'Total number of edits performed: ',AJE.totedits
	print ''
	raw_input('Press enter to exit')
