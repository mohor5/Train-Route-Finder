import unittest
from graph import RailNetwork, StationNotFoundError, NoRouteError


def sample():
    n = RailNetwork()
    n.add_route("Howrah", "Asansol", 120, 150)
    n.add_route("Asansol", "Dhanbad", 60, 80)
    n.add_route("Howrah", "Dhanbad", 200, 120)   # direct but slower
    n.add_route("Dhanbad", "Gaya", 90, 100)
    n.add_station("Guwahati")                      # disconnected
    return n


class TestRailNetwork(unittest.TestCase):
    def test_fewest_stops_prefers_direct(self):
        self.assertEqual(sample().fewest_stops("Howrah", "Dhanbad"),
                         ["Howrah", "Dhanbad"])

    def test_fastest_uses_two_hops(self):
        total, path = sample().shortest_path("Howrah", "Dhanbad")
        self.assertEqual((total, path), (180, ["Howrah", "Asansol", "Dhanbad"]))

    def test_cheapest_uses_direct(self):
        total, path = sample().shortest_path("Howrah", "Dhanbad", "cost")
        self.assertEqual((total, path), (120, ["Howrah", "Dhanbad"]))

    def test_same_start_and_end(self):
        self.assertEqual(sample().shortest_path("Gaya", "Gaya"), (0, ["Gaya"]))
        self.assertEqual(sample().fewest_stops("Gaya", "Gaya"), ["Gaya"])

    def test_disconnected_raises(self):
        with self.assertRaises(NoRouteError):
            sample().shortest_path("Howrah", "Guwahati")
        with self.assertRaises(NoRouteError):
            sample().fewest_stops("Howrah", "Guwahati")

    def test_unknown_station_raises(self):
        with self.assertRaises(StationNotFoundError):
            sample().shortest_path("Howrah", "Nowhere")

    def test_invalid_metric_and_weights(self):
        with self.assertRaises(ValueError):
            sample().shortest_path("Howrah", "Gaya", "speed")
        with self.assertRaises(ValueError):
            RailNetwork().add_route("A", "B", -1, 5)

    def test_reachable_within(self):
        n = sample()
        self.assertEqual(n.reachable_within("Howrah", 1), ["Asansol", "Dhanbad"])
        self.assertEqual(n.reachable_within("Howrah", 2),
                         ["Asansol", "Dhanbad", "Gaya"])
        self.assertEqual(n.reachable_within("Guwahati", 3), [])


if __name__ == "__main__":
    unittest.main()
