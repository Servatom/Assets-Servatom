import os
from commonClasses import FileClass

directory_parent = "/var/www/assets/"

def getFiles(directory):
    # get all immediate sub directories and files in the directory
    items = []
    for name in os.listdir(directory):
        if os.path.isdir(os.path.join(directory, name)):
            # replace / with % in name
            items.append(FileClass(name, isFolder=True))
        else:
            items.append(FileClass(name, isFolder=False))
    return items
