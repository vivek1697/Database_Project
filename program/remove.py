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

	file_list_in_treePic = os.listdir("../treePic")
	for item in file_list_in_treePic:
		if item == b_tree_need_to_be_delete
		final_b_plus_tree == item
	else:
		print('File not found in treePic')
	#b_plus_tree_list_in_treePic = helper.read_from_file_to_list("../index/directory.txt") #need to read file name form folder , different case than others
    return

def removeTable(rel):
    return

    
    #If tree is there fetch that tree name
    #Find that B+ tree in Tree pic file
    #Read json and extract file list
    #Iterate on file list and delete file one by one from Index
    #After iteration will complete delete file from tree pic