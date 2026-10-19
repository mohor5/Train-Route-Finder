import unittest
from data import build_network
from main import main


class TestSampleNetwork(unittest.TestCase):
    def test_network_is_fully_connected(self):
        n = build_network()
        start = "Howrah"
        reachable = set(n.reachable_within(start, len(n.adj))) | {start}
        self.assertEqual(reachable, set(n.adj))

    def test_cli_route_succeeds(self):
        self.assertEqual(main(["route", "Howrah", "New Delhi"]), 0)

    def test_cli_unknown_station_fails(self):
        self.assertEqual(main(["route", "Howrah", "Nowhere"]), 1)


if __name__ == "__main__":
    unittest.main()
