import sys
import os

def createDatabase(filename):
	return open(filename, 'w+')

def openDatabase(filename, mode):
	return open(filename, mode)

def deleteDatabase(filename):
	try:
		os.remove(filename)
	except OSError:
		print("File %s does not exist" % (filename))

def wipeDatabase(database):
	database.close()
	return createDatabase(database.name)

def readDatabase(database):
	database.seek(0)
	return database.read()

def databaseToDict(database):
	items = []
	stocks = {}
	locations = {}
	tok = ""
	listing = [] 
	for char in readDatabase(database):
		if char != ';':
			tok += char
		else:
			listing = tok.split(':')
			items.append(listing[0])
			stocks[listing[0]] = listing[1]
			locations[listing[0]] = listing[2]
			tok = ""
	return items, stocks, locations

def createItem(database, item, stock, location):
	if readDatabase(database).find(item) == -1:
		database.write("%s:%s:%s;" % (item, stock, location))
	else:
		print("Item %s already exits" % (item))

def removeItem(database, item):
	data = readDatabase(database)
	itemIndex = data.find(item)
	if itemIndex == -1:
		print("Item %s not found" % (item))
		sys.exit()
	nextSemi = data.find(';', itemIndex)
	database = wipeDatabase(database)
	database.write(data[:itemIndex] + data[nextSemi+1:])

def listItems(database):
	items, stocks, locations = databaseToDict(database)
	for item in items:
		print("Item: %s Stock: %s Location: %s" % (item, stocks[item], locations[item]))

def parse(args):
	for arg in args:
		if arg == "-c":
			if len(args) == 2:
				createDatabase(args[1])
			else:
				print("ERROR: inv -c [filename]")
		elif arg == "-d":
			if len(args) == 2:
				deleteDatabase(args[1])
			else:
				print("ERROR: inv -d [filename]")
		elif arg == "-i":
			if len(args) == 5:
				database = openDatabase(args[1], 'r+')
				createItem(database, args[2], args[3], args[4])
			else:
				print("ERROR: inv -i [database] [item] [stock] [location]")
		elif arg == "-r":
			if len(args) == 3:
				database = openDatabase(args[1], 'r')
				removeItem(database, args[2])
			else:
				print("ERROR: inv -r [database] [item]")
		elif arg == "-l":
			if len(args) == 2:
				database = openDatabase(args[1], 'r')
				listItems(database)
			else:
				print("ERROR: inv -l [database]")

parse(sys.argv[1:])
