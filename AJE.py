import os
import sys
import re
import glob

##################################################################
#
#	AJE Macro toolkit
#
#	Global variables:
#
#	filename = file name of Tex file to be processed
#
#	options = keeps track of user options:
#	[0] = Run the BE macro?
#	[1] = Generate a compare file?
#	[2] = Use custom dictionary?
#	An option of 1 activates that request
#
#	rules = list of rules in tuple format ('before','after')
#	
###################################################################	

totedits=0
rules=[]

def FileFind(flag):

###################################################################
#
#	FileFind is the top menu that asks for options such as the 
#	file name, whether the BE macro should be run, and whether
#	to create a compare file
#	
###################################################################

	global filename
	global options
	options=[0,0,0]
	os.system('cls')
	goodfile=[]

#
# ch initializes the _find_getch() function, which allows singe-key
# entry to be performed. The definition is inherent to the AJE module
#
	ch=_find_getch()

	print 'American/British English Macro for LaTeX v1.0'
	print ''
        print 'Note: (Y or N) really just means (Y or anything else)'
        print 'at the moment'
	print ''
	id=raw_input('Enter alphanumeric identifier for your submission (e.g., LJK3681A): ')

#
# The next few lines gets the current working directory and sets it
# so that the program can find the .tex files. 
#
	dir=os.getcwd()
	os.chdir(dir+'/')
	filelist=[]
	direct=glob.glob("*.tex")

#
# 'direct' has all .tex files, iterates with 'x', finds match with 'x' and 'id'
# from above. If nothing is found, returns error. 
#
# TODO: Create a menu of files if multiple files with same sub ID are found
#

#	for x in direct:
#		if id in x: goodfile=x
	menu={}
	nummenu=0
	filelist=[]
	for x in direct:
		if id in x:
			filelist.append(x)	
	if (len(filelist)==0):
		print 'File not found!'
		print 'Press Enter to try again'
		trash=raw_input()
		return flag
	for x in range(1,len(filelist)+1):
		print str(x)+' - '+filelist[x-1]
	print ''
	print 'Select target file: ',
	choice=raw_input()
	try:
                if int(choice) not in range(1,len(filelist)+1): return flag
                goodfile=filelist[int(choice)-1]
        except:
                return flag

	print ''
	print 'Target file: '+goodfile
	print ''
	print 'Is this the correct file? (Y or N) ',
	proceed=ch()
	print proceed
	if (proceed=='Y' or proceed=='y'):
		filename=str(goodfile)
	else: return flag
	flag=1
	print ''

#
# Asks if BE macro should be run, sets respective flag in 'options'
#
	print ''
	print 'Run British English macro? (Y or N) ',
	BEMacro=ch()
	print BEMacro
	if (BEMacro == 'Y' or BEMacro == 'y'):
		print ''
		print 'British English macro will run'
		options[0]=1
	else:
		print ''
		print 'British English macro will NOT run'
	print ''


#	print 'Use custom rules (from customrules.txt)?  (Y or N) ',
	customdic='Y'
#	print customdic
	if (customdic=='Y' or customdic=='y'):
#		print ''
#		print 'Custom rule list will be run'
		options[2]=1
#	else:
#		print ''
#		print 'Default rule list will be run'
#	print ''
        raw_input('Press Enter to continue')
	os.system('cls')
	return flag

def ProcessRules():
	
#########################################################################
#
# 	ProcessRules does just that! It generates all the normal edits
#	given by the current Word macro and appends them to the rules list: rules.
#	If the relevent option is marked in 'options', the custom rule list
# 	from the user will also be added
#
#########################################################################

	global options
	global rules
	
#
# This generates " around 3" -> " approximately 3", for example. This

# of rule generation procedure will probably be useful to generate other 
# repetative types of rules down the line. 

