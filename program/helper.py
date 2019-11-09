import json
import os
def read_from_file_to_list(path):
    cwd = os.getcwd()
    content = open(cwd + path, 'r')
    content_list = json.loads(content.read())
    content.close()
    return content_list