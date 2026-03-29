import gradio as gr
from fastapi import FastAPI
from pydantic import BaseModel

from environment import Env
from grader import Grader

env = Env()
grader = Grader()

# ---------------- API MODELS ----------------
class ResetRequest(BaseModel):
    task: str

class StepRequest(BaseModel):
    move: str

# ---------------- CORE LOGIC ----------------
def format_output(result):
    state = result["state"]
    return {
        "position": state["position"],
        "fuel": state["fuel"],
        "deliveries_left": len(state["deliveries_left"]),
        "reward": result["reward"],
        "done": result["done"]
    }

def reset_logic(task):
    state = env.reset(task)
    grader.reset()
    return format_output({
        "state": state,
        "reward": 0,
        "done": False
    })

def step_logic(move):
    result = env.step({"move": move})
    grader.update(result)
    return format_output(result)

# ---------------- FASTAPI ----------------
app = FastAPI()

@app.post("/reset")
def reset_api(req: ResetRequest):
    return reset_logic(req.task)

@app.post("/step")
def step_api(req: StepRequest):
    return step_logic(req.move)

# ---------------- GRADIO UI ----------------
def ui_reset(task):
    result = reset_logic(task)
    return str(result)

def ui_move(direction):
    result = step_logic(direction)
    return str(result)

with gr.Blocks() as demo:
    gr.Markdown("# Warehouse Delivery Optimization Environment (OpenEnv)")

    task_select = gr.Dropdown(
        ["easy", "medium", "hard"],
        value="easy",
        label="Select Task"
    )

    output = gr.Textbox(lines=10, label="Status")

    gr.Button("Reset").click(ui_reset, inputs=task_select, outputs=output)

    with gr.Row():
        gr.Button("Up").click(lambda: ui_move("up"), outputs=output)
        gr.Button("Down").click(lambda: ui_move("down"), outputs=output)
        gr.Button("Left").click(lambda: ui_move("left"), outputs=output)
        gr.Button("Right").click(lambda: ui_move("right"), outputs=output)

# ---------------- MOUNT ----------------
from gradio.routes import mount_gradio_app
app = mount_gradio_app(app, demo, path="/")