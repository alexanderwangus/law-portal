import numpy as np, copy
from pymongo import MongoClient
import GenerateFakeData as gfd
import sys, getopt


client = MongoClient("mongodb://localhost:27017")
db = client.test

def loadData():
  sections = gfd.getFakeData()
  for wordLists in sections:
    for wordList in wordLists:
      db.test.insert_one({
        "word" : wordList[0],
        "year" : int(wordList[1])
      })

def fetchWords(startYear, endYear):
  cursor = db.test.find({"$and": [{"year": {"$gte": startYear}}, {"year": {"$lte": endYear}}]})
  for document in cursor:
    print document["word"], document["year"]

def main(argv):
  # loadData()
  opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
  fetchWords(int(args[0]), int(args[1]))

# Usage: python portal.py [Start Year] [End Year]
# Note: Years are inclusive
if __name__ == '__main__': main(sys.argv[1:])