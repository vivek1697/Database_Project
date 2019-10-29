import json
import random
import functools
import helper


def build(rel, att, od):
    # Import page pool
    page_pool_list = helper.read_from_file_to_list("../index/pagePool.txt")

    # Create tree JSON variable
    b_plus_tree = {}

    # Ensure that proper path for the desired rel_att is fetched
    path = "../data/" + rel + "/"

    # fetch relation schemas
    schemas_list = helper.read_from_file_to_list("../data/schemas.txt")
    index = list(map(lambda a: a[3] if (
        a[0] == rel and a[1] == att) else 0, schemas_list))[0]

    # Import the column on which index is to be made
    att_column_data = []
    rel_page_link_list = helper.read_from_file_to_list(path + "pageLink.txt")
    for item in rel_page_link_list:
        tuples_in_file = helper.read_from_file_to_list(path + item)
        for eachTuple in tuples_in_file:
            att_column_data.append(eachTuple[index])

    # Create node in the selected page variable

    # LOOP : Check conditions and append to Tree JSON variable (IMPORTANT)
    for eachItem in att_column_data:
        # conditions for handling the tree
        if len(b_plus_tree.keys()) == 0:
            # create new root and insert a value in it
            created_root = select_random_page_from_page_pool_and_remove_from_list(
                page_pool_list)
            b_plus_tree[created_root] = ['I', 'nil', [select_random_page_from_page_pool_and_remove_from_list(
                page_pool_list), eachItem, select_random_page_from_page_pool_and_remove_from_list(page_pool_list)]]
        elif len(b_plus_tree.keys()) == 1:
            # insert in pre-existing root
            # fetch pre-existing root
            root = list(filter(lambda element: element[1][1] == 'nil', b_plus_tree.items()))[0]
            root_node_struct = root[1][3]
            if len(root_node_struct) is (2*(2*od) + 1): 
                # this is to check if the root node is filled or not; the formula denotes the total number of elements in the list depending on the order
                # remember the formula works like, for max total number of elements in 1 node is 2*od and the pointers is 2*d + 1 so the total length is 2*d + 2*d + 1
            else:
                # function to filter values and add to the list
                # remove all the odd index numbers from the node list
                for search_key_value in root_node_struct[1::2]: # fetch all odd elements from list; list[start;stop;step]
                    if eachItem < search_key_value:
                        # handle insert before the search key value
                    else:
                        # move on
                        continue


        else:
            # handle more cases for an already built tree

            # LOOP : Create the separate page file in the index folder, keep on doing it until you exhaust the entire Tree Variable (as it is completely built by now)

            # LOOP : Write Tree variable in treePic Folder.

            # Write page pool list back to file
    return


def select_random_page_from_page_pool_and_remove_from_list(page_pool_list_passed):
    # Pick page to write to from the page pool
    selected_page = random.choice(page_pool_list)
    # Remove from the page pool list
    page_pool_list_passed.remove(selected_page)
    return selected_page
