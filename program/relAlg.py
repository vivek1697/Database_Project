import ast
import random
import math
import os
import json
import collections
import glob

def select(rel, att, op, val):
    val = val
    if att == "cost":
        val = int(val)

    opr = ""
    if op == "=":
        opr = op        
    elif op == ">":
        opr = "gt"
    elif op == ">=":
        opr = "gte"
    elif op == "<":
        opr = "lt"
    elif op == "<=":
        opr = "lte"
    elif op == "!=":
        opr = "nte"

    # shove result into respective page files (create folders if necessary)
    folder_name = "select_"+rel+"_"+att+"_"+opr+"_"+str(val)
    rel_path = os.path.join(os.path.dirname(__file__),"../data/")
    if len(glob.glob(rel_path + folder_name + "_*")) != 0:
        num = int(sorted(glob.glob(rel_path + folder_name + "_[0-9]*"))[-1].split('/')[-1].split('_')[-1])
        folder_name = folder_name + "_" + str(num + 1)
    else:
        folder_name = folder_name + "_0"
    rel_path = rel_path + folder_name
    os.mkdir(rel_path)

    # fetch relation schemas
    
    schemasFile = open(os.path.join(os.path.dirname(__file__), "../data/schemas.txt"), 'r+')
    schemas_list = json.loads(schemasFile.read())
    new_schema = list(filter(lambda a: a != None, list(map(lambda a: [folder_name, a[1], a[2], a[3]] if a[0] == rel else None, schemas_list))))
    index = list(filter(lambda a: a != None, list(map(lambda a: a[3] if (a[0] == rel and a[1] == att) else None, schemas_list))))[0]
    schemas_list.extend(new_schema)
    schemasFile.seek(0)
    schemasFile.truncate(0)
    schemasFile.write(json.dumps(schemas_list))
    schemasFile.close()

    cost_b = 0
    selection_result = []
    att_column_data = []
    if os.path.isfile(os.path.join(os.path.dirname(__file__), "../treePic/"+rel+"_"+att+".txt")):
        treeFile = open(os.path.join(os.path.dirname(__file__), "../treePic/"+rel+"_"+att+".txt"), "r")
        tree_json = json.loads(treeFile.read())
        root_key = list(filter(lambda a: a if tree_json[a][1] == "nil" else None, tree_json.keys()))[0]
        key = root_key
        cost_b = cost_b + 1
        while tree_json[key][0] != "L":
            control_value = ""
            for each in tree_json[key][2][1::2]:
                if val < each:
                    control_value = each
                    break
            if control_value == "":
                key = tree_json[key][2][-1] 
            else:
                key = tree_json[key][2][tree_json[key][2].index(control_value)-1]
            cost_b = cost_b + 1

        leaf_key = key
        if "<" in op:
            if "=" in op:
                data_file_pointers_for_val = tree_json[leaf_key][4][tree_json[leaf_key][4].index(val)+1]
                for item in data_file_pointers_for_val:
                    fragments = item.split('.')
                    fetchedDataFile = fragments[0]+"."+fragments[1]
                    dataFileIndex = int(fragments[2])
                    openDataFile = open(os.path.join(os.path.dirname(__file__), "../data/" + rel + "/" + fetchedDataFile),"r")
                    dataTuple = json.loads(openDataFile.read())
                    cost_b = cost_b + 1
                    att_column_data.append(dataTuple[dataFileIndex])
            
            # handle left ward flow
            if tree_json[leaf_key][4].index(val) != 0:
                control_index = tree_json[leaf_key][4].index(val)-2 # skip the val index
                while not control_index < 0:
                    data_file_pointers_for_val = tree_json[leaf_key][4][control_index + 1]
                    for item in data_file_pointers_for_val:
                        fragments = item.split('.')
                        fetchedDataFile = fragments[0]+"."+fragments[1]
                        dataFileIndex = int(fragments[2])
                        openDataFile = open(os.path.join(os.path.dirname(__file__), "../data/" + rel + "/" + fetchedDataFile),"r")
                        dataTuple = json.loads(openDataFile.read())
                        cost_b = cost_b + 1
                        att_column_data.append(dataTuple[dataFileIndex])
                    control_index = control_index - 2
                
            # anyways do this
            left_key = tree_json[leaf_key][2] # becasue the leaf we were on has already been processed
            while tree_json[left_key][2] != "nil":
                # handle logic of leftward recursion
                for each in tree_json[left_key][4][::2]:
                    data_file_pointers_for_val = tree_json[left_key][4][tree_json[left_key][4].index(each)+1]
                    for item in data_file_pointers_for_val:
                        fragments = item.split('.')
                        fetchedDataFile = fragments[0]+"."+fragments[1]
                        dataFileIndex = int(fragments[2])
                        openDataFile = open(os.path.join(os.path.dirname(__file__), "../data/" + rel + "/" + fetchedDataFile),"r")
                        dataTuple = json.loads(openDataFile.read())
                        cost_b = cost_b + 1
                        att_column_data.append(dataTuple[dataFileIndex])
                
                cost_b = cost_b + 1
                
                # update left_key
                left_key = tree_json[left_key][2]

            # handle the last one too
            for each in tree_json[left_key][4][::2]:
                data_file_pointers_for_val = tree_json[left_key][4][tree_json[left_key][4].index(each)+1]
                for item in data_file_pointers_for_val:
                    fragments = item.split('.')
                    fetchedDataFile = fragments[0]+"."+fragments[1]
                    dataFileIndex = int(fragments[2])
                    openDataFile = open(os.path.join(os.path.dirname(__file__), "../data/" + rel + "/" + fetchedDataFile),"r")
                    dataTuple = json.loads(openDataFile.read())
                    cost_b = cost_b + 1
                    att_column_data.append(dataTuple[dataFileIndex])
            
            cost_b = cost_b + 1

        elif op == "=":
            data_file_pointers_for_val = tree_json[leaf_key][4][tree_json[leaf_key][4].index(val)+1]
            for item in data_file_pointers_for_val:
                fragments = item.split('.')
                fetchedDataFile = fragments[0]+"."+fragments[1]
                dataFileIndex = int(fragments[2])
                openDataFile = open(os.path.join(os.path.dirname(__file__), "../data/" + rel + "/" + fetchedDataFile),"r")
                dataTuple = json.loads(openDataFile.read())
                cost_b = cost_b + 1
                att_column_data.append(dataTuple[dataFileIndex])

        elif ">" in op:
            if "=" in op:
                data_file_pointers_for_val = tree_json[leaf_key][4][tree_json[leaf_key][4].index(val)+1]
                for item in data_file_pointers_for_val:
                    fragments = item.split('.')
                    fetchedDataFile = fragments[0]+"."+fragments[1]
                    dataFileIndex = int(fragments[2])
                    openDataFile = open(os.path.join(os.path.dirname(__file__), "../data/" + rel + "/" + fetchedDataFile),"r")
                    dataTuple = json.loads(openDataFile.read())
                    cost_b = cost_b + 1
                    att_column_data.append(dataTuple[dataFileIndex])
            
            # handle right ward flow
            if tree_json[leaf_key][4].index(val) != len(tree_json[leaf_key][4]):
                control_index = tree_json[leaf_key][4].index(val) + 2 # skip the val index
                while not control_index > len(tree_json[leaf_key][4]) - 1:
                    data_file_pointers_for_val = tree_json[leaf_key][4][control_index + 1]
                    for item in data_file_pointers_for_val:
                        fragments = item.split('.')
                        fetchedDataFile = fragments[0]+"."+fragments[1]
                        dataFileIndex = int(fragments[2])
                        openDataFile = open(os.path.join(os.path.dirname(__file__), "../data/" + rel + "/" + fetchedDataFile),"r")
                        dataTuple = json.loads(openDataFile.read())
                        cost_b = cost_b + 1
                        att_column_data.append(dataTuple[dataFileIndex])
                    control_index = control_index + 2
                
            # anyways do this
            right_key = tree_json[leaf_key][3] # becasue the eaf we were on has already been processed
            while tree_json[right_key][3] != "nil":
                # handle logic of leftward recursion
                for each in tree_json[right_key][4][::2]:
                    data_file_pointers_for_val = tree_json[right_key][4][tree_json[right_key][4].index(each)+1]
                    for item in data_file_pointers_for_val:
                        fragments = item.split('.')
                        fetchedDataFile = fragments[0]+"."+fragments[1]
                        dataFileIndex = int(fragments[2])
                        openDataFile = open(os.path.join(os.path.dirname(__file__), "../data/" + rel + "/" + fetchedDataFile),"r")
                        dataTuple = json.loads(openDataFile.read())
                        cost_b = cost_b + 1
                        att_column_data.append(dataTuple[dataFileIndex])
                
                cost_b = cost_b + 1
                
                # update left_key
                right_key = tree_json[right_key][3]

            # handle the last one too
            for each in tree_json[right_key][4][::2]:
                data_file_pointers_for_val = tree_json[right_key][4][tree_json[right_key][4].index(each)+1]
                for item in data_file_pointers_for_val:
                    fragments = item.split('.')
                    fetchedDataFile = fragments[0]+"."+fragments[1]
                    dataFileIndex = int(fragments[2])
                    openDataFile = open(os.path.join(os.path.dirname(__file__), "../data/" + rel + "/" + fetchedDataFile),"r")
                    dataTuple = json.loads(openDataFile.read())
                    cost_b = cost_b + 1
                    att_column_data.append(dataTuple[dataFileIndex])
            
            cost_b = cost_b + 1
        selection_result = att_column_data
        print("With B+ tree, on "+folder_name+" gives cost "+str(cost_b)+" pages")
    else:
        path = "../data/" + rel + "/"
        content = open(os.path.join(os.path.dirname(__file__), path + "pageLink.txt"), 'r')
        rel_page_link_list = json.loads(content.read())
        cost_b = len(rel_page_link_list)
        content.close()
        for item in rel_page_link_list:
            tupleFile = open(os.path.join(os.path.dirname(__file__), path + item), 'r')
            tuples_in_file = json.loads(tupleFile.read())
            tupleFile.close()
            for eachTuple in tuples_in_file:
                att_column_data.append(eachTuple)
        
        
        for item in att_column_data:
            if op == "=":
                if item[index] == val:
                    selection_result.append(item)
            elif op == ">":
                if item[index] > val:
                    selection_result.append(item)
            elif op == ">=":
                if item[index] >= val:
                    selection_result.append(item)
            elif op == "<":
                if item[index] < val:
                    selection_result.append(item)
            elif op == "<=":
                if item[index] <= val:
                    selection_result.append(item)
            elif op == "!=":
                if item[index] != val:
                    selection_result.append(item)
        print("Without B+ tree, on "+folder_name+" gives cost "+str(cost_b)+" pages")

    # Import page pool
    content = open(os.path.join(os.path.dirname(__file__), "../data/pagePool.txt"), 'r')
    page_pool_list = json.loads(content.read())
    content.close()

  	# Ensure that proper path for the desired rel_att is fetched
    path = "/data/" + rel + "/"

    # Write to individual pages
    pageLink = []
    length = math.ceil(len(selection_result)/2)
    for i in range(length):
        temp = selection_result[:2]
        selection_result = list(filter(lambda a: a not in temp,selection_result))
        page0 = page_pool_list[0]
        pageLink.append(page0)
        page_pool_list.remove(page0)
        f = open(rel_path + "/" + page0, 'w+')
        f.write(json.dumps(temp))
        f.close()

    # Write to pageLink
    with open(rel_path + "/pageLink.txt" , "w+") as content:
        content.write(json.dumps(pageLink))


    # rewrite page pool list
    with open(os.path.join(os.path.dirname(__file__), "../data/pagePool.txt"),"w") as pagePoolFile:
        pagePoolFile.write(json.dumps(page_pool_list))
    

    return folder_name

    


    
    #Select random page from pagepool
    #Enter Result in page one by one
    #if B tree from tree pic is exsits select data from B tree
    #if B tree is not exsits serch sequencial

