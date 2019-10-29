import json

def read_from_file_to_list(path):
    content = open(path, 'r')
    content_list = json.loads(content.read())
    content.close()
    return content_list