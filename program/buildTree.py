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
    index = list(map(lambda a: a[3] if (a[0] == rel and a[1] == att) else 0, schemas_list))[0]

    # Import the column on which index is to be made
    column_data = [att]
    rel_page_link_list = helper.read_from_file_to_list(path + "pageLink.txt")
    for item in rel_page_link_list:
        tuples_in_file = helper.read_from_file_to_list(path + item)
        for eachTuple in tuples_in_file:
            column_data.append(eachTuple[index])

    # Pick page to write to from the page pool
    # selected_page = random.choice(page_pool_list)

    # Remove from the page pool list
    # page_pool_list.remove(selected_page)

    # Create node in the selected page variable

    # LOOP : Check conditions and append to Tree JSON variable (IMPORTANT)

    # LOOP : Create the separate page file in the index folder, keep on doing it until you exhaust the entire Tree Variable (as it is completely built by now)

    # LOOP : Write Tree variable in treePic Folder.

    # Write page pool list back to file
    return
    
