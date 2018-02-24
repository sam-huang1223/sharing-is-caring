from shapely.geometry import Point
from shapely.geometry.polygon import Polygon


class Area:
    def __init__(self, name, vertices, initial_score):
        self.name = name
        self.vertices = vertices[:-1]
        self.centre = self.get_center()
        self.score = initial_score

    def __contains__(self, item):
        # can also reverse engineer voronoi generating points based on polygon vertices
        point = Point(*item)
        polygon = Polygon(self.vertices)
        return polygon.contains(point)

    def get_center(self):
        polygon = Polygon(self.vertices)
        return polygon.centroid.x, polygon.centroid.y


class Display:
    def __init__(self, areas, start_xs, start_ys, end_xs, end_ys, co2, profit):
        self.areas = {area.name: area for area in areas}
        self.start_xs = start_xs
        self.start_ys = start_ys
        self.end_xs = end_xs
        self.end_ys = end_ys
        self.co2 = co2
        self.profit = profit

        #self.assign_initial_distribution(initial_distribution_df)
        print(self.get_adjacent(self.areas[0]))

        self.json_output = {area.name: [area.score] for area in self.areas.values()}

        for n in range(len(self.start_xs)):
            self.step(n)

        assert sum([values[-1] for values in self.json_output.values()]) == sum([values[0] for values in self.json_output.values()])

    def step(self, n):
        other_found = False
        for area in self.areas.values():
            start_point = (self.start_xs[n], self.start_ys[n])
            end_point = (self.end_xs[n], self.end_ys[n])
            if start_point in area:
                print("{} found in area {}".format(start_point, area.name))
                area.score -= 1
                print("area {} score changed from {} to {}".format(area.name, area.score+1, area.score))
                if other_found:
                    break
                else:
                    other_found = True
            if end_point in area:
                print("{} found in area {}".format(end_point, area.name))
                area.score += 1
                print("area {} score changed from {} to {}".format(area.name, area.score-1, area.score))
                if other_found:
                    break
                else:
                    other_found = True

        for area in self.areas.values():
            self.json_output[area.name].append(area.score)

    def get_adjacent(self, target_area):
        return set([area.name for vertex in target_area.vertices for area in self.areas.values() if vertex in area.vertices and area != target_area])




'''
    def assign_initial_distribution(self, df):
        for row in df.iterrows():
            point = Point((row[1]['x'], row[1]['y']))
            for area in self.areas:
                polygon = Polygon(area.vertices)
                if polygon.contains(point):
                    area.score += 1
                    break
'''
