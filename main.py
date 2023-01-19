from typing import Union

from fastapi import FastAPI

from pydantic import BaseModel

from fastapi import File, UploadFile

import json




app = FastAPI()


class Item(BaseModel):
    id: str = "id"
    name: str = "your name"
    research_focus: str = "your research focus"
    hobbies: list = ["hobby1", "hobby2", "hobby3"]
    spirit_animal: dict = {"animal-type": "type", "special-power": "power", "favorite-food": "food" }





@app.post("/saveToFile")
def post_info(item: Item):
    with open('test.json', mode='a') as myfile:
        myfile.truncate(0)
        myfile.write(item.json())
    return item

    

@app.get("/readFromFile")
def read_info():
    f = open('test.json')
    data = json.load(f) 
    return data