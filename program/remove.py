import ast
import os
import json
import shutil


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
		for each in list(content.keys())[::-1]:
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
	if not os.path.isdir(os.path.join(os.path.dirname(__file__), "../data/" + rel)):
		print(os.path.join(os.path.dirname(__file__), "../data/" + rel))
		print("this relation does not exist.")
		return
	
	# restore page pool
	with open(os.path.join(os.path.dirname(__file__), "../data/" + rel + "/pageLink.txt"), "r") as pageLinkFile:
		pageLinkList = json.loads(pageLinkFile.read())
		content = open(os.path.join(os.path.dirname(__file__), "../data/pagePool.txt"), 'r+')
		page_pool_list = json.loads(content.read())
		page_pool_list.extend(pageLinkList)
		content.seek(0)
		content.truncate(0)
		content.write(json.dumps(page_pool_list))
		content.close()

	# clean the schema
	content = open(os.path.join(os.path.dirname(__file__), "../data/schemas.txt"), 'r+')
	schemas_list = json.loads(content.read())
	schemas_list = list(filter(lambda a: a if a[0] != rel else None, schemas_list))
	content.seek(0)
	content.truncate(0)
	content.write(json.dumps(schemas_list))
	content.close()

	# wipe the directory
	shutil.rmtree(os.path.join(os.path.dirname(__file__), "../data/" + rel))

	return

# removeTree("Supply", "pid")
# removeTable("project_Supply_sid_1")    
