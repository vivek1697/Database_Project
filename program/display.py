import ast
import json
import pathlib
import os.path


def displayTree(fname):
    with open(os.path.join(os.path.dirname(__file__), "../index/" + fname),"r") as rootFile:
        content = json.loads(rootFile.read())
        with open(os.path.join(os.path.dirname(__file__), "../index/directory.txt"),"r") as directoryFile:
            directoryContent = json.loads(directoryFile.read())
            treeFileName = list(directoryContent.keys())[list(directoryContent.values()).index(content)]
            with open(os.path.join(os.path.dirname(__file__), "../treePic/" + treeFileName),"r") as treeFile:
                tree_json = json.loads(treeFile.read())
                print("The tree file is : "+treeFileName+"\n\nThe tree in an unordered format is ...")
                print(json.dumps(tree_json, indent=4))
    return treeFileName

def displayTable(rel, fname):
    # Ensure that proper path for the desired rel_att is fetched
    path = "../data/" + rel + "/"
    

    tuple_list = []
    content = open(os.path.join(os.path.dirname(__file__), path + "pageLink.txt"), 'r')
    rel_page_link_list = json.loads(content.read())
    content.close()
    for item in rel_page_link_list:
        content = open(os.path.join(os.path.dirname(__file__), path + item), 'r')
        tuples_in_file = json.loads(content.read())
        content.close()
        for eachTuple in tuples_in_file:
            tuple_list.append(eachTuple)

    
    if os.path.isfile(os.path.join(os.path.dirname(__file__), "../queryOutput/" + fname)):
        f = open(os.path.join(os.path.dirname(__file__), "../queryOutput/" + fname ), "a")
        f.write("\n" + rel + "\n")
        f.write("\n" + json.dumps(tuple_list) + "\n") 
        f.close()
    else:
        f = open(os.path.join(os.path.dirname(__file__), "../queryOutput/" + fname ), "w+")
        f.write("\n" + rel + "\n")
        f.write("\n" + json.dumps(tuple_list) + "\n")    
        f.close
    return


# displayTable("project_select_join_join_Supply_sid_Suppliers_sid_2_pid_Products_pid_0_cost_gte_47_0_sname_pname_cost_0","queryResult.txt")

# displayTree("pg94.txt")