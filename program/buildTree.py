import ast, random


def build(rel, att, od):
    # Import page pool
    page_pool = open('data.txt', 'r')
    page_pool_list = ast.literal_eval(page_pool.read())
    
    # Create tree JSON variable
    b_plus_tree = {}
    
    # Ensure that proper path for the desired rel_att is fetched
    
    # Import the column on which index is to be made

    # Pick page to write to from the page pool
    selected_page = random.choice(page_pool_list)
    
    # Remove from the page pool list
    page_pool_list.remove(selected_page)

    # Create node in the selected page variable

    # LOOP : Check conditions and append to Tree JSON variable (IMPORTANT)

    # LOOP : Create the separate page file in the index folder, keep on doing it until you exhaust the entire Tree Variable (as it is completely built by now)

    # LOOP : Write Tree variable in treePic Folder.

    # Write page pool list back to file
    return
