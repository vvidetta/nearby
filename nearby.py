import sys
import overpass
import math

class bbox:
    def __init__(self, s: float, w: float, n: float, e: float):
        self.s = s
        self.w = w
        self.n = n
        self.e = e

def get_bbox(lat: float, lon: float) -> bbox:
    earth_radius = 6371000.0 # mean radius in metres
    earth_circumference = 2 * math.pi * earth_radius

    search_radius = 80467.2 # 50 miles in metres
    delta_lat = 360 * search_radius / earth_circumference
    s = lat - delta_lat
    n = lat + delta_lat

    lat_factor = math.cos(lat * math.pi / 180)
    delta_lon = delta_lat / lat_factor
    w = lon - delta_lon
    e = lon + delta_lon
    return bbox(s, w, n, e)

def main(args: list[str]) -> int:
    if len(args) != 3:
        usage="""
Usage: nearby.py <Latitude> <Longitude>

<Latitude> is a real number between -180  and 180.
<Longitude> is a real number between -90 and 90.

Given a point on earth, query the OpenStreetMap API for all railway stations
inside the 100 mile x 100 mile box centered at that point. The results are written to
stdout in CSV format (name, latitude, longitude).

"""
        print(usage, file=sys.stderr)
        return 1

    lat = float(args[1])
    lon = float(args[2])

    api = overpass.API()
    box = get_bbox(lat, lon)

    query = f"node({box.s}, {box.w}, {box.n}, {box.e})[railway=station][network=\"National Rail\"];"
    response = api.get(query, responseformat="json")
    stations = response["elements"]
    for station in stations:
        name = station["tags"]["name"]
        lat = station["lat"]
        lon = station["lon"]
        print(f"{name}, {lat}, {lon}")
    return 0

if __name__ == "__main__":
  sys.exit(main(sys.argv))
