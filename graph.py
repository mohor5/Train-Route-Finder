"""Train route finder: core graph and algorithms.

Stations are nodes; routes are undirected weighted edges stored in an
adjacency list (dict of lists). Each edge has a travel time and a cost.
"""
import heapq
from collections import deque


class StationNotFoundError(Exception):
    pass


class NoRouteError(Exception):
    pass


class RailNetwork:
    def __init__(self):
        # station -> list of (neighbour, minutes, cost)
        self.adj = {}

    def add_station(self, name):
        self.adj.setdefault(name, [])

    def add_route(self, a, b, minutes, cost):
        """Add a two-way route between stations a and b."""
        if minutes < 0 or cost < 0:
            raise ValueError("minutes and cost must be non-negative")
        self.add_station(a)
        self.add_station(b)
        self.adj[a].append((b, minutes, cost))
        self.adj[b].append((a, minutes, cost))

    def _check(self, *stations):
        for s in stations:
            if s not in self.adj:
                raise StationNotFoundError(s)

    def fewest_stops(self, src, dst):
        """BFS: path with the fewest stations. O(V + E)."""
        self._check(src, dst)
        parent = {src: None}
        queue = deque([src])
        while queue:
            cur = queue.popleft()
            if cur == dst:
                return self._build_path(parent, dst)
            for nxt, _, _ in self.adj[cur]:
                if nxt not in parent:
                    parent[nxt] = cur
                    queue.append(nxt)
        raise NoRouteError(f"No route from {src} to {dst}")

    def shortest_path(self, src, dst, metric="minutes"):
        """Dijkstra with a min-heap. O((V + E) log V).

        metric is "minutes" or "cost". Returns (total, path).
        """
        if metric not in ("minutes", "cost"):
            raise ValueError("metric must be 'minutes' or 'cost'")
        self._check(src, dst)
        idx = 1 if metric == "minutes" else 2
        best = {src: 0}
        parent = {src: None}
        heap = [(0, src)]
        while heap:
            dist, cur = heapq.heappop(heap)
            if dist > best.get(cur, float("inf")):
                continue  # stale heap entry
            if cur == dst:
                return dist, self._build_path(parent, dst)
            for edge in self.adj[cur]:
                nxt, w = edge[0], edge[idx]
                new = dist + w
                if new < best.get(nxt, float("inf")):
                    best[nxt] = new
                    parent[nxt] = cur
                    heapq.heappush(heap, (new, nxt))
        raise NoRouteError(f"No route from {src} to {dst}")

    def reachable_within(self, src, max_stops):
        """BFS limited by depth: stations reachable in <= max_stops hops."""
        self._check(src)
        seen = {src: 0}
        queue = deque([src])
        while queue:
            cur = queue.popleft()
            if seen[cur] == max_stops:
                continue
            for nxt, _, _ in self.adj[cur]:
                if nxt not in seen:
                    seen[nxt] = seen[cur] + 1
                    queue.append(nxt)
        return sorted(s for s in seen if s != src)

    @staticmethod
    def _build_path(parent, dst):
        path = []
        while dst is not None:
            path.append(dst)
            dst = parent[dst]
        return path[::-1]
