import ast
import json
import pathlib
import os.path


def displayTree(fname):
    return

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

    
    if os.path.isfile(os.path.join(os.path.dirname(__file__), fname)):
        f = open(os.path.join(os.path.dirname(__file__), fname ), "a")
        f.write("\n" + rel + "\n")
        f.write("\n" + json.dumps(tuple_list) + "\n") 
        f.close()
    else:
        f = open(os.path.join(os.path.dirname(__file__), fname ), "w+")
        f.write("\n" + rel + "\n")
        f.write("\n" + json.dumps(tuple_list) + "\n")    
        f.close
    return


#displayTable("Products","abc.txt")

