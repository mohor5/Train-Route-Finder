"""Sample rail network. Times and costs are illustrative, not a real timetable."""
from graph import RailNetwork

# (station A, station B, minutes, cost in rupees)
ROUTES = [
    ("Howrah", "Asansol", 160, 180),
    ("Asansol", "Dhanbad", 60, 90),
    ("Dhanbad", "Gaya", 150, 200),
    ("Gaya", "Patna", 120, 140),
    ("Gaya", "Mughalsarai", 120, 150),
    ("Patna", "Mughalsarai", 220, 250),
    ("Howrah", "Patna", 480, 400),
    ("Mughalsarai", "Varanasi", 40, 60),
    ("Mughalsarai", "Prayagraj", 130, 160),
    ("Prayagraj", "Kanpur", 150, 180),
    ("Kanpur", "Lucknow", 80, 100),
    ("Varanasi", "Lucknow", 300, 250),
    ("Kanpur", "New Delhi", 360, 350),
    ("Lucknow", "New Delhi", 400, 380),
    ("Howrah", "New Jalpaiguri", 500, 450),
    ("New Jalpaiguri", "Guwahati", 360, 330),
]


def build_network():
    network = RailNetwork()
    for a, b, minutes, cost in ROUTES:
        network.add_route(a, b, minutes, cost)
    return network
