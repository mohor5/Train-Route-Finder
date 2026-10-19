# Train Route Finder

A Python project that models a rail network as a weighted graph and finds routes between stations, with a command-line demo, a REST API and a web page.

## Features
- Fewest stops between two stations (BFS)
- Fastest or cheapest route (Dijkstra's algorithm with a min-heap)
- All stations reachable within N stops
- Clear errors for unknown stations, disconnected stations and invalid input
- REST API (FastAPI) and a simple web page for picking two stations

## Complexity
| Operation | Algorithm | Time |
|---|---|---|
| Fewest stops | BFS | O(V + E) |
| Fastest / cheapest route | Dijkstra with heap | O((V + E) log V) |
| Reachable within N stops | Depth-limited BFS | O(V + E) |

The network is stored as an adjacency list, which uses O(V + E) space.

## Run it
    pip install -r requirements.txt
    python -m uvicorn api:app --reload

Open http://127.0.0.1:8000/ for the web page, or http://127.0.0.1:8000/docs for the API docs.

Command-line demo:

    python main.py route Howrah "New Delhi" --metric cost

## Run the tests
    python -m unittest -v

## Note on data
The stations, travel times and costs in data.py are illustrative sample data, not a real timetable.