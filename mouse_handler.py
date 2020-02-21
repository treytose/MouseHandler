'''
@author Trey Holthe
2/20/2020

Requirements:
 - mouse

The MouseHandler class contains methods for creating paths for a mouse to follow 
and then moving the mouse along that path.

Currently Supported Paths:
    line segmentation - creates several points on a line and move to each of those points
    brezier curve - interpolates along a brezier curve for a seemingly natural mouse movement
'''
import mouse, random, time, math

class MouseHandler: 
    def get_point_segments(self, point_a, point_b, increment_pct=0.1):
        x1 = point_a[0]
        y1 = point_a[1]
        x2 = point_b[0]
        y2 = point_b[1]

        x_distance = abs(x2 - x1) #note: this is not the line distance 
        y_distance = abs(y2-y1)        

        num_points = int(1 / increment_pct)

        points = []

        current_x = x1
        current_y = y1

        for i in range(num_points):
            points.append((current_x, current_y))

            current_x = (i+1) * (x_distance * increment_pct)
            current_y = (i+1) * (y_distance * increment_pct)

        if x2 < x1:
            r = points[1:]
            r.reverse()
            points = points[:1] + r

        points.append(point_b)

        return points 

    def get_bezier_path(self, point_a, point_b, increment_pct=0.1):
        if increment_pct > 0.5:
            raise Exception('Invalid increment percentage given. Must be value of 0.5 or less')
        # get random point_c 
        rx = random.random() * abs(point_a[0]-point_b[0]) + min(point_a[0], point_b[0])
        ry = random.random() * abs(point_a[1]-point_b[1]) + min(point_a[1], point_b[1])
        
        mid_point = (rx, ry)        

        num_points = int(1 / increment_pct)
        points = []
        for i in range(num_points):
            points.append(self.__quad_bezier__(point_a, mid_point, point_b, increment_pct * i))

        points.append(point_b)

        return points


    # provided by "Coding Math" on YouTube #
    def __quad_bezier__(self, p0, p1, p2, t):
        px = math.pow(1 - t, 2) * p0[0] + (1 - t) * 2 * t * p1[0] + t * t * p2[0]
        py = math.pow(1-t, 2) * p0[1] + (1-t) * 2 * t * p1[1] + t * t * p2[1]

        return (px, py)


    def move_on_path(self, path, speed=1):
        for point in path:
            mouse.move(*point, duration=speed/len(path))



    def get_random_coordinate(self, rect):
        x = random.random() * abs(rect.x1 - rect.x2) + min(rect.x1, rect.x2)
        y = random.random() * abs(rect.y1 - rect.y2) + min(rect.y1, rect.y2)
        return (x, y)

class Rect:
    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.x2 = x2 
        self.y1 = y1
        self.y2 = y2


if __name__ == '__main__':
    m = MouseHandler()

    path = m.get_bezier_path(mouse.get_position(), (100,100), 0.01)
    m.move_on_path(path, 2)