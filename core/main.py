from fileinput import filename
from typing import List
from fastapi import FastAPI,status,HTTPException,Form,Body,File,UploadFile
from typing import Optional
import string
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from dataclasses import dataclass

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("app startup")

    yield

    print("app shoutdown")


app = FastAPI(lifespan=lifespan)




names_list = [
    {"id":1,"name":"kiarash"},
    {"id":2,"name":"hadi"},
    {"id":3,"name":"fatemeh"},
    {"id":4,"name":"ayeen"},
    {"id":5,"name":"shadkam"},
]

@app.on_event("startup")
async def startup_event():
    names_list[0]["name"] = "paya"


@app.get('/')
def index():
    return JSONResponse(content={
        "message":"Hello World!"
    },status_code=status.HTTP_200_OK)


@dataclass
class Student:
    name:str
    age:int


@app.post('/names',status_code=status.HTTP_201_CREATED)
#def create_name(name:str=Body()):
def create_name(Student:Student=Body()):
    last_name = names_list[-1]
    id = int(last_name["id"]) + 1
    name_obj = {"id":id,"name":Student.name}
    names_list.append(name_obj)
    return JSONResponse(content=
                        {"name":Student.name,
                        "age":Student.age}
                        )



@app.put("/names/{name_id}",status_code=status.HTTP_204_NO_CONTENT)
def update_name(name_id:int,new_name):
    for name in names_list:
        if int(name["id"]) == int(name_id):
            name["name"] = new_name
            return name
    return "object not found"



@app.get("/names",status_code=status.HTTP_200_OK)
def names():
    return names_list


@app.get("/names/{name_id}",status_code=status.HTTP_200_OK)
def name_detail(name_id:int):
    for name in names_list:
        if int(name["id"]) == int(name_id):
            return name
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="object not found")


@app.post("/upload_file")
async def upload_file(file:UploadFile):
    content = await file.read()
    return JSONResponse(content=
                        {"filename":file.filename,
                         "content_type":file.content_type,
                         "file_size":len(content)})

@app.post("/upload-multiple")
async def upload_multiple(files:List[UploadFile]):
    return [
        {"filename": file.filename,
         "content_type": file.content_type,}
        for file in files
    ]
