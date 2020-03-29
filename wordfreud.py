import argparse
import time
import os
from classes import Toolbox
from classes import Properties
from classes import App

# Create object to deal with application logic
app = App()
# By default, switch off info/debug output (-v switches it on)
app.setVerbose(False)

# set commandline parameters
parser = argparse.ArgumentParser(usage='%(prog)s input-file-with-words [input-file-with-numbers] [options]')
parser.add_argument('wf', nargs=1, help='Input file with words', type=argparse.FileType('r'))
parser.add_argument('nf', nargs='?', help='(optional) Input file with numbers', type=argparse.FileType('r'))
parser.add_argument('-o', help='Output file. If omitted stdout is used', type=argparse.FileType('w'))
parser.add_argument('--fullyear2shortyear', help='Full year to short year; add yy based yyyy (year)', action='store_const', const=True, default=False)
parser.add_argument('--year2age', help='Year to age; add (current) age based on year', action='store_const', const=True, default=False)
parser.add_argument('--offsetyear', help='Offset year; this will be used to calculate the age of any year that is found (instead of the current year). Only works when -year2age flag is set', type=int)
parser.add_argument('-g', help='Glue; This determines which characters are used to glue individual pieces together. Pass all characters as a single string.\nExample: "_-." -> this will result in 3 characters being used as glue: _, - & .', default=' _-.')
parser.add_argument('-ga', help='Glue All; in this mode, \'glue\' is also put between words and special characters and/or numbers', action='store_const', const=True, default=False)
parser.add_argument('-c', help='Special Characters', type=str, default='')
parser.add_argument('-pc', help='Prepend Character', action='store_const', const=True, default=False)
parser.add_argument('-ac', help='Append Character', action='store_const', const=True, default=False)
parser.add_argument('-sm', help='Substitute Map', default="")
parser.add_argument('-sl', help='Substitute To Lowercase ', action='store_const', const=True, default=False)
parser.add_argument('-su', help='Substitute To Uppercase', action='store_const', const=True, default=False)
parser.add_argument('-sc', help='Substitute To CamelCase', action='store_const', const=True, default=False)
parser.add_argument('-v', help='Verbose', action='store_const', const=True, default=False)

args = parser.parse_args()

## initialize variables that deal with file i/o
# file pointer words
fpw = None
# file pointer numbers
fpn = None
# file pointer output
fpo = None
if type(args.wf) is list:
	fpw = args.wf[0]
else:
	fpw = args.wf
if args.nf is not None:
	fpn = args.nf
if args.o is not None:
	fpo = args.o

# initialize and populate Properties object based on the parameters that were wet
# this will determine how the list is generated
properties = Properties()
if args.g is not None:
	properties.glueChars = args.g
if args.c is not None:
	properties.charSpecials = args.c
if args.sm is not None:
	properties.subMap = args.sm
if args.offsetyear is not None:
	properties.offsetYear = args.offsetyear
# These booleans always have a value
if (not args.pc and not args.ac and (args.c or fpn is not None)):
	args.ac = True
properties.fullYear2shortYear = args.fullyear2shortyear
properties.fullYear2age = args.year2age
properties.glueAll = args.ga
properties.charNoPrepend = args.pc
properties.charNoAppend = args.ac
properties.subToLower = args.sl
properties.subToUpper = args.su
properties.subCamelCase = args.sc

app.setVerbose(args.v)

attrs = vars(properties)
app.output("-- init @ " + time.strftime("%Y-%m-%d %H:%M:%S") + " --\nProperties:")
app.output('\n'.join(" * %s: %s" % item for item in attrs.items())+"\n")

# get wordList
if fpw is not None:
	with fpw as f:
		content = f.readlines()
else:
	print("no file input - aborting")
wLines = [x.strip() for x in content]

# get numbers and generate variations
if fpn is not None:
	with fpn as f:
		content = f.readlines()
	nLines = [x.strip() for x in content]
	numbList = Toolbox(properties).getNumberVariations(nLines)
	app.output("numbers: " + ", ".join(numbList) + "\n")
else:
	numbList = []

result = []

totalResults = 0
for line in wLines:
	app.output("processing " + line)
	variations = Toolbox(properties).genLineVariations(line)
	app.output("- it has " + str(len(variations)) + " word-variations")
	result = Toolbox(properties).addNumbers(variations, numbList)
	app.output("- and it has " + str(len(result)) + " total variations with numbers and special characters")
	ncResult = len(result)
	result = Toolbox(properties).addCharacterSubstitutions(result)
	scResult = len(result)
	app.output("- and it has " + str(scResult - ncResult) + " total variations with substitution characters")
	if fpo is not None:
		fpo.write("\n".join(result) + "\n")
	else:
		print(os.linesep.join(result))
	app.output("- that is a total of "+str(scResult)+" combinations for "+line)
	totalResults += scResult

if fpw is not None:
	fpw.close()
if fpn is not None:
	fpn.close()
if fpo is not None:
	fpo.close()

app.output("\n-- finished @ " + time.strftime("%Y-%m-%d %H:%M:%S") + " :: "+str(totalResults)+" results in total --")