# Note: The space in front of the numbers for things like "3cm" ensures that
# TeX code does not get hit.

	for x in range(0,10):
		rules.append((0,' about '+str(x),' approximately '+str(x)))
		rules.append((0,' around '+str(x),' approximately '+str(x)))
		rules.append((0,'About '+str(x),' Approximately '+str(x)))
		rules.append((0,'Around '+str(x),' Approximately '+str(x)))
		rules.append((0,'Roughly '+str(x),' Approximately '+str(x)))
		rules.append((0,' roughly '+str(x),' approximately '+str(x)))
		rules.append((0,'Fig.'+str(x),'Fig. '+str(x)))
		rules.append((0,str(x)+' fold ',str(x)+'-fold '))
		rules.append((0,str(x)+' year old ',str(x)+'-year-old '))
		rules.append((0,str(x)+' month old ',str(x)+'-month-old '))
                for y in ['nm','kb','kB','u','cm','m','km','ng','mg','g',\
                          'kg','nl','ul','ml','l','nL','uL','mL','L','h',\
                          'min','s','cell','hr','M','mM','nM','uM','W','N','V','dB']:
                        
                        rules.append((0,' '+str(x)+y,' '+str(x)+' '+y))
                        
                        for z in ['thick','long','wide','tall','high']:
                                rules.append((0,str(x)+' '+y+' '+z,str(x)+'-'+y+'-'+z))
		
	

# This generates rules that require a-z wildcards. ord(i) gives the value of
# the byte of 'a' and 'z'. To grab the character, chr(x) inverts the option
#
# TODO: There has to be a way to mimick things like [a-z] . [A-Z] -> [a-z]. [A-Z]
#       without simply creating rules for EVERY combination. Also unsure
#       about the weird findReplacePatterns in the Word macro

	for x in range(ord('a'),ord('z')+1):

# This removes spaces before colons

                rules.append((0,str(chr(x))+' :',str(chr(x))+':'))

# Other replacements
# TODO: Do a like -> such as replacement

#                rules.append((0
		
# Theme used here is as follows:
#
# (A,B,C)
#
# A: 0 = Replace automatically, 1 = Ask user for replacement,
#    2 = British word that should remain when BE Macro Run
# B: Original
# C: First replacement
#
# Note that the 2-option routine could probably be mimicked somehow,
# but because the AE macro in Word has only ever had one replacement,
# I am just going to neglect it here.


	rules.append((0,'Acknowledgement ','Acknowledgements '))
	rules.append((0,'Acknowledgment ','Acknowledgments '))
	rules.append((0,' administrated',' administered'))
	rules.append((0,'. Also ','. Additionally, '))
	rules.append((0,' are showed',' are shown'))
	rules.append((0,'As a consequence of the fact that ','As a consequence '))
	rules.append((0,'as can be seen ','as seen '))
	rules.append((0,'As can be seen ','As shown '))
	rules.append((0,'As compared','Compared'))
	rules.append((0,' as mean',' as the mean'))
	rules.append((0,' as means',' as the means'))
	rules.append((0,'Because of the fact that ','Because '))
	rules.append((0,' because of the fact that ',' because '))
	rules.append((0,' been also ',' also been '))
	rules.append((0,'. Besides,','. Moreover,'))
	rules.append((0,'Besides ','In addition to '))
	rules.append((0,'But ','However, '))
	rules.append((0,' catalyzation ',' catalysis '))
	rules.append((0,'Certain of the ','Certain '))
	rules.append((0,' constituted of ',' composed of '))
	rules.append((0,' deals with ',' addresses '))
	rules.append((0,' deal with ',' address '))