def project(rel, attList):
    # fetch entire list of attributes [[list of att0], [list of att1], [list of att2]]
    # Import page pool
    content = open(os.path.join(os.path.dirname(__file__), "../data/pagePool.txt"), 'r')
    page_pool_list = json.loads(content.read())
    content.close()

    # Ensure that proper path for the desired rel_att is fetched
    path = "../data/" + rel + "/"

    # fetch relation schemas
    content = open(os.path.join(os.path.dirname(__file__), "../data/schemas.txt"), 'r')
    schemas_list = json.loads(content.read())
    content.close()
    indexes = {}
    for eachAtt in attList:
        indexes[eachAtt] = list(filter(lambda x : x != None, list(map(lambda a: a[3] if (
            a[0] == rel and a[1] == eachAtt) else None, schemas_list))))[0]

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
            att_column_data.append(list(filter(lambda x: x != None,list(map(lambda a: [a, next(z for z in indexes.keys() if indexes[z] == eachTuple.index(a))] if eachTuple.index(a) in list(indexes.values()) else None, eachTuple)))))
    
    for each in att_column_data[0]:
        indexes[each[1]] = att_column_data[0].index(each)

    for index, each in enumerate(att_column_data):
        att_column_data[index] = [item[0] for item in each]

    # remove duplicates from cumulative result set, i.e. [[tuple0], [tuple1], ... , [tupleN]]
    result = []
    if len(attList) == 1:
        result = list(collections.OrderedDict.fromkeys(list(map(lambda a: a[0], att_column_data))))
        result = list(map(lambda a: [a],result))
    else:
        # handle multiple columns differently
        result = att_column_data

    

    # shove result into respective page files (create folders if necessary)
    rel_path = os.path.join(os.path.dirname(__file__),"../data/")
    file_name = "project_"+rel+"_"+"_".join(attList)
    if len(glob.glob(rel_path + file_name + "_*")) != 0:
        num = int(sorted(glob.glob(rel_path + file_name + "_[0-9]*"))[-1].split('/')[-1].split('_')[-1])
        file_name = file_name + "_" + str(num + 1)
    else:
        file_name = file_name + "_0"
    rel_path = rel_path + file_name
    os.mkdir(rel_path)
         
    # insert schema entry
    content = open(os.path.join(os.path.dirname(__file__), "../data/schemas.txt"), 'r+')
    schemas_list = json.loads(content.read())
    
    new_schema = []
    for eachAtt in attList:
        new_schema.append(list(filter(lambda x : x != None, list(map(lambda a: [file_name, eachAtt, a[2], indexes[eachAtt]] if (
            a[0] == rel and a[1] == eachAtt) else None, schemas_list))))[0])

    schemas_list.extend(new_schema)
    content.seek(0)
    content.truncate(0)
    content.write(json.dumps(schemas_list))
    content.close()

    # Write to individual pages
    pageLink = []
    length = math.ceil(len(result)/2)
    for i in range(length):
        temp = result[:2]
        result = list(filter(lambda a: a not in temp,result))
        page0 = page_pool_list[0]
        pageLink.append(page0)
        page_pool_list.remove(page0)
        f = open(rel_path + "/" + page0, 'w+')
        f.write(json.dumps(temp))
        f.close()

    # Write to pageLink
    with open(rel_path + "/pageLink.txt" , "w+") as content:
        content.write(json.dumps(pageLink))


    # rewrite page pool list
    with open(os.path.join(os.path.dirname(__file__), "../data/pagePool.txt"),"w") as pagePoolFile:
        pagePoolFile.write(json.dumps(page_pool_list))

    return file_name

