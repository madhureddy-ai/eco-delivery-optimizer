from fastapi import FastAPI
from pydantic import BaseModel
from environment import Env
from tasks import TASKS
from grader import Grader

app = FastAPI()

env = Env()
grader = Grader()


class Action(BaseModel):
    move: str


@app.get("/")
def home():
    return {"msg": "working"}


@app.post("/reset")
def reset(data: dict):
    task = data.get("task", "easy")
    state = env.reset(task)
    grader.reset()
    return state


@app.post("/step")
def step(action: Action):
    result = env.step(action.dict())
    grader.update(result)
    return result


@app.get("/grader")
def get_score():
    return {"score": grader.get_score()}


@app.get("/tasks")
def get_tasks():
    return ["easy", "medium", "hard"]


@app.get("/baseline")
def baseline():
    return {"message": "Run baseline.py locally to see scores"}