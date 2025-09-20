readme = """
# LangGraph Ping-Pong State Machine

This project demonstrates a simple LangGraph-based state machine that loops between two nodes ("ping" and "pong") until a condition is met.

### What It Does:
- Starts at the "ping" node
- Alternates between "ping" and "pong"
- Stops when `count >= 6`
- Uses conditional edges and loop control with LangGraph

# """

with open("README.md", "w") as f:
  f.write(readme)
!cat README.md  # to preview

!pip install -q langgraph langchain openai

import os
from getpass import getpass
os.environ["OPENAI_API_KEY"] = getpass("Enter your OpenAI API Key: ")

from langgraph.graph import StateGraph

# Step 1: Define the state schema (can be just 'dict')
state_schema = dict

# Node A: Ping
def ping_node(state):
  count = state.get("count",0)
  print(f"Node A says: Ping (count = {count})")
  return {"count": count+1}

# Node B: Pong
def pong_node(state):
  count = state.get("count", 0)
  print(f"Node B says: Pong (count = {count})")
  return state

# End Node
def end_node(state):
  print("Reached end of graph!")
  return state

# Condition function: decide if we should stop or continue
def should_continue(state):
  if state["count"] >= 6:
    return "end"
  else:
    return "pong"

# Build the graph
builder = StateGraph(state_schema)
builder.add_node("ping", ping_node)
builder.add_node("pong", pong_node)
builder.add_node("end", end_node)

builder.set_entry_point("ping")

# Use a conditional edge from ping -> (pong or end)
builder.add_conditional_edges("ping", should_continue)

# Simulate edge pong -> ping (loop)
builder.add_edge("pong", "ping")

graph = builder.compile()
graph.invoke({"count":0})

