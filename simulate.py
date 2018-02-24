import numpy as np
from map import Area, Display
import geojson
import pandas as pd

start_xs = np.array([-73.933250])
start_ys = np.array([40.690121])
end_xs = np.array([-73.933250])
end_ys = np.array([40.690121])
co2_savings = np.array([30])
profit = np.array([10])

assert len(start_xs) == len(start_ys) == len(end_xs) == len(end_ys) == len(co2_savings) == len(profit), "arrays of unequal size"

with open("data/fire_companies.geojson", 'r') as f:
    raw = geojson.load(f)

INITIAL_CARS = 100

area_coords = {area["id"]: list(geojson.utils.coords(area)) for area in raw.features}
areas = [Area(key, value, INITIAL_CARS) for key, value in area_coords.items()]

disp = Display(areas, start_xs, start_ys, end_xs, end_ys, co2_savings, profit)
output = disp.json_output
print(output)

