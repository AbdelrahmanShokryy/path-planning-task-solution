from __future__ import annotations

import math
from typing import List

from src.models import CarPose, Cone, Path2D


class PathPlanning:
    def __init__(self, car_pose: CarPose, cones: List[Cone]):
        self.car_pose = car_pose
        self.cones = cones

    def generatePath(self) -> Path2D:
        car = self.car_pose
        half_width = 1.0  # I assume the track is 2 m wide

        # direction the car is facing, and the "left" direction
        fx, fy = math.cos(car.yaw), math.sin(car.yaw)
        lx, ly = -fy, fx

        # 1) split cones into blue and yellow, ignore cones behind the car
        blue = []
        yellow = []
        for c in self.cones:
            ahead = (c.x - car.x) * fx + (c.y - car.y) * fy
            if ahead > 0:
                if c.color == 1:
                    blue.append((ahead, c.x, c.y))
                else:
                    yellow.append((ahead, c.x, c.y))
        blue.sort()
        yellow.sort()

        # 2) make the middle points of the track
        points = []
        n = min(len(blue), len(yellow))
        for i in range(n):  # one blue + one yellow -> point in the middle
            points.append(((blue[i][1] + yellow[i][1]) / 2, (blue[i][2] + yellow[i][2]) / 2))
        for i in range(n, len(blue)):  # extra blue cones -> move them to the right
            points.append((blue[i][1] - half_width * lx, blue[i][2] - half_width * ly))
        for i in range(n, len(yellow)):  # extra yellow cones -> move them to the left
            points.append((yellow[i][1] + half_width * lx, yellow[i][2] + half_width * ly))
        points.sort(key=lambda p: (p[0] - car.x) * fx + (p[1] - car.y) * fy)

        # 3) walk from the car to each point in steps of 0.5 m
        path = []
        x, y = car.x, car.y
        dx, dy = fx, fy  # direction we are walking
        for (px, py) in points:
            while math.hypot(px - x, py - y) > 0.5 and len(path) < 18:
                d = math.hypot(px - x, py - y)
                dx, dy = (px - x) / d, (py - y) / d
                x += dx * 0.5
                y += dy * 0.5
                path.append((x, y))

        # 4) after the last point keep going the same way until 9 m (18 points)
        while len(path) < 18:
            x += dx * 0.5
            y += dy * 0.5
            path.append((x, y))

        return path
