import json
import random
import bPlusTreeNodeStructs # This file is VERY IMPORTANT!!! It contains helper functions that I have created and defined to use for building the B+ Tree
import os

def build(rel, att, od):
    # Import page pool
    content = open(os.path.join(os.path.dirname(__file__), "../index/pagePool.txt"), 'r')
    page_pool_list = json.loads(content.read())
    content.close()

    # Ensure that proper path for the desired rel_att is fetched
    path = "../data/" + rel + "/"

    # fetch relation schemas
    content = open(os.path.join(os.path.dirname(__file__), "../data/schemas.txt"), 'r')
    schemas_list = json.loads(content.read())
    content.close()
    index = list(filter(lambda x : x != None, list(map(lambda a: a[3] if (
        a[0] == rel and a[1] == att) else None, schemas_list))))[0]

    # Import the column on which index is to be made
    att_column_data = []
    content = open(os.path.join(os.path.dirname(__file__), path + "pageLink.txt"), 'r')
    rel_page_link_list = json.loads(content.read())
    content.close()
    for item in rel_page_link_list:
        content = open(os.path.join(os.path.dirname(__file__), path + item), 'r')
        tuples_in_file = json.loads(content.read())
        content.close()
        for eachTuple in tuples_in_file:
            att_column_data.append(eachTuple[index])

    # remove duplicates in the attribute set and sort them for the B+ tree 
    sorted_att_set = sorted(list(set(att_column_data)))
    
    tree = [] # This variable will store the tree nodes
    
    # LOOP : Check conditions and append to Tree List (IMPORTANT)
    for item in sorted_att_set:
        itemNode = bPlusTreeNodeStructs.SingleNode(item)
        if len(tree) == 0:
            # create a root node
            root = bPlusTreeNodeStructs.TreeNode("nil", None, od, "")
            root.insertNodeAtEnd(itemNode)
            tree.append(root)
        elif len(tree) == 1 and tree[0].parentPtr == None:
            # there is a root node but it's not full
            root = tree[0]
            if root.isFull():
                # SPLIT Logic
                bPlusTreeNodeStructs.splitInHalfAndInsert(root, itemNode, tree)
            else:
                # append to the root node
                root.insertNodeAtEnd(itemNode)
        else:
            # more nodes exist
            # check against root node for fitting in value (in an ascending sort array it is always larger, so always to the right)
            rightMostNode = bPlusTreeNodeStructs.traverseRightUntilLeaf(next(tNode for tNode in tree if tNode.parentPtr == None)) # pass a root here or else everything will fail or go wrong. NOT GOOD CODE!!!!!! AAAAAA!!!!
            if rightMostNode.isFull():
                bPlusTreeNodeStructs.splitInHalfAndInsert(rightMostNode, itemNode, tree)
            else:
                rightMostNode.insertNodeAtEnd(itemNode)
            # select left or right tree

    # helps print the tree for debugging (generically commented)
    # for each in tree:
    #     print(each)

    # create a pass to assign data file pointers to leaf nodes (i.e page numbers and indexes to the place where the actual tuple is)
    for nodeIndex, leafNode in enumerate(tree):
        # for each leaf node in the tree list
        if leafNode.isLeaf:
            # if the node is a leaf then proceed
            for ind, specificKey in enumerate(leafNode.valueStruct):
                # for each key in the leaf node
                for eachFileName in rel_page_link_list:
                    # iterate over the files of the relation in question
                    # fetch all tuples in the respective page file
                    content = open(os.path.join(os.path.dirname(__file__), path + eachFileName), 'r')
                    tuples_in_file = json.loads(content.read())
                    content.close()
                    for respTupleIndex, eachTuple in enumerate(tuples_in_file):
                        # for each tuple in the page file
                        if specificKey.val == eachTuple[index]:
                            # append the tuple index and page file name to the leaf node key
                            tree[nodeIndex].valueStruct[ind].dataFilePtr.append(eachFileName+"."+str(respTupleIndex)) 

    

    # create a pass to insert tree pointers, i.e. pick page from page pool and assign it to nodes... and, probably create the file
    
    for eachNode in tree:
        page = random.choice(page_pool_list)
        eachNode.name = page
        page_pool_list.remove(page)
        

    # fetch the root node
    root = next(tNode for tNode in tree if tNode.parentPtr == None)

    bPlusTreeNodeStructs.recursivelyAssignPagesFromRoot(root)

    # this is another pass to assign leaf pages
    for eachNode in tree:
        if eachNode.isLeaf:
            eachNode.left = 'nil' if eachNode.leftPtr is None else eachNode.leftPtr.name
            eachNode.right = 'nil' if eachNode.rightPtr is None else eachNode.rightPtr.name

    # create tree JSON (Or list maybe? ASK this?)
    tree_json = {}
    for each in tree:
        temp = ['L' if each.isLeaf else 'I', 'nil' if each.parentPtr is None else each.parentLabel]

        values_I = []
        values_L = []
        for eachitem in each.valueStruct:
            if eachitem.prev not in values_I:
                values_I.append(eachitem.prev)
            values_I.append(eachitem.val)
            if eachitem.next not in values_I:
                values_I.append(eachitem.next)
            values_L.extend([eachitem.val, eachitem.dataFilePtr])

        if each.isLeaf:
            temp.extend([each.left, each.right])
            temp.append(values_L) 
        else:
            temp.append(values_I)

        tree_json[each.name] = temp

    # print the tree just in case as a json
    print(tree_json)

    # write the page pool back !!! IMPORTANT !!!! DO NOT FORGET
    
    # helps print the tree for debugging (generically commented)
    # for each in tree:
    #     print(each)

    # create a pass to shove into and create the files in a respective place, maybe?
    

    return

build("Supply", "pid", 2) # TO TEST 