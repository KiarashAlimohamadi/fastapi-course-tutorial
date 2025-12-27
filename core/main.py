from fastapi import FastAPI,status,HTTPException
from typing import Optional
import string
from fastapi.responses import JSONResponse


app = FastAPI()


names_list = [
    {"id":1,"name":"kiarash"},
    {"id":2,"name":"hadi"},
    {"id":3,"name":"fatemeh"},
    {"id":4,"name":"ayeen"},
    {"id":5,"name":"shadkam"},
]



@app.get('/')
def index():
    return JSONResponse(content={
        "message":"Hello World!"
    },status_code=status.HTTP_200_OK)





@app.post('/names',status_code=status.HTTP_201_CREATED)
def create_name(name:str):
    last_name = names_list[-1]
    id = int(last_name["id"]) + 1
    name_obj = {"id":id,"name":name}
    names_list.append(name_obj)
    return name_obj



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
