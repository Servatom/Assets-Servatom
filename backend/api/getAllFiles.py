import os

url = os.getenv('API_URL')
class FileClass:
    url = ""
    def __init__(self, title, isFolder):
        self.title = title
        self.isFolder = isFolder
    
    def serialize(self):
        return {
            'url': url + self.title,
            'isFolder': self.isFolder
        }

def getFiles(directory):
    # get all immediate sub directories and files in the directory
    items = []
    for name in os.listdir(directory):
        if os.path.isdir(os.path.join(directory, name)):
            # replace / with % in name
            items.append(FileClass(name, isFolder=True))
        else:
            items.append(FileClass(name, isFolder=False))
    result = []
    for item in items:
        result.append(item.serialize())
    return result
