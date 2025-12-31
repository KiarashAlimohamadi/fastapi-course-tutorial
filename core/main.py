#--------------IMPORTS---------------------------------------------------


from fileinput import filename
from typing import List
from fastapi import FastAPI,status,HTTPException,Form,Body,File,UploadFile,Depends
from typing import Optional
import string
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from dataclasses import dataclass
from pydantic import BaseModel,field_validator,Field,field_serializer
from database_test import Base,engine,User,get_db
from sqlalchemy.orm import Session

#-------------------------------------------------------------------------


#---------------------- LIFE SPAN -----------------------------------------

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("app startup")
    Base.metadata.create_all(engine)
    yield
    print("app shoutdown")

#---------------------------------------------------------------------------


#-------------------------------- START APP ---------------------------------

app = FastAPI(lifespan=lifespan)

#---------------------------------------------------------------------------


#----------------------------- THINK IT IS A DATA BASE :) ------------------

names_list = [
    {"id":1,"name":"kiarash"},
    {"id":2,"name":"hadi"},
    {"id":3,"name":"fatemeh"},
    {"id":4,"name":"ayeen"},
    {"id":5,"name":"shadkam"},
]
#---------------------------------------------------------------------------


#-------------------------------- SCHEMAS------------------------------------

"""
schemas
"""
class PersonCreateSchema(BaseModel):

    name:str = Field(default="default name",description="enter person's name")
    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str):
        if not value.replace(" ", "").isalpha():
            raise ValueError("name must contain only letters and spaces")
        return value.strip()

    @field_serializer("name")
    def serialize_name(self,value):
        return value.title()


class PersonResponseSchema(BaseModel):
    id: int
    name: str = Field(alias="first_name")

    class Config:
        from_attributes = True
        populate_by_name = True



#---------------------------------------------------------------------------


#------------------------------ FUNCTIONS -----------------------------------



@app.get('/')
def index():
    return JSONResponse(content={
        "message":"Hello World!"
    },status_code=status.HTTP_200_OK)


#@dataclass
#class Student:
#    name:str
#    age:int


@app.post('/names',status_code=status.HTTP_201_CREATED,response_model=PersonResponseSchema)
#def create_name(name:str=Body()):
def create_name(person:PersonCreateSchema,db:Session = Depends(get_db)):
    #last_name = names_list[-1]
    #id = int(last_name["id"]) + 1
    #name_obj = {"id":id,"name":person.name}
    #names_list.append(name_obj)
    #return name_obj
    new_user = User(first_name=person.name,age=40)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.put("/names/{name_id}",status_code=status.HTTP_204_NO_CONTENT)
def update_name(name_id:int,new_name):
    for name in names_list:
        if int(name["id"]) == int(name_id):
            name["name"] = new_name
            return name
    return "object not found"



@app.get("/names",status_code=status.HTTP_200_OK,response_model=List[PersonResponseSchema])
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


