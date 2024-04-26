import pygame
import numpy as np
import copy
import math
from PIL import Image
import time

class Quadrilateral:
    def __init__(self, points, color, pygame_context):
        self.points = copy.deepcopy(points)
        self.color = copy.deepcopy(color)
        self.pygame_context = pygame_context
    
    def draw(self):
        pygame.draw.polygon(self.pygame_context.screen, self.color, self.points)

    def centroid(self):
        x_coordinate = sum([p[0] for p in self.points]) / len(self.points)
        y_coordinate = sum([p[1] for p in self.points]) / len(self.points)
        return [x_coordinate, y_coordinate]

    # returns None if the transformation fails   
    def applyTransformation(self, transformation):
        new_q = Quadrilateral(self.points, self.color, self.pygame_context)
        for i in range(len(new_q.points)):
            transformed_point = transformation.transform(new_q.points[i])
            if transformed_point[2]==0: return None
            if (transformed_point[0] < 0  or transformed_point[0] >= self.pygame_context.width):
                return None
            if (transformed_point[1] < 0  or transformed_point[1] >= self.pygame_context.height):
                return None
            new_q.points[i] = [transformed_point[0], transformed_point[1]]
        return new_q
    
class Grid:
    # intially, each grid is always a grid of rectangles
    def __init__(self, four_corners, pygame_context, 
                 step_length=10, quadrilaterals=None):
        self.pygame_context = pygame_context
        self.four_corners = copy.deepcopy(four_corners)
        self.step_length = copy.deepcopy(step_length)
        ref_point = self.four_corners[0]
        if self.four_corners[1][0] != ref_point[0]:
            x_delta_neighbor = self.four_corners[1]
            y_delta_neighbor = self.four_corners[3]
        else:
            x_delta_neighbor = self.four_corners[3]
            y_delta_neighbor = self.four_corners[1]
        
        self.quadrilaterals = []
        if quadrilaterals is not None:
            for q_row in quadrilaterals:
                self.quadrilaterals.append([])
                for q_cell in q_row:
                    self.quadrilaterals[-1].append(Quadrilateral(q_cell.points, q_cell.color, q_cell.pygame_context))
        else:
            sign = lambda x: 1 if x>=0 else -1

            x_total_delta = x_delta_neighbor[0] - ref_point[0]
            x_step = sign(x_total_delta) * self.step_length
            x_deltas = [0]
            while abs(x_deltas[-1] + x_step) < abs(x_total_delta):
                x_deltas.append(x_deltas[-1] + x_step)
            if abs(x_deltas[-1]) < abs(x_total_delta):
                x_deltas.append(x_total_delta)

            y_total_delta = y_delta_neighbor[1] - ref_point[1]
            y_step = sign(y_total_delta) * self.step_length
            y_deltas = [0]
            while abs(y_deltas[-1] + y_step) < abs(y_total_delta):
                y_deltas.append(y_deltas[-1] + y_step)
            if abs(y_deltas[-1]) < abs(y_total_delta):
                y_deltas.append(y_total_delta)

            for j in range(1, len(y_deltas)):
                self.quadrilaterals.append([])
                for i in range(1, len(x_deltas)):
                    color = (max(0, math.ceil(255 * (1 - (i-1)/len(x_deltas) - (j-1)/len(y_deltas)))),
                            math.ceil(255 * j / len(y_deltas)),
                            math.ceil(255 * i / len(x_deltas)))
                    points = [
                        [ref_point[0] + x_deltas[i-1], ref_point[1] + y_deltas[j-1]],
                        [ref_point[0] + x_deltas[i], ref_point[1] + y_deltas[j-1]],
                        [ref_point[0] + x_deltas[i], ref_point[1] + y_deltas[j]],
                        [ref_point[0] + x_deltas[i-1], ref_point[1] + y_deltas[j]]
                    ]
                    self.quadrilaterals[-1].append(Quadrilateral(points, color, self.pygame_context))

    def draw(self):
        #Quadrilateral(self.four_corners, (0, 255, 0), self.pygame_context).draw()
        for quad_row in self.quadrilaterals:
            for quadrilateral in quad_row:
                quadrilateral.draw()

    def centroid(self):
        x_coordinate = sum([p[0] for p in self.four_corners]) / len(self.four_corners)
        y_coordinate = sum([p[1] for p in self.four_corners]) / len(self.four_corners)
        return [x_coordinate, y_coordinate]
    
    # returns None if the transformation fails on any of the quadrilaterals  
    def applyTransformation(self, transformation):
        new_grid = Grid(self.four_corners, self.pygame_context, self.step_length, self.quadrilaterals)
        q = Quadrilateral(new_grid.four_corners, (255, 0, 0), self.pygame_context).applyTransformation(transformation)
        if q is None:
            return None
        new_grid.four_corners = q.points

        for i in range(len(new_grid.quadrilaterals)):
            for j in range(len(new_grid.quadrilaterals[i])):
                new_grid.quadrilaterals[i][j] = new_grid.quadrilaterals[i][j]\
                    .applyTransformation(transformation)
                if new_grid.quadrilaterals[i][j] is None:
                    return None
        return new_grid

