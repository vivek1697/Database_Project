import ast
import os
import json


def removeTree(rel, att):
	if not os.path.isfile(os.path.join(os.path.dirname(__file__), "../treePic/"+rel+"_"+att+".txt")):
		print("b+ tree for given attribs does not exist")
		return

	# remove directory entry
	with open(os.path.join(os.path.dirname(__file__), "../index/directory.txt"),"r+") as directoryFile:
		content = json.loads(directoryFile.read())
		del content[rel+"_"+att+".txt"]
		directoryFile.seek(0)
		directoryFile.truncate(0)
		directoryFile.write(json.dumps(content))

	# remove index entries
	with open(os.path.join(os.path.dirname(__file__), "../treePic/"+rel+"_"+att+".txt"),"r") as treePicFile:
		pagePoolFile = open(os.path.join(os.path.dirname(__file__), "../index/pagePool.txt"),"r+")
		pagePool = json.loads(pagePoolFile.read())
		content = json.loads(treePicFile.read())
		for each in content.keys():
			pagePool.insert(0, each)
			os.remove(os.path.join(os.path.dirname(__file__), "../index/"+each))
		pagePoolFile.seek(0)
		pagePoolFile.truncate(0)
		pagePoolFile.write(json.dumps(pagePool))
		pagePoolFile.close()

	# remove treepic file
	os.remove(os.path.join(os.path.dirname(__file__), "../treePic/"+rel+"_"+att+".txt"))
	
	return

def removeTable(rel):
    return

removeTree("Supply", "pid")
    
    