#	rules.append((0,' due to the fact that ',' because '))
#	rules.append((0,'Due to the fact that','Because'))
	rules.append((0,'e.g, ','e.g., '))
	rules.append((0,'e.g. ','e.g., '))
	rules.append((0,'. Even though','. Although'))
	rules.append((0,' evidences ',' evidence '))
	rules.append((0,'Evidences ','Evidence '))
	rules.append((0,'For purpose of ','For the purpose of '))
	rules.append((0,' for purpose of ',' for the purpose of '))
	rules.append((0,' get ',' obtain '))
	rules.append((0,'Given the fact that ','Given that '))
	rules.append((0,' given the fact that ',' given that '))
	rules.append((0,' got ',' obtained '))
	rules.append((0,' has been showed ',' has been shown '))
	rules.append((0,' has been later ',' was subsequently '))
	rules.append((0,'. However ','. However, '))
	rules.append((0,'; however ','; however, '))
	rules.append((0,'i.e, ','i.e., '))
	rules.append((0,'i.e. ','i.e., '))
	rules.append((0,' is showed ',' is shown '))
	rules.append((0,' in order to ', ' to '))
        rules.append((0,'In order to ','To '))
        rules.append((0,'An individual that ','An individual who '))
        rules.append((0,' individuals that ',' individuals who '))
        rules.append((0,'Individuals that ','Individuals who '))
        rules.append((0,'Interestingly enough','Interestingly'))
        rules.append((0,"manufacture's","manufacturer's"))
        rules.append((0,'Moreover ','Moreover, '))
        rules.append((0,'Not many ','Few '))
	rules.append((0,' nowadays ',' currently '))
	rules.append((0,'Nowadays','Currently'))
	rules.append((0,' of the both ',' of both '))
        rules.append((0,'Patients that ','Patients who '))
        rules.append((0,'A patient that','A patient who'))
        rules.append((0,'People that ','People who '))
        rules.append((0,'A person that','A person who'))
	rules.append((0,' points out ',' notes '))
	rules.append((0,' point out ',' note '))
	rules.append((0,' pointed out ',' noted '))
	rules.append((0,' probably ',' most likely '))
	rules.append((0,' researches ',' studies '))
	rules.append((0,'Researches ','Studies '))
	rules.append((0,' see e.g., ',' see, e.g., '))
	rules.append((0,' see e.g. ',' see, e.g., '))
	rules.append((0,' see e.g., ',' see, e.g., '))
	rules.append((0,' saw ',' observed '))
	rules.append((0,' seen ',' observed '))
#	rules.append((0,' since ',' because '))
#	rules.append((0,'Since ','Because '))
	rules.append((0,' so as to ',' to '))
	rules.append((0,' statistical significant ',' statistically significant '))
	rules.append((0,' statistical difference ',' significant difference '))
	rules.append((0,' statistically different ',' significantly different '))
	rules.append((0,"a Student's ","Student's "))
	rules.append((0,"the Student's ","Student's "))
	rules.append((0,'Then ','Then, '))
	rules.append((0,'. Therefore ','. Therefore, '))
	rules.append((0,'; therefore ','; therefore, '))
	rules.append((0,' was showed ',' was shown '))
	rules.append((0,' were showed ',' were shown '))
	rules.append((0,' when it comes to ',' in regard to '))
	rules.append((0,'When it comes to ','In regard to '))
	rules.append((0,'When it comes to ','In regard to '))
	rules.append((0,' whether or not ',' whether '))
	rules.append((0,' worth to mention ',' worth mentioning '))
	rules.append((0,'A lot of ','Many '))
	rules.append((0,' a lot of ',' many '))
        rules.append((0,' also are ',' are also '))
        rules.append((0,' also is ',' is also '))
        rules.append((0,' also was ',' was also '))
        rules.append((0,' also were ',' were also '))
        rules.append((0,' also will ',' will also '))
        rules.append((0,' are showed ',' are shown '))
        rules.append((0,' asses ',' assess '))
        rules.append((0,' be also ',' also be '))
        rules.append((0,' certain of the ',' certain '))
        rules.append((0,' in a proper way ',' correctly '))
        rules.append((0,' is showed ',' is shown '))
        rules.append((0,' not many ',' few '))
        rules.append((0,'data was ','data were '))
        rules.append((0,'Data was ','Data were '))
        rules.append((0,'data is ','data are '))
        rules.append((0,'Data is ','Data are '))
        rules.append((0,'Data has been ','Data have been '))
        rules.append((0,' data has been ',' data have been '))
        rules.append((0,'This data ','These data '))
        rules.append((0,' this data ',' these data '))
        rules.append((0,' this data.',' these data.'))
        rules.append((0,'ally-','ally '))
        rules.append((3,' centre',' center'))
        rules.append((3,' fibre',' fiber'))
        rules.append((3,' litre ',' liter '))
        rules.append((3,' colour',' color'))
        rules.append((3,' flavour',' flavor'))
        rules.append((3,' humour ',' humor '))
        rules.append((3,' labour',' labor'))
        rules.append((3,' neighbour',' neighbor'))
        rules.append((3,' defence ',' defense '))
        rules.append((3,' licence',' license'))
        rules.append((3,' offence',' offense'))
        rules.append((3,' pretence ',' pretense '))
        