class GifViewPort:
    def __init__(self, four_corners, pygame_context, frames, points = None, color_indices = None):
        self.pygame_context = pygame_context
        self.four_corners = copy.deepcopy(four_corners)
        self.frames = frames
        if points is None:
            # construct the points and color_indices matrices
            ref_point = self.four_corners[0]
            opposite_point = self.four_corners[2]
            sign = lambda x: 1 if x>=0 else -1
            x, y = round(ref_point[0]), round(ref_point[1])
            x_delta, y_delta = round(opposite_point[0] - ref_point[0]), round(opposite_point[1] - ref_point[1])
            gif_w, gif_h = frames[0].shape[:2]
            if x_delta == 0: x_delta += 1
            if y_delta == 0: y_delta += 1
            self.points = []
            self.color_indices = []
            for d_x in range(0, x_delta, sign(x_delta)):
                for d_y in range(0, y_delta, sign(y_delta)):
                    self.points.append([float(x + d_x), float(y + d_y)])
                    image_x = int(gif_w * d_y / y_delta)
                    image_y = int(gif_h * d_x / x_delta)
                    self.color_indices.append([image_x, image_y])
            self.points = np.array(self.points)
        else:
            assert frames is not None, "Frames cannot be Null if the points are already computed"
            self.points = copy.deepcopy(points)
            self.color_indices = copy.deepcopy(color_indices)

    def draw(self):
        frame_idx = int(12 * time.time()) % len(self.frames)
        for point, color_idx in zip(self.points, self.color_indices):
            rounded_point = [round(point[0]), round(point[1])]
            self.pygame_context.screen.set_at(rounded_point, self.frames[frame_idx][color_idx[0]][color_idx[1]])

    def centroid(self):
        x_coordinate = sum([p[0] for p in self.four_corners]) / len(self.four_corners)
        y_coordinate = sum([p[1] for p in self.four_corners]) / len(self.four_corners)
        return [x_coordinate, y_coordinate]
    
    # returns None if the transformation fails on any of the quadrilaterals  
    def applyTransformation(self, transformation):
        new_gif_viewport = GifViewPort(self.four_corners, self.pygame_context, self.frames, self.points, self.color_indices)
        for points_list in [new_gif_viewport.four_corners]:
            for i in range(len(points_list)):
                transformed_point = transformation.transform(points_list[i])
                if transformed_point[2]==0: return None
                if (transformed_point[0] < 0  or transformed_point[0] >= self.pygame_context.width):
                    return None
                if (transformed_point[1] < 0  or transformed_point[1] >= self.pygame_context.height):
                    return None
                points_list[i] = [transformed_point[0], transformed_point[1]]
        new_gif_viewport.points = transformation.transformAll(new_gif_viewport.points)
        if np.any(new_gif_viewport.points[:, -1] == 0):
            return None
        new_gif_viewport.points[:, 0] = new_gif_viewport.points[:, 0] / new_gif_viewport.points[:, 2]
        new_gif_viewport.points[:, 1] = new_gif_viewport.points[:, 1] / new_gif_viewport.points[:, 2]
        new_gif_viewport.points = new_gif_viewport.points[:, :2]
        if (np.any(new_gif_viewport.points < 0) 
            or np.any(new_gif_viewport.points[:, 0] >= self.pygame_context.width) 
            or np.any(new_gif_viewport.points[:, 1] >= self.pygame_context.height)):
            return None
        return new_gif_viewport

def getFourCornerPointsFromDiagonalPoints(start_point, end_point):
    points = [
        list(start_point),
        [start_point[0], end_point[1]],
        list(end_point),
        [end_point[0], start_point[1]]
    ]
    return points

def drawCross(surface, color, center, size):
    x, y = center
    pygame.draw.line(surface, color, (x-size, y-size), (x+size, y+size), 2)
    pygame.draw.line(surface, color, (x-size, y+size), (x+size, y-size), 2)

def drawDashedLine(surface, color, start_pos, end_pos, width=1, dash_length=5):
    x_delta_total = end_pos[0] - start_pos[0]
    y_delta_total = end_pos[1] - start_pos[1]
    total_distance = np.sqrt(x_delta_total ** 2 + y_delta_total ** 2)
    start_distance = 0
    while start_distance < total_distance:
        end_distance = min(total_distance, start_distance+dash_length)
        segment_start_point = [start_pos[0] + x_delta_total * start_distance / total_distance,
                               start_pos[1] + y_delta_total * start_distance / total_distance]
        segment_end_point = [start_pos[0] + x_delta_total * end_distance / total_distance,
                               start_pos[1] + y_delta_total * end_distance / total_distance]
        pygame.draw.line(surface, color, segment_start_point, segment_end_point, width)
        start_distance += 1.5*dash_length

def extractGifFrames(gif_path):
    im = Image.open(gif_path)
    frames = []
    # To iterate through the entire gif
    try:
        while 1:
            im.seek(im.tell()+1)
            frames.append(np.array(im))
            # do something to im
    except EOFError:
        pass # end of sequence
    return frames