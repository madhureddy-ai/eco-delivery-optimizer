import gradio as gr
from environment import Env
from grader import Grader

env = Env()
grader = Grader()


def format_output(result):
    state = result["state"]
    return f"""
### 📍 Position: {state['position']}
### ⛽ Fuel: {state['fuel']}
### 📦 Deliveries Left: {len(state['deliveries_left'])}

### 🎯 Reward: {result['reward']}
### 🏁 Done: {result['done']}
"""

#  RESET
def reset():
    state = env.reset("easy")
    grader.reset()
    return format_output({
        "state": state,
        "reward": 0,
        "done": False
    })

#  MOVE
def move(direction):
    result = env.step({"move": direction})
    grader.update(result)
    return format_output(result)

#  UI
with gr.Blocks() as demo:
    gr.Markdown("# 🚀 Warehouse Delivery Optimization Environment (OpenEnv)")

    output = gr.Markdown()

    gr.Button("Reset").click(reset, outputs=output)

    with gr.Row():
        gr.Button("Up").click(lambda: move("up"), outputs=output)
        gr.Button("Down").click(lambda: move("down"), outputs=output)
        gr.Button("Left").click(lambda: move("left"), outputs=output)
        gr.Button("Right").click(lambda: move("right"), outputs=output)

demo.launch()