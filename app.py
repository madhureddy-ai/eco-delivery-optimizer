from fastapi import FastAPI
import gradio as gr
from environment import Env
from grader import Grader

app = FastAPI()

env = Env()
grader = Grader()

# ---------- CORE LOGIC ----------

def format_output(result):
    state = result["state"]
    return {
        "position": state["position"],
        "fuel": state["fuel"],
        "deliveries_left": len(state["deliveries_left"]),
        "reward": result["reward"],
        "done": result["done"]
    }

# ---------- API ENDPOINTS (IMPORTANT) ----------

@app.post("/reset")
def reset_api(task: str = "easy"):
    state = env.reset(task)
    grader.reset()
    return format_output({
        "state": state,
        "reward": 0,
        "done": False
    })

@app.post("/step")
def step_api(action: dict):
    result = env.step(action)
    grader.update(result)
    return format_output(result)

@app.get("/tasks")
def get_tasks():
    return ["easy", "medium", "hard"]

# ---------- GRADIO UI ----------

def reset_ui(task):
    return str(reset_api(task))

def move_ui(direction):
    return str(step_api({"move": direction}))

with gr.Blocks() as demo:
    gr.Markdown("# Warehouse Delivery Optimization Environment (OpenEnv)")

    task_select = gr.Dropdown(
        ["easy", "medium", "hard"],
        value="easy",
        label="Select Task"
    )

    output = gr.Textbox(lines=10, label="Status")

    gr.Button("Reset").click(reset_ui, inputs=task_select, outputs=output)

    with gr.Row():
        gr.Button("Up").click(lambda: move_ui("up"), outputs=output)
        gr.Button("Down").click(lambda: move_ui("down"), outputs=output)
        gr.Button("Left").click(lambda: move_ui("left"), outputs=output)
        gr.Button("Right").click(lambda: move_ui("right"), outputs=output)

demo.launch()