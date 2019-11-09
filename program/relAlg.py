import os, json, collections

def select(rel, att, op, val):
    return

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
            att_column_data.append(list(filter(lambda x: x != None,list(map(lambda a: a if eachTuple.index(a) in list(indexes.values()) else None, eachTuple)))))
    
    # remove duplicates from cumulative result set, i.e. [[tuple0], [tuple1], ... , [tupleN]]
    result = []
    if len(attList) == 1:
        result = list(collections.OrderedDict.fromkeys(list(map(lambda a: a[0], att_column_data))))
        result = list(map(lambda a: [a],result))
    else:
        # handle multiple columns differently
        result = att_column_data

        
    # shove result into respective page files (create folders if necessary)
    return

def join(rel1, att1, rel2, att2):
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

    # write logic to filter out equalized tuples and shove them into a result list
    result = []
    for eachTuple in rel1_data:
        result.extend(list(filter(lambda a: a != None, list(map(lambda rel2_tuple: list(collections.OrderedDict.fromkeys(eachTuple + rel2_tuple)) if eachTuple[index_rel1_att1] == rel2_tuple[index_rel2_att2] else None , rel2_data)))))

    # main join answer
    result = list(filter(lambda a: a != [], result))
    
    return

# project("Supply",["pid"])
# join("Products", "pid", "Supply", "pid")