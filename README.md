# Warehouse Delivery Optimization Environment (OpenEnv)

## Description
This environment simulates a warehouse logistics system where an autonomous agent must optimize package deliveries under fuel and movement constraints.

The agent represents a warehouse worker or delivery robot navigating a grid-based warehouse to complete assigned delivery tasks efficiently.

## Real-World Motivation
Warehouse logistics is a real-world problem involving route optimization, resource management, and efficiency under constraints. This environment models simplified decision-making similar to real delivery systems used in logistics and supply chains.

## Features
- Package delivery simulation in a warehouse
- Fuel/resource constraints
- Multiple delivery objectives
- Efficiency-based reward system

## Tasks
- easy: Single package delivery with sufficient fuel
- medium: Multiple package deliveries requiring planning
- hard: Multiple deliveries with tight fuel constraints

## Action Space
The agent can take one of the following actions:
- up
- down
- left
- right

## Observation Space
The environment state includes:
- Current position of the agent
- Remaining fuel
- Pending deliveries

## Reward Function
- Small penalty for each step (encourages efficiency)
- Penalty for invalid moves
- Positive reward for completing deliveries
- Episode ends when fuel runs out or all deliveries are completed

## API Endpoints
- /reset
- /step
- /grader
- /tasks
- /baseline

## How to Run

### Docker
docker build -t eco-env .
docker run -p 8000:8000 eco-env

### Local
uvicorn main:app --reload

## Baseline
python baseline.py

## Output
Scores range from 0.0 to 1.0 based on delivery completion and efficiency.