#
# If the user stipulated a custom rules list, this will add it
# the "if not" line skips over commented lines in the custome rule
# file. eval() tells Python to look at the string tuple in the .txt
# file and pretend it was an actual piece of code and is thus 
# able to append it like a normal tuple
#
	if(options[2]==1):
		custfile=open('customrules.txt','r+')
		with custfile as openfile:
			for line in openfile:
				if not line.startswith("#"):

#
# If a blank entry in a custom dictionary is found, it would normally
# break the program. The continue skips over it
#
					try:
                                                if len(eval(line)[1])>0:
                                                        rules.append(eval(line))
                                        except:
                                                continue

		custfile.close()	
#
# DEBUG: Prints rules list in a debugrules.txt file
#
#        debugrules=open('debugrules.txt','w+')
#        for x,y,z in rules:
#                debugrules.write(y+' -> '+z+'\n')
#        debugrules.close()

        
def AEMacro(line):

#############################################################################
#
#
#	The AEMacro is the meat and potatoes of the code! It iterates through
#	every "line" of a .tex document and performs every change in order.
#	The problem is that "lines" in .tex aren't just the words in between
#	a pair of periods. The lines are whenever the author stopped typing
#	and hit 'Enter', unfortunately. Maybe this can be fixed a bit later
#	so that you don't get a giant wall of text sometimes.
#
############################################################################
	global rules
	global options
	global totedits
	ch=_find_getch()

#
# This section returns the line if 1) it is a line with no characters (empty),
# 2) it is all spaces, 3) it is a latex comment line, which should
# be ignored, or 4) if it is a latex preamble code, with the exception of
# \abstract{blah blah blah}
#

	if len(line)==0: return line
	if len(line.strip())==0: return line
	if (line.strip()[0]=='%'):
		return line
	if (line.strip()[0]=='\\'):
                if 'abstract' not in line:
                        return line


#
# Iteration begins, if f = 1 from the (f,x,y) tuple, program asks for permission
# else it does the replacement
#

	for f,x,y in rules:
		if (x in line and (f==1 or (f==3 and options[0]==0))):

#
# The line is printed so that the user can see what is going on in the line
# before approving an edit.
#
#
                        print '****************Current Working Line************************'
                        print ''
			print line
			print ''
			print '************************************************************'
			print ''
			print ''

#
# skip is used to jump around in the split up 'newline' list. 'newline' is
# the line being evaluated for the current rule but blown apart. For example,
# the line 
#
#"I would like cake in order to be happy in order to make the world a better place
#
# would produce a 'newline' of 
#
# ['I would like cake','be happy','make the world a better place']
#
# for the 'in order to' rule. The program has 2 edits to ask about here. 'skip'
# tells it that the insertion of 'to' could happen at newline[skip]. At the first
# edit, 'to' may or may not be inserted at newline[1]. Once that edit is made
# (or not), skip is iterated by two because the insertion of 'to'/'in order to'
# means that newlie is now
#
# ['I would like cake',' to ','be happy','make the world a better place']
#
# Thus, the next edit's index is going to be inserted at newline[3], which requires
# skip to iterate by 2 to skip over 'be happy'
# 
# numsplits had a purpose.... just forgot what it was?
#
# 'space' hunts down where in the line that the edit occurs so that it can properly
# display it to the user
#
# xfound simply determines at what positions the searched for rules appear,
# which is taken advantage of 2 lines below it. This is needed when more than 1 of
# the same edit (e.g., two instances of "since" in a line) appears in a line.
# This is a list of the positions of the first characters of the current edit, allowing
# the user to be shown each edit and surrounding text before making a decision
# 

			skip=1
			newline=line.split(x)
			numsplits=len(newline)
			xfound=[m.start() for m in re.finditer(x,line)]

