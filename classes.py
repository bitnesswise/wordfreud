import datetime
import re
import warnings

# Collection of properties that define how the list is generated
# As well as some convenience functions that allow us to work with these properties in a smooth way
class Properties:
	# initialize with default values
	def __init__(self):
		### number properties
		# when true, it will convert four-digit years to two digit years and add them as well
		self.fullYear2shortYear = True
		# when true, it will convert four-digit years to an age and add it as well
		self.fullYear2age = True
		# year offset. if set, it should be a four digit year that will then be used instead of the current
		# year to determine the age of any year that is encoutered.
		# so, if the numberlist contains 1970 and the offsetYear is 2000 then the age is 30
		self.offsetYear = None
		### character properties
		# special characters we want to add to every word
		self.charSpecials = "!@"
		# when true, it appends the character to the word
		self.charPrependNo = False
		# when true, it prepends the character to the word
		self.charAppendNo = True
		### substitute properties
		# substitution map; substitutions are separated by a comma; first character is to be substituted by second character
		# p.e.: self.subMap = "a@,e3,i1,o0"
		self.subMap = ""
		# when true, a lowercase version of the word is added
		self.subToLower = True
		# when true, an uppercase version of the word is added
		self.subToUpper = True
		# when true, a CamelCase version of the word is added
		self.subCamelCase = True
		### Other properties
		## prepend append
		# when true, it will prepend words with the combination of numbers and special characters
		self.charNoPrepend = False
		# when true, it will append words with the combination of numbers and special characters
		self.charNoAppend = True
		## glue
		# characters that are to be used to glue things together (spaces between words for example)
		self.glueChars = " ._-"
		# when true, it will also use glue to combine words with numbers/special characters
		self.glueAll = False

	def getCharacterSubstitutes(self):
		subList = self.substitute.split(",")
		subDic = []
		for sub in subList:
			if sub[0] in subDic:
				warning.warn(sub[0]+" already existed. Old value "+subDic[sub[0]]+" will be overwritten by "+sub[1])
			subDic[sub[0]] = sub[1]
		return subList

	def getGlueCharactersAsList(self):
		charList = [""]
		for x in range(len(self.glueChars)):
			charList.append(self.glueChars[x])
		return charList

	def getSpecialCharsAsList(self):
		charList = []
		for x in range(len(self.charSpecials)):
			charList.append(self.charSpecials[x])
		return charList

	def getMapAsDict(self):
		if len(self.subMap) == 0:
			return {}
		elif (not self.subMap.find(",")) and len(self.subMap) >= 4:
			print("WARNING : can't map the special characters because there is no separator (,)")
			return {}
		else:
			charDict = {}
			mapList = self.subMap.split(",")
			for m in mapList:
				if len(m) != 2:
					print("WARNING: the length of "+m+" is not equal to two, so it's ignored")
					continue
				k = m[0:1]
				v = m[1:2]
				if k in charDict:
					print("WARNING: can only have 1 replacement value for "+k+" - multiple given. Using the first ("+charDict[k]+") only")
				else:
					charDict[k] = v
			return charDict

# Collection of functions that can generate certain aspects of the list
# Has to be initialized with a Properties object
class Toolbox:
	def __init__(self, properties):
		self.props = properties

	# Generate a list of the inputted numbers and their variations
	# 1. if a year is detected, the age is calculated and added
	# 2. if a four-digit year is detected, the two digit variant is added
	def getNumberVariations(self, numbers):
		output = []
		thisYear = datetime.datetime.now().year
		if self.props.offsetYear is not None:
			offsetYear = int(self.props.offsetYear)
			if offsetYear < 1900:
				warnings.warn("unsupported offset year: "+str(self.props.offsetYear)+" - it will be ignored")
			elif offsetYear > thisYear:
				warnings.warn("offset year detected that is in the future: "+str(self.props.offsetYear)+" - it will be ignored")
			else:
				thisYear = offsetYear

		for number in numbers:
			if re.match("[^0-9]", number):
				warning.warn("unsupported number-string: "+number+" - it will be ignored")

			self.addNumberVariation(output, number)
			if int(number) > 1900 and int(number) <= thisYear:
				if self.props.fullYear2age:
					self.addNumberVariation(output, str(thisYear - int(number)))
					self.addNumberVariation(output, str(thisYear - int(number) - 1))
				if self.props.fullYear2shortYear:
					self.addNumberVariation(output, (number[2:]))
		return output

	# adds the number variations to the existing list of numbers they were based on, but only if they don't already exist
	# this function is much more generic than that and needs a new name
	def addNumberVariation(self, numbList, number):
		if number not in numbList:
			numbList.append(number)

	
	def addNumbers(self, words, numbers):
		output = []
		chars = self.props.getSpecialCharsAsList()

		# add word without anything
		for word in words:
			output.append(word)

		# add special characters to the words
		for char in chars:
			for word in words:
				if self.props.charNoAppend:
					output.append(word+char)
				if self.props.charNoPrepend:
					output.append(char+word)
		# generat all combinations of numbers & numbers + special characters
		finArr = []
		if (len(numbers) > 0):
			for number in numbers:
				finArr.append(number)
				for char in chars:
					finArr.append(char+number)
					finArr.append(number+char)
		elif (len(numbers) == 0 and self.props.glueAll):
			for char in chars:
				finArr.append(char)
	
		for fin in finArr:
			for word in words:
				if self.props.charNoAppend:
					if self.props.glueAll:
						output += self.glueWords([word,fin])
					else:
						output.append(word+fin)
				if self.props.charNoPrepend:
					if self.props.glueAll:
						output += self.glueWords([fin,word])
					else:
						output.append(fin+word)
		return output

	def addCharacterSubstitutions(self, words):
		output = []
		mapDict = self.props.getMapAsDict()
		for word in words:
			output.append(word)
			replaced = word
			for search in mapDict:
				replace = mapDict[search]
				replaced = replaced.replace(search, replace)
			if replaced != word:
				output.append(replaced)

		return output

	def unfrag(self, wordList, i=None, curCombo=None):
		if i is None:
			i = 0
			curCombo = []
		
		partList = wordList[i]
		j = i + 1
		if j < len(wordList):
			output = []
			curCombo.append("dummy")
			for part in partList:
				curCombo.pop()
				curCombo.append(part)
				fList = self.unfrag(wordList, j, curCombo)
				output = output + fList
			return output
		else:
			output = []
			for word in partList:
				tList = curCombo[:]
				tList.append(word)
				if len(tList) > 1:
					gList = self.glueWords(tList)
				else:
					gList = tList
				output = output + gList
			return output

	def genLineVariations(self, line):
		words = line.split(" ")
		wordList = []
		for word in words:
			wordList.append(self.genWordVariations(word))

		return self.unfrag(wordList)

	def genWordVariations(self, word):
		output = [word]
		if re.match("[a-zA-Z]", word):
			if self.props.subToLower and word.lower() is not word:
				output.append(word.lower())
			if self.props.subToUpper and word.upper() is not word:
				output.append(word.upper())
			if re.match("[a-zA-Z].*[a-zA-Z]", word):
				if self.props.subCamelCase:
					output.append(word[0].upper() + word[1:].lower())
		else:
			output.append(word)
		return output

	def glueWords(self, wordList):
		output = []
		glueList = self.props.getGlueCharactersAsList()

		for glue in glueList:
			output.append(glue.join(wordList))

		return output

class App:
	def __init__(self):
		self.isVerbose = True
	def setVerbose(self, boolean):
		self.isVerbose = boolean
	def output(self, msg):
		if (self.isVerbose):
			print(msg)
	
