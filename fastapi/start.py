from enum import Enum
from typing import Optional, List
from fastapi import FastAPI, Form, File, UploadFile
from fastapi.responses import HTMLResponse
import os 

class ModelName(str,Enum):
    alexnet="alexnet"
    resnet="resnet"
    lenet="lenet"
app = FastAPI()
fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]

@app.get("/")
async def main():
    content = """
    <body>
    <form action="/files/" enctype="multipart/form-data" method="post">
    <input name="files" type="file" multiple>
    <input type="submit">
    </form>
    <form action="/uploadfile/" enctype="multipart/form-data" method="post">
    <input name="files" type="file" multiple>
    <input type="submit">
    </form>
    </body>
    """
    return HTMLResponse(content=content)

@app.get("/")
async def root():
    return {"message":"hello, world!"}

@app.get("/items/")
async def read_item(skip: int = 0, limit: int = 10):
    return fake_items_db[skip : skip + limit]

#{item_id} : path_parameter 
@app.get("/items/{item_id}")
async def read_item(item_id: str, q: Optional[str] = None):
    if q:
        return {"item_id": item_id, "q": q}
    return {"item_id": item_id}

@app.get("/models/{model_name}")
async def get_model(model_name:ModelName):
    if model_name == ModelName.alexnet:
        return {"model_name":model_name, "message":"Deep Learning FTW!"}
    if model_name.value == "lenet":
        return {"model_name":model_name,"message":"LeCNN all the images"}
    return {"model_name": model_name, "message": "Have some residuals"}

@app.post("/login/")
async def login(username: str = Form(...), password: str = Form(...)):
    return {"username": username}

@app.post("/files/")
async def create_files(files: List[bytes] = File(...)):
    return {"file_sizes": [len(file) for file in files]}

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
    content = await file.read()
    with open(os.path.join("./", file.filename), "wb") as fp:
        fp.write(content)    
    return {"filename": file.filename}

@app.post("/uploadfiles/")
async def create_upload_files(files: List[UploadFile] = File(...)):
    return {"filenames": [file.filename for file in files]}
