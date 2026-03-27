import gradio as gr
from environment import Env
from grader import Grader

env = Env()
grader = Grader()

def reset():
    state = env.reset("easy")
    grader.reset()
    return state

def move(direction):
    result = env.step({"move": direction})
    grader.update(result)
    return result

with gr.Blocks() as demo:
    gr.Markdown("# 🚀 Warehouse Delivery Optimization Environment (OpenEnv)")

    state = gr.JSON()

    gr.Button("Reset").click(reset, outputs=state)

    with gr.Row():
        gr.Button("Up").click(lambda: move("up"), outputs=state)
        gr.Button("Down").click(lambda: move("down"), outputs=state)
        gr.Button("Left").click(lambda: move("left"), outputs=state)
        gr.Button("Right").click(lambda: move("right"), outputs=state)

demo.launch()