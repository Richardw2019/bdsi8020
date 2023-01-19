from typing import Union

from fastapi import FastAPI

from pydantic import BaseModel

from fastapi import File, UploadFile

import json




app = FastAPI()


class Item(BaseModel):
    id: int = "id"
    name: str = "your name"
    research_focus: str = "your research focus"
    hobbies: list = ["hobby1", "hobby2", "hobby3"]
    spirit_animal: dict = {"animal-type": "type", "special-power": "power", "favorite-food": "food" }


# @app.get("/")
# def read_root():
#     return {"Hello": "World"}


@app.post("/saveToFile")
def post_info(item: Item):
    with open('test.json', mode='a') as myfile:
        myfile.truncate(0)
        return myfile.write(item.json())

    

@app.get("/readFromFile")
def read_info():
    f = open('test.json')
    data = json.load(f)
    
    return data



   

# class Item(BaseModel):
#     name: str
#     price: float
#     is_offer: Union[bool, None] = None


# @app.get("/")
# def read_root():
#     return {"Hello": "World"}


# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: Union[str, None] = None):
#     return {"item_id": item_id, "q": q}


# @app.put("/items/{item_id}")
# def update_item(item_id: int, item: Item):
#     return {"item_name": item.name, "item_id": item_id}