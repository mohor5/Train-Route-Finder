# Train Route Finder

A Python project that models a rail network as a weighted graph and finds routes between stations.

## Features
- Fewest stops between two stations (BFS)
- Fastest or cheapest route (Dijkstra's algorithm with a min-heap)
- All stations reachable within N stops
- Clear errors for unknown stations, disconnected stations and invalid input

## Complexity
| Operation | Algorithm | Time |
|---|---|---|
| Fewest stops | BFS | O(V + E) |
| Fastest / cheapest route | Dijkstra with heap | O((V + E) log V) |
| Reachable within N stops | Depth-limited BFS | O(V + E) |

The network is stored as an adjacency list, which uses O(V + E) space.

## Run the tests
    python -m unittest -v

## Status
In progress. Next: a FastAPI wrapper and a simple web page to pick two stations.