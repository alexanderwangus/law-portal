# -*- coding: utf-8 -*-

import numpy as np, copy
from pymongo import MongoClient


Base_Dir = "/Users/Wang/Documents/Work/law-portal/"

InFileName = Base_Dir + "Sample Text.txt"

def getFakeData():
	Chapters = {}

	####################
	##  Read in data  ##
	####################

	with open(InFileName, 'r') as InFile:
		for idx, line in enumerate(InFile):
			## Test if we've come to a new chapter
			# print idx, line
			if line == line.upper() \
			 and 'CHAPTER' in line \
			 and 'SUBCHAPTER' not in line:
				# print line
				Current_Chapter = line.rstrip('\n')
				Chapters[Current_Chapter] = {}
				Current_Subchapter = "" ## empty subchapter, for chapters that don't have subchapters.
				Chapters[Current_Chapter][Current_Subchapter] = {}
				continue
			elif line == line.upper() and 'SUBCHAPTER' in line:
				Current_Subchapter = line.rstrip('\n')
				Chapters[Current_Chapter][Current_Subchapter] = {}
				## if we do have subchapters, remove the empty subchapter
				if "" in Chapters[Current_Chapter]:
					del Chapters[Current_Chapter][""]
				continue
			elif "§" in line[:2]:
				Current_Section = line.rstrip('\n')
				Chapters[Current_Chapter][Current_Subchapter][Current_Section] = []
				continue
			elif line == "\n":
				continue ## for now, ignore blank lines.  We can re-insert them, as we desire, later on (e.g. between sections, subchapters, etc.).  For now, they just confuse the logic.
			else:
				Chapters[Current_Chapter][Current_Subchapter][Current_Section] += line.split() + ['\n'] ## preserve linebreaks as separate "words"

	##############################
	##  Print out word by word  ##
	##############################

	## Note: this could easily be changed to write to file or output to another format.

	# for Chapter, Subchapters in Chapters.iteritems():
	# 	print Chapter
	# 	for SubChapter, Sections in Subchapters.iteritems():
	# 		print SubChapter
	# 		for Section, Wordlist in Sections.iteritems():
	# 			print Section
	# 			for Word in Wordlist:
	# 				print Word


	######################################
	##  Randomly Assign Dates to Words  ##
	######################################

	## This will replace each word with a list, containing first the word and then the year that it was added.
	## The years will be randomly assigned.
	## First, I'll randomly generate a year, from 2000 to 2005
	## Then, I'll generate a number of consecutive words to be added in that year.

	Chapter_Data = copy.deepcopy(Chapters)  ## not really necessary, but I somewhat psychotically keep everything backed up.
	# print Chapter_Data
	words = []

	np.random.seed(42)

	YearAdded = np.random.randint(2000, 2005)
	N_Words = np.random.negative_binomial(15, 0.25)

	for Chapter, Subchapters in Chapter_Data.iteritems():
		for SubChapter, Sections in Subchapters.iteritems():
			for Section, Wordlist in Sections.iteritems():
				for wdx, Word in enumerate(Wordlist):
					Wordlist[wdx] = [Word, YearAdded]
					N_Words -= 1
					if N_Words == 0:
						YearAdded = np.random.randint(2000, 2005)
						N_Words = np.random.negative_binomial(15, 0.25)
				words.append(Wordlist)
	return words