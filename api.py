"""REST API for the train route finder.

Run with:  uvicorn api:app --reload
Docs at:   http://127.0.0.1:8000/docs
"""
from pathlib import Path
from typing import Literal

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import FileResponse

from data import build_network
from graph import NoRouteError, StationNotFoundError

app = FastAPI(title="Train Route Finder")
network = build_network()
STATIC_DIR = Path(__file__).parent / "static"


def _not_found(error):
    if isinstance(error, StationNotFoundError):
        return HTTPException(status_code=404, detail=f"Unknown station: {error}")
    return HTTPException(status_code=404, detail=str(error))


@app.get("/", include_in_schema=False)
def home():
    return FileResponse(STATIC_DIR / "index.html")


@app.get("/stations")
def list_stations():
    return {"stations": sorted(network.adj)}


@app.get("/route")
def fastest_or_cheapest(src: str, dst: str,
                        metric: Literal["minutes", "cost"] = "minutes"):
    try:
        total, path = network.shortest_path(src, dst, metric)
    except (StationNotFoundError, NoRouteError) as error:
        raise _not_found(error)
    return {"src": src, "dst": dst, "metric": metric, "total": total, "path": path}


@app.get("/stops")
def fewest_stops(src: str, dst: str):
    try:
        path = network.fewest_stops(src, dst)
    except (StationNotFoundError, NoRouteError) as error:
        raise _not_found(error)
    return {"src": src, "dst": dst, "stops": len(path) - 1, "path": path}


@app.get("/nearby")
def nearby(src: str, max_stops: int = Query(2, ge=0, le=50)):
    try:
        stations = network.reachable_within(src, max_stops)
    except StationNotFoundError as error:
        raise _not_found(error)
    return {"src": src, "max_stops": max_stops, "stations": stations}