#
# iterates n times, where n is the number of times a target edit was found, asks
# the user if they want the edit to be made, and inserts it into newline, as described
# previously. 
#
			for iter in range(0,line.count(x)):
				space=line.find(x,xfound[iter],len(line))
				if ((space+len(x)/2)<20): space=20
				print ''
                                print '***********************Current edit***********************'
                                print ''
				print line[space+len(x)-20:space+len(x)+20]
				print ''
				print 'Replace \''+x+'\' with \''+y+'\'? (Y or N) ',
				edit=ch()
				print ''
				if (edit=='y' or edit=='Y'):
					newline.insert(skip,y)
					skip=skip+2
					totedits=totedits+1
				else:
					newline.insert(skip,x)
					skip=skip+2
#					line=line.replace(x,y,1)

#
# If an edit started at the first character of a line (possible with things like
# "In order to blah blah blah", generating 'newline' will have the first entry as
# ''. This simply pops that first entry. Newline is then joined back together as
# a complete line and returned to be output.
#
			if xfound[0]==0:
				newline.pop(0)			
			line=''
			line=line.join(newline)

#
# Repeat above procedure except do not prompt
#
		if (x in line and (f==0)):
                        
			skip=1
			newline=line.split(x)
			numsplits=len(newline)
			xfound=[m.start() for m in re.finditer(x,line)]

			for iter in range(0,line.count(x)):
				newline.insert(skip,y)
				skip=skip+2
				totedits=totedits+1
				
			if xfound[0]==0:
				newline.pop(0)			
			line=''
			line=line.join(newline)
                
	os.system('cls')

#
# BE Macro. This runs essentially identical to above
#

	if (options[0]==1):

#
# 'iz' -> 'is' conversion
#
#		if 'iz' in line:
#                        print '****************Current Working Line************************'
#                        print ''
#                        print line
#                        print ''
#                        print '************************************************************'
#                        print ''
#                        print ''
#			skip=1
#			newline=line.split('iz')
##			numsplits=len(newline)
#			xfound=[m.start() for m in re.finditer('iz',line)]
#			for iter in range(0,line.count('iz')):
#				space=line.find('iz',xfound[iter],len(line))
#				if (space<20): space=20
#				print ''
#                               print '***********************Current edit***********************'
#                                print ''
#				print line[space-20:space+20+2]
#				print ''
##				print 'Replace "-iz" with "is"? (Y or N) ',
##				edit=ch()
#                                edit='y'
#				if (edit=='y'or edit=='Y'):
#					newline.insert(skip,'is')
#					skip=skip+2
#					totedits=totedits+1
#				else:
#					newline.insert(skip,'iz')
#					skip=skip+2
#				print ''
##				print line
#			line=''
#			line=line.join(newline)
#		os.system('cls')
#
#
# 'yz' -> 'ys' correction
#
		if 'yz' in line:
                        print '****************Current Working Line************************'
                        print ''
                        print line
                        print ''
                        print '************************************************************'
                        print ''
                        print ''
			skip=1
			newline=line.split('yz')
			numsplits=len(newline)
			xfound=[m.start() for m in re.finditer('yz',line)]
			for iter in range(0,line.count('yz')):
                                print ''
                                print '***********************Current edit***********************'
                                print ''

				space=line.find('yz',xfound[iter],len(line))
				if (space<20): space=20
				print line[space-20:space+20+2]
				print ''
#				print 'Replace "-yz" with "ys"? (Y or N)',
#				edit=ch()
                                edit='y'
				if (edit=='y'or edit=='Y'):
					newline.insert(skip,'ys')
					skip=skip+2
					totedits=totedits+1
				else:
					newline.insert(skip,'yz')
					skip=skip+2
				print ''
			line=''
			line=line.join(newline)
		os.system('cls')

