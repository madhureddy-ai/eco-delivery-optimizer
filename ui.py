import gradio as gr
import requests

def reset():
    res = requests.post("/reset", json={"task": "easy"})
    return res.json()

def move(direction):
    res = requests.post("/step", json={"move": direction})
    return res.json()

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