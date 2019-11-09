import ast
import os


def removeTree(rel, att):
	final_b_plus_tree = {}
	#Ask user which B+ tree he wants to delete
	#get the B+ tree name and save it into a variable
	b_tree_name = raw_input("Enter B+ tree name which you want to delete")
	print(b_tree_name)
	
	#check whether the B+ tree is exist in Directory
	existing_b_tree_list = helper.read_from_file_to_list("../index/directory.txt")
	for item in existing_b_tree_list:
		if item == b_tree_name:
			b_tree_need_to_be_delete = item
		else:
			print('Tree not found')

	#Find that B+ tree in Tree pic file		
	file_list_in_treePic = os.listdir("../treePic")
	for item in file_list_in_treePic:
		if item == b_tree_need_to_be_delete
			final_b_plus_tree == item
		else:
			print('File not found in treePic')
	
	#Read json and extract file list
	with open(final_b_plus_tree) as f:
		final_b_plus_tree_file_content = f.read()
		file_list_to_be_delete = json.loads(final_b_plus_tree_file_content)
		file_list_in_index = os.listdir("../index")
		#Iterate on file list and delete file one by one from Index
		for item in file_list_to_be_delete:
			if item in file_list_in_index
				os.remove("../index/"+item)
			else:
				print("File not found in index")
		#After iteration will complete delete file from tree pic
		os.remove("../treePic/"+final_b_plus_tree)
	return

def removeTable(rel):
    return

    
    
    
    