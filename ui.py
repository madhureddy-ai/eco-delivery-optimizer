import gradio as gr
from environment import Env
from grader import Grader

env = Env()
grader = Grader()

# GRID
def render_grid(state, size=5):
    grid = [["⬜" for _ in range(size)] for _ in range(size)]

    ax, ay = state["position"]
    grid[ax][ay] = "🚗"

    for dx, dy in state["deliveries_left"]:
        if grid[dx][dy] == "🚗":
            grid[dx][dy] = "🚗📦"
        else:
            grid[dx][dy] = "📦"

    return "\n".join([" ".join(row) for row in grid])


# OUTPUT
def format_output(result):
    state = result["state"]
    grid = render_grid(state)

    fuel_used = max(1, (20 - state["fuel"]))
    efficiency = result["reward"] / fuel_used

    return (
        f"{grid}\n\n"
        f"🚗 Position: {state['position']}\n"
        f"⛽ Energy: {state['fuel']}\n"
        f"📦 Deliveries Left: {len(state['deliveries_left'])}\n"
        f"💰 Cost Savings: {round(result['reward'],2)}\n"
        f"⚡ Efficiency: {round(efficiency,2)}\n"
        f"🏁 Done: {result['done']}"
    )


def reset():
    state = env.reset("easy")
    grader.reset()
    return format_output({
        "state": state,
        "reward": 0,
        "done": False
    })


def move(direction):
    result = env.step({"move": direction})
    grader.update(result)
    return format_output(result)


# AUTO AGENT
def auto_move():
    state = env.state()
    ax, ay = state["position"]

    deliveries = state["deliveries_left"]
    if not deliveries:
        return format_output({
            "state": state,
            "reward": 0,
            "done": True
        })

    target = min(deliveries, key=lambda d: abs(d[0]-ax) + abs(d[1]-ay))
    tx, ty = target

    if ax < tx:
        direction = "down"
    elif ax > tx:
        direction = "up"
    elif ay < ty:
        direction = "right"
    else:
        direction = "left"

    result = env.step({"move": direction})
    grader.update(result)
    return format_output(result)


with gr.Blocks() as demo:
    gr.Markdown("# 🚀 AI-Powered Warehouse Delivery Optimization System")

    output = gr.Textbox(lines=15, label="Live Simulation")

    gr.Button("🔄 Reset").click(reset, outputs=output)

    with gr.Row():
        gr.Button("⬆ Up").click(lambda: move("up"), outputs=output)
        gr.Button("⬇ Down").click(lambda: move("down"), outputs=output)
        gr.Button("⬅ Left").click(lambda: move("left"), outputs=output)
        gr.Button("➡ Right").click(lambda: move("right"), outputs=output)

    gr.Button("🤖 Run Auto-Agent").click(auto_move, outputs=output)