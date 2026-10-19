import unittest

from fastapi.testclient import TestClient

from api import app

client = TestClient(app)


class TestApi(unittest.TestCase):
    def test_home_page_is_served(self):
        response = client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Train Route Finder", response.text)

    def test_stations(self):
        response = client.get("/stations")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Howrah", response.json()["stations"])

    def test_route_fastest(self):
        response = client.get("/route", params={"src": "Howrah", "dst": "New Delhi"})
        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertEqual(body["path"][0], "Howrah")
        self.assertEqual(body["path"][-1], "New Delhi")
        self.assertEqual(body["total"], 1130)

    def test_route_cheapest_differs_from_fastest(self):
        fast = client.get("/route", params={"src": "Howrah", "dst": "New Delhi"}).json()
        cheap = client.get("/route", params={"src": "Howrah", "dst": "New Delhi",
                                             "metric": "cost"}).json()
        self.assertNotEqual(fast["path"], cheap["path"])

    def test_unknown_station_returns_404(self):
        response = client.get("/route", params={"src": "Howrah", "dst": "Nowhere"})
        self.assertEqual(response.status_code, 404)

    def test_invalid_metric_returns_422(self):
        response = client.get("/route", params={"src": "Howrah", "dst": "Gaya",
                                                "metric": "speed"})
        self.assertEqual(response.status_code, 422)

    def test_stops(self):
        body = client.get("/stops", params={"src": "Howrah", "dst": "Guwahati"}).json()
        self.assertEqual(body["stops"], 2)

    def test_nearby_validates_max_stops(self):
        response = client.get("/nearby", params={"src": "Howrah", "max_stops": -1})
        self.assertEqual(response.status_code, 422)


if __name__ == "__main__":
    unittest.main()
