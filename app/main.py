﻿from fastapi import FastAPI

app = FastAPI()


@app.get("/hotels")
def get_hotels():
    return "Отель Лагуна Бридж 5*"