def join(rel1, att1, rel2, att2):
    # individual costs for calculation
    cost_rel1_att1_b = 0
    cost_rel1_att1 = 0
    cost_rel2_att2_b = 0
    cost_rel2_att2 = 0

    rel1_data = [] # populate this either sequentially or using b+ tree
    # check if B+ tree exists on rel1_att1 or rel2_att2 and use it
    if os.path.isfile(os.path.join(os.path.dirname(__file__), "../treePic/"+rel1+"_"+att1+".txt")):
        # print("b+ tree for given attribs already exists")
        tree = open(os.path.join(os.path.dirname(__file__), "../treePic/"+rel1+"_"+att1+".txt"),"r")
        tree_json = json.loads(tree.read())
        root_key = list(filter(lambda a: a if tree_json[a][1] == "nil" else None, tree_json.keys()))[0]
        cost_rel1_att1_b = cost_rel1_att1_b + 1
        key = root_key
        while tree_json[key][0] != "L":
            key = tree_json[key][2][-1]
            cost_rel1_att1_b = cost_rel1_att1_b + 1

        # now in the end the key is on the right most leaf of the tree (because I calculated it that way)
        left_key = key
        while tree_json[left_key][2] != "nil":
            for each in tree_json[left_key][4][1::2]:
                for item in each:
                    fragments = item.split('.')
                    fetchedDataFile = fragments[0]+"."+fragments[1]
                    dataFileIndex = int(fragments[2])
                    openDataFile = open(os.path.join(os.path.dirname(__file__), "../data/" + rel1 + "/" + fetchedDataFile),"r")
                    dataTuple = json.loads(openDataFile.read())
                    cost_rel1_att1_b = cost_rel1_att1_b + 1
                    rel1_data.append(dataTuple[dataFileIndex])
            left_key = tree_json[left_key][2]
            cost_rel1_att1_b = cost_rel1_att1_b + 1
        
        for each in tree_json[left_key][4][1::2]:
            for item in each:
                fragments = item.split('.')
                fetchedDataFile = fragments[0]+"."+fragments[1]
                dataFileIndex = int(fragments[2])
                openDataFile = open(os.path.join(os.path.dirname(__file__), "../data/" + rel1 + "/" + fetchedDataFile),"r")
                dataTuple = json.loads(openDataFile.read())
                cost_rel1_att1_b = cost_rel1_att1_b + 1
                rel1_data.append(dataTuple[dataFileIndex])
    else:
        # fetch all tuples in rel1
        path = "../data/" + rel1 + "/"
        content = open(os.path.join(os.path.dirname(__file__), path + "pageLink.txt"), 'r')
        rel_page_link_list = json.loads(content.read())
        cost_rel1_att1 = len(rel_page_link_list)
        content.close()
        for item in rel_page_link_list:
            content = open(os.path.join(os.path.dirname(__file__), path + item), 'r')
            tuples_in_file = json.loads(content.read())
            content.close()
            for eachTuple in tuples_in_file:
                rel1_data.append(eachTuple)

    rel2_data = [] # populate this either sequentially or using b+ tree
    if os.path.isfile(os.path.join(os.path.dirname(__file__), "../treePic/"+rel2+"_"+att2+".txt")):
        # print("b+ tree for given attribs already exists")
        tree = open(os.path.join(os.path.dirname(__file__), "../treePic/"+rel2+"_"+att2+".txt"),"r")
        tree_json = json.loads(tree.read())
        root_key = list(filter(lambda a: a if tree_json[a][1] == "nil" else None, tree_json.keys()))[0]
        cost_rel2_att2_b = cost_rel2_att2_b + 1
        key = root_key
        while tree_json[key][0] != "L":
            key = tree_json[key][2][-1]
            cost_rel2_att2_b = cost_rel2_att2_b + 1

        # now in the end the key is on the right most leaf of the tree (because I calculated it that way)
        left_key = key
        while tree_json[left_key][2] != "nil":
            for each in tree_json[left_key][4][1::2]:
                for item in each:
                    fragments = item.split('.')
                    fetchedDataFile = fragments[0]+"."+fragments[1]
                    dataFileIndex = int(fragments[2])
                    openDataFile = open(os.path.join(os.path.dirname(__file__), "../data/" + rel2 + "/" + fetchedDataFile),"r")
                    dataTuple = json.loads(openDataFile.read())
                    cost_rel2_att2_b = cost_rel2_att2_b + 1
                    rel2_data.append(dataTuple[dataFileIndex])
            left_key = tree_json[left_key][2]
            cost_rel2_att2_b = cost_rel2_att2_b + 1
        
        for each in tree_json[left_key][4][1::2]:
            for item in each:
                fragments = item.split('.')
                fetchedDataFile = fragments[0]+"."+fragments[1]
                dataFileIndex = int(fragments[2])
                openDataFile = open(os.path.join(os.path.dirname(__file__), "../data/" + rel2 + "/" + fetchedDataFile),"r")
                dataTuple = json.loads(openDataFile.read())
                cost_rel2_att2_b = cost_rel2_att2_b + 1
                rel2_data.append(dataTuple[dataFileIndex])
    else:
        # fetch all tuples in rel2 sequentially
        path = "../data/" + rel2 + "/"
        content = open(os.path.join(os.path.dirname(__file__), path + "pageLink.txt"), 'r')
        rel_page_link_list = json.loads(content.read())
        cost_rel2_att2 = len(rel_page_link_list)
        content.close()
        for item in rel_page_link_list:
            content = open(os.path.join(os.path.dirname(__file__), path + item), 'r')
            tuples_in_file = json.loads(content.read())
            content.close()
            for eachTuple in tuples_in_file:
                rel2_data.append(eachTuple)

    total_cost = 0
    if cost_rel1_att1_b == 0 and cost_rel2_att2_b == 0:
        total_cost = cost_rel1_att1 * cost_rel2_att2
        print("In a join, Without B+ Tree the total cost is "+str(total_cost)+" pages")
    elif cost_rel1_att1_b != 0 and cost_rel2_att2_b == 0:
        total_cost = cost_rel1_att1_b + cost_rel2_att2
        print("In a join, With B+ tree on " + rel1 + " with " + att1 + ", the cost is " + str(total_cost) + " pages")
    elif cost_rel1_att1_b == 0 and cost_rel2_att2_b != 0:
        total_cost = cost_rel1_att1 + cost_rel2_att2_b
        print("In a join, With B+ tree on " + rel2 + " with " + att2 + ", the cost is " + str(total_cost) + " pages")
    else:
        total_cost = cost_rel1_att1_b + cost_rel2_att2_b
        print("In a join, With B+ tree on " + rel1 + " with " + att1 + " and also on " + rel2 + " with " + val2 + ", the cost is " + str(total_cost) + " pages")

    # Import page pool
    content = open(os.path.join(os.path.dirname(__file__), "../data/pagePool.txt"), 'r')
    page_pool_list = json.loads(content.read())
    content.close()

    # fetch the index of att1 and att2
    content = open(os.path.join(os.path.dirname(__file__), "../data/schemas.txt"), 'r')
    schemas_list = json.loads(content.read())
    content.close()
    
    index_rel1_att1 = list(filter(lambda x : x != None, list(map(lambda a: a[3] if (
        a[0] == rel1 and a[1] == att1) else None, schemas_list))))[0]

    index_rel2_att2 = list(filter(lambda x : x != None, list(map(lambda a: a[3] if (
        a[0] == rel2 and a[1] == att2) else None, schemas_list))))[0]

    # store all attributes to create a schema and push it into the schema file

    # write logic to filter out equalized tuples and shove them into a result list
    result = []
    for eachTuple in rel1_data:
        result.extend(list(filter(lambda a: a != None, list(map(lambda rel2_tuple: list(collections.OrderedDict.fromkeys(eachTuple + rel2_tuple)) if eachTuple[index_rel1_att1] == rel2_tuple[index_rel2_att2] else None , rel2_data)))))

    # main join answer
    result = list(filter(lambda a: a != [], result))

    # shove result into respective page files (create folders if necessary)
    rel_path = os.path.join(os.path.dirname(__file__), "../data/")
    file_name = "join_"+rel1+"_"+att1+"_"+rel2+"_"+att2
    if len(glob.glob(rel_path + file_name + "_*")) != 0:
        num = int(sorted(glob.glob(rel_path + file_name + "_[0-9]*"))[-1].split('/')[-1].split('_')[-1])
        file_name = file_name + "_" + str(num + 1)
    else:
        file_name = file_name + "_0"
    rel_path = rel_path + file_name
    os.mkdir(rel_path)
    
    # write to schemas table too
    content = open(os.path.join(os.path.dirname(__file__), "../data/schemas.txt"), 'r+')
    schemas_list = json.loads(content.read())
    new_schema = list(filter(lambda x : x != None, list(map(lambda a: [file_name, a[1], a[2], a[3]] if (
        a[0] == rel1) else None, schemas_list)))) # for rel1 it is constant

    secondary_column_schema = list(filter(lambda x : x != None, list(map(lambda a: [file_name, a[1], a[2], len(new_schema) + (a[3]-1 if a[3] > index_rel2_att2 else a[3])] if (
        a[0] == rel2 and a[1] != att2) else None, schemas_list))))

    new_schema.extend(secondary_column_schema)
    schemas_list.extend(new_schema)
    content.seek(0)
    content.truncate(0)
    content.write(json.dumps(schemas_list))
    content.close()

    pageLink = []
    length = math.ceil(len(result)/2)
    for i in range(length):
        temp = result[:2]
        result = list(filter(lambda a: a not in temp,result))
        page0 = page_pool_list[0]
        pageLink.append(page0)
        page_pool_list.remove(page0)
        f = open((rel_path + "/" + page0), 'w+')
        f.write(json.dumps(temp))
        f.close()

    # # Write to pageLink
    with open(rel_path + "/pageLink.txt" , "w+") as content:
        content.write(json.dumps(pageLink))

    # # rewrite page pool list
    with open(os.path.join(os.path.dirname(__file__), "../data/pagePool.txt"),"w") as pagePoolFile:
        pagePoolFile.write(json.dumps(page_pool_list))

    return file_name

# project("Supply",["sid"])
# join("Suppliers", "sid", "Supply", "sid")
# select("Suppliers", "sname", "=", "Brown")