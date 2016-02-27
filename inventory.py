import sys
import os

def openDatabase(filename, mode):
	return open(filename, mode)

def closeDatabase(filename):
	try:
		openDatabase(filename, 'r').close()
	except IOError:
		print("There was an error closing the database")
		pass
	

def deleteDatabase(filename):
	try:
		os.remove(filename)
	except OSError:
		print("File %s does not exist" % (filename))

def wipeDatabase(database):
	database.close()
	return openDatabase(database.name, "w+")

def readDatabase(database):
	database.seek(0)
	return database.read()

def inDatabase(database, item):
	data = readDatabase(database)
	if data.find(item[0]) == -1:
		return False
	else: 
		return True

def databaseToDict(database):
	items = {}
	tok = ""
	listing = [] 
	for char in readDatabase(database):
		if char != '\n':
			tok += char
		else:
			listing = tok.split(':')
			items[listing[0]] = [listing[0], listing[1], listing[2]]
			listing = []
			tok = ""
	return items

def createItem(database, item):
	if not inDatabase(database, item):
		database.write("%s:%s:%s" % (item[0], item[1], item[2]))
	else:
		print("Item %s already exits" % (item[0]))

def removeItem(database, item):
	data = readDatabase(database)
	itemIndex = data.find(item[0])
	if itemIndex == -1:
		print("Item %s not found" % (item[0]))
		sys.exit()
	nextNewline = data.find('\n', itemIndex, len(data))
	database = wipeDatabase(database)
	database.write(data[:itemIndex] + data[nextNewline+1:])



def printItem(database, item):
	if inDatabase(database, item[0]):
		print("Item: %s Stock: %s Location: %s" % (item[0], item[1], item[2]))
	else:
		print("Item %s not found" % (item[0]))

def listItems(database):
	items = databaseToDict(database)
	for item in items:
		printItem(database, items[item])

def parse(args):
	for arg in args:
		if arg == "-c":
			if len(args) == 2:
				openDatabase(args[1], 'w+')
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
				createItem(database, [args[2], args[3], args[4]])
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
		elif arg == "-g":
			if len(args) == 3:
				database = openDatabase(args[1], 'r')
				items = databaseToDict(database)
				printItem(database, items[args[2]])
			else:
				print("ERROR: inv -g [database] [item]")
		elif arg == "-e":
			if len(args) == 5:
				database = openDatabase(args[1], 'r')
				items = databaseToDict(database)
				if args[3] == "stock":
					items[args[2]] = str(int(items[args[2]][1]) + args[4])
	closeDatabase(args[1])

parse(sys.argv[1:])
