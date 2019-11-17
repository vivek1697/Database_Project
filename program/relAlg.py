import ast
import random
import math
import os
import json
import collections
import glob

def select(rel, att, op, val):
	# Import page pool
    content = open(os.path.join(os.path.dirname(__file__), "../data/pagePool.txt"), 'r')
    page_pool_list = json.loads(content.read())
    content.close()

  	# Ensure that proper path for the desired rel_att is fetched
    path = "/data/" + rel + "/"

    # fetch relation schemas
    schemas_list = helper.read_from_file_to_list("/data/schemas.txt")
    index = list(map(lambda a: a[3] if (
        a[0] == rel and a[1] == att) else 0, schemas_list))[0]

    # Import the column on which index is to be made
    att_column_data = []
    rel_page_link_list = helper.read_from_file_to_list(path + "pageLink.txt")
    for item in rel_page_link_list:
        tuples_in_file = helper.read_from_file_to_list(path + item)
        for eachTuple in tuples_in_file:
            att_column_data.append(eachTuple[index])
    
    #Handle cases for 6 operators
    selection_result = []
    for item in att_column_data:
        if op == "=":
            if item == val:
                selection_result.append(item)
        elif op == ">":
            if item > val:
                selection_result.append(item)
        elif op == ">=":
            if item >= val:
                selection_result.append(item)
        elif op == "<":
            if item < val:
                selection_result.append(item)
        elif op == "<=":
            if item <= val:
                selection_result.append(item)
        elif op == "!=":
            if item != val:
                selection_result.append(item)   
    
    #Read value from result and print to pages
    list_length = len(selection_result)
    total_range = math.ceil(list_length/2)
    for i in range(total_range-1):
        selected_page = random.choice(page_pool_list)
        page_pool_list.remove(selected_page)
        temp = selection_result[:2]
        final_result = list(map(lambda x: [x], temp))
        for item in temp:
            selection_result.remove(item)
            #TODO need to complete code to write values in selected page
            f = open(selected_page, "w")
            f.write(str(final_result))
            f.close()
    return   

    


    
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
        num = int(sorted(glob.glob(rel_path + file_name + "_*"))[-1].split('/')[-1].split('_')[-1])
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
    # check if B+ tree exists on rel1_att1 or rel2_att2 and use it

    # Import page pool
    content = open(os.path.join(os.path.dirname(__file__), "../data/pagePool.txt"), 'r')
    page_pool_list = json.loads(content.read())
    content.close()

    # fetch all tuples in rel1
    path = "../data/" + rel1 + "/"
    rel1_data = []
    content = open(os.path.join(os.path.dirname(__file__), path + "pageLink.txt"), 'r')
    rel_page_link_list = json.loads(content.read())
    content.close()
    for item in rel_page_link_list:
        content = open(os.path.join(os.path.dirname(__file__), path + item), 'r')
        tuples_in_file = json.loads(content.read())
        content.close()
        for eachTuple in tuples_in_file:
            rel1_data.append(eachTuple)

    # fetch all tuples in rel2
    path = "../data/" + rel2 + "/"
    rel2_data = []
    content = open(os.path.join(os.path.dirname(__file__), path + "pageLink.txt"), 'r')
    rel_page_link_list = json.loads(content.read())
    content.close()
    for item in rel_page_link_list:
        content = open(os.path.join(os.path.dirname(__file__), path + item), 'r')
        tuples_in_file = json.loads(content.read())
        content.close()
        for eachTuple in tuples_in_file:
            rel2_data.append(eachTuple)

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
        num = int(sorted(glob.glob(rel_path + file_name + "_*"))[-1].split('/')[-1].split('_')[-1])
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
# join("Products", "pid", "Supply", "pid")
# select("Suppliers", "sid", "<", "s04")