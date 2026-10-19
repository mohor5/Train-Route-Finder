"""Command-line demo.

Examples:
    python main.py stations
    python main.py route Howrah "New Delhi"
    python main.py route Howrah "New Delhi" --metric cost
    python main.py stops Howrah "New Delhi"
    python main.py nearby Howrah --max-stops 2
"""
import argparse
import sys

from data import build_network
from graph import NoRouteError, StationNotFoundError


def main(argv=None):
    parser = argparse.ArgumentParser(description="Train route finder")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("stations", help="list all stations")

    route = sub.add_parser("route", help="fastest or cheapest route")
    route.add_argument("src")
    route.add_argument("dst")
    route.add_argument("--metric", choices=["minutes", "cost"], default="minutes")

    stops = sub.add_parser("stops", help="route with the fewest stops")
    stops.add_argument("src")
    stops.add_argument("dst")

    nearby = sub.add_parser("nearby", help="stations within N stops")
    nearby.add_argument("src")
    nearby.add_argument("--max-stops", type=int, default=2)

    args = parser.parse_args(argv)
    network = build_network()

    try:
        if args.command == "stations":
            print("\n".join(sorted(network.adj)))
        elif args.command == "route":
            total, path = network.shortest_path(args.src, args.dst, args.metric)
            unit = "minutes" if args.metric == "minutes" else "rupees"
            print(" -> ".join(path))
            print(f"Total: {total} {unit}")
        elif args.command == "stops":
            path = network.fewest_stops(args.src, args.dst)
            print(" -> ".join(path))
            print(f"Stops: {len(path) - 1}")
        elif args.command == "nearby":
            print("\n".join(network.reachable_within(args.src, args.max_stops)))
    except StationNotFoundError as e:
        print(f"Unknown station: {e}", file=sys.stderr)
        return 1
    except NoRouteError as e:
        print(e, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
