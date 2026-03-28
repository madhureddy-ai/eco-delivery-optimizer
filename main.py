from fastapi import FastAPI
from pydantic import BaseModel
from environment import Env
from grader import Grader

app = FastAPI()

env = Env()
grader = Grader()


class Action(BaseModel):
    move: str


@app.get("/")
def home():
    return {"message": "Warehouse Delivery Optimization API is running"}


@app.post("/reset")
def reset(data: dict):
    task = data.get("task", "easy")
    state = env.reset(task)
    grader.reset()
    return {"state": state}


@app.post("/step")
def step(action: Action):
    result = env.step(action.dict())
    grader.update(result)
    return result


@app.get("/state")
def state():
    return env.state()


@app.get("/tasks")
def tasks():
    return ["easy", "medium", "hard"]


@app.get("/grader")
def get_score():
    return {"score": grader.get_score()}