# Run through the British english substitutions
# Note: The end of the list catches incorrect yz/iz corrections,
# such as "size -> sise" and "horizon -> horison", and reverts back

                BErules=[(1,' color',' colour'),(1,' fiber',' fibre'),(1,' liter ',' litre '),(1,' flavor',' flavour'),(1,' humor ',' humour '),(1,' labor',' labour'),(1,' neighbor',' neighbour'),(1,' horison',' horizon'),(1,' sise',' size')]

                for f,x,y in BErules:
                        if (x in line and (f==1)):
                                os.system('cls')
                                print '****************Current Working Line************************'
                                print ''
                                print line
                                print ''
                                print '************************************************************'
                                print ''
                                print ''

                                skip=1
                                newline=line.split(x)
                                numsplits=len(newline)
                                xfound=[m.start() for m in re.finditer(x,line)]

                                for iter in range(0,line.count(x)):
                                        space=line.find(x,xfound[iter],len(line))
                                        if ((space+len(x)/2)<20): space=20
                                        print ''
                                        print '***********************Current edit***********************'
                                        print ''
                                        print line[space+len(x)-20:space+len(x)+20]
                                        print ''
#                                        print 'Replace \''+x+'\' with \''+y+'\'? (Y or N) ',
#                                        edit=ch()
                                        edit='y'
                                        print ''
                                        if (edit=='y' or edit=='Y'):
                                                newline.insert(skip,y)
                                                skip=skip+2
                                                totedits=totedits+1
                                        else:
                                                newline.insert(skip,x)
                                                skip=skip+2

                                if xfound[0]==0:
                                        newline.pop(0)			
                                line=''
                                line=line.join(newline)


	return line



def _find_getch():

##########################################################################
#
#	_find_getch() module. This is a linux/MS-compatible tool for
#	grabbing a single keyboard entry.
#	
#	The only problem is that it is not easy to break the terminal.
#	If you want to break the terminal, you need to Ctrl-Z and hold so
#	that the program sees it in the fraction of a second between
#	edits/requests for new 'ch' input. This probably needs to be
#	addressed at some point.
#
##########################################################################


    	try:
        	import termios
    	except ImportError:
        	# Non-POSIX. Return msvcrt's (Windows') getch.
        	import msvcrt
        	return msvcrt.getch
		
 # POSIX system. Create and return a getch that manipulates the tty.
	import tty, sys,termios
    	def _getch():
       		fd = sys.stdin.fileno()
        	old_settings = termios.tcgetattr(fd)
        	try:
            		tty.setraw(fd)
            		ch = sys.stdin.read(1)
        	finally:
            		termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

        	return ch
    	return _getch

def DiffFile():

##########################################################################
#
#       The DiffFile module asks the user if a compare file should be
#       generated. If so, the file is generated. The output is tossed
#       into \pdflatex to ensure that the main directory does not clutter
#
##########################################################################

        import subprocess
        global options
        global filename
        ch=_find_getch()

        print 'Generate compare file and PDF (Y or N)? ',
        generate=ch()
        print generate
        print ''

        if ((generate=='y' or generate=='Y')):        
                print 'Generating compare file.'
                print 'Please note that a comparison file cannot be generated if the original file cannot be compiled.'
                print 'This is often the case, e.g., when .cls files are not provided by the author.'
                        

                if not os.path.exists('pdflatex'):
                        os.makedirs('pdflatex')
                        
                makearg="latexdiff "+filename+' '+filename.split('.')[0]+'_edited.tex'+' > '\
                         +filename.split('.')[0]+'_compare.tex'
                print "argumen texecuted: "+str(makearg)
                try:
                        return_code=subprocess.call(makearg,shell=True)

                except:
                        print 'Comparison file could not be made.'
                        return
        
                makearg="pdflatex -interaction=batchmode --output-directory=pdflatex "+filename.split('.')[0]+"_compare.tex"
        
                try:
                        return_code=subprocess.call(makearg,shell=True)
                        print ''
                        print 'Comparison PDF can be found in the pdflatex directory'
                except:
                        print 'pdlatex could not be called. This is not unusual!'
                        return



        return

						




