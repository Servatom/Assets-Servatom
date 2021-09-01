from fastapi import FastAPI, Depends, Request, File, UploadFile, HTTPException, status
from fastapi.responses import FileResponse
import aiofiles
from fastapi.templating import Jinja2Templates
import os
from getAllFiles import *
import shutil
from commonClasses import *
from security import *
import models.models as models
from sqlalchemy.orm import Session
from models.database import SessionLocal, engine

from models.models import UserModel
import models.models as models
from models.database import SessionLocal, engine


app = FastAPI()

domain = "https://assets.servatom.com"
parent = "assets"

templates = Jinja2Templates(directory="templates/")

models.Base.metadata.create_all(bind=engine)


def get_db():
    try :
        db = SessionLocal()
        yield db
    finally:
        db.close()

@app.get("/")
def index(req: Request):
    files = getFiles(parent)
    all_files = []
    # add the domain name to each file
    for file in files:
        file.url = domain + "/" + file.title
        all_files.append(file)
    #return all_files
    return templates.TemplateResponse("index.html", {"items": all_files, "request": req})

@app.get("/{param:path}")
def getFile(param: str, req: Request):
    if param == "favicon.ico": # web browser issue
        print("Error ignored")
        return
    param = param.rstrip("/")
    file = parent + "/" + param
    print(file)

    # if the file is a directory give the list of files in the directory else return the file

    if os.path.isdir(file):
        files = getFiles(file)
        all_files = []
        # add the domain name to each file
        for i in files:
            i.url = "https://assets.servatom.com/" + param + "/" + i.title
            all_files.append(i)

        #return templates.TemplateResponse("index.html", {"items": all_files, "request": req})
        
        return all_files
    else:
        return FileResponse(file)

# Post requests
@app.post("/upload/{param:path}")
def uploadFile(param: str, file: UploadFile = File(...), user=Depends(get_current_user)):
    # remove spaces from teh filename
    filename = param.replace(" ", "")
    fileStore = parent + "/" + param + "/" + file.filename
    # store file in the folder
    # check if file is there
    if os.path.isfile(fileStore):
        return "File already exists"
    else:
        with open(fileStore, "wb") as f:
            f.write(file.file.read())
        return "File uploaded"


# create folder
@app.post("/create/{param:path}")
def createFolder(param: str, folder_Req: CreateFolder, user=Depends(get_current_user)):
    # get folder name from the body json file
    folder = folder_Req.folderName
    # check if the folder already exists
    if os.path.isdir(parent + "/" + param + "/" + folder):
        # send folder already exists with status
        return {"message": "Folder already exists"}

    # create folder
    os.mkdir(parent + "/" + param + "/" + folder)
    return {"message": f"Folder created at => {param}/{folder_Req.folderName}"}

# delete file
@app.delete("/delete/{param:path}")
def deleteFile(param: str, req: Request, user=Depends(get_current_user)):
    # get file name from the body json file
    file = param
    # check if the file exists
    if os.path.isfile(parent + "/" + param):
        # delete the file
        os.remove(parent + "/" + param)
        return {"message": f"File deleted at => {param}"}
    elif os.path.isdir(parent + "/" + param):
        # delete the folder
        shutil.rmtree(parent + "/" + param)
        return {"message": f"Folder deleted at => {param}"}
    else:
        return {"message": f"File not found at => {param}"} 


# Security crap
@app.post('/signup')
def signup(user_req: UserCreate, db: Session = Depends(get_db)):
    # has passwd
    # get number of users
    users = db.query(UserModel).count()
    if users == 1:
        return {"message": "Maximum users reached"}
    try:
        user = UserModel(username=user_req.username, password=hashMe(user_req.password))
        db.add(user)
        db.commit()
        return {"status": "user_created"}
    except:
        return {"status": "user_exists"}


@app.post('/login')
def login(user_req: UserLogin, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter_by(username=user_req.username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if not verify_passwd(user_req.password, user.password):
        raise HTTPException(status_code=401, detail="Incorrect creds")
    

    access_token = create_access_token(user.username)
    return {"access_token": access_token, "type": "bearer"}
