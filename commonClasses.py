from  pydantic import BaseModel
class CreateFolder(BaseModel):
    folderName: str

class FileClass:
    url = ""
    def __init__(self, title, isFolder):
        self.title = title
        self.isFolder = isFolder

class UserCreate(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str