import pygame
import numpy as np
import copy
import math

from src.pygame_utils import PyGameContext, COLORS
from src.shapes import *
from src.transformations import *
from src.static_drawings import draw_demo_v1

# load gifs
gif_frames = []
for fname in ['killua', 'killua_gon', 'naruto']:
    gif_frames.append(extract_gif_frames(f'../../data/gifs/{fname}.gif'))

# Initialize Pygame
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
pygame_context = PyGameContext(width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
corner_circle_active_radius = 10
observer_distance = 400

# drawings_timeline[t] contains all drawings valid at time t
drawings_timeline = [[]]
step = 0

def add_shape_to_timeline(shape, drawings_timeline, step):
    drawings_timeline = drawings_timeline[:step+1]
    new_drawings = []
    for drawing in drawings_timeline[-1]:
        new_drawings.append(drawing)
    new_drawings.append(shape)
    drawings_timeline.append(new_drawings)
    return drawings_timeline

def euclidean_distance(p1, p2):
    return np.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)

def find_nearest_corner(point, grid):
    min_distance, nearest_corner_idx = np.inf, None
    for idx, corner in enumerate(grid.four_corners):
        if euclidean_distance(point, corner) < min_distance:
            min_distance = euclidean_distance(point, corner)
            nearest_corner_idx = idx
    return min_distance, nearest_corner_idx


# returns closest shape in drawings array to the given location 'loc'
# distance(shape, loc) = minimum distance between the shape's four corners and loc
# consider only shapes where distance(shape, loc) <= max_allowed_distance
def find_closest_shape(args):
    point = args['point']
    drawings = args['drawings']
    max_allowed_distance = args['max_allowed_distance']
    nearest_shape_idx, nearest_corner_idx_in_shape, minimum_distance = -1, None, np.inf
    for idx in range(len(drawings)):
        distance_to_shape, nearest_corner_idx = find_nearest_corner(point, drawings[idx])
        if distance_to_shape <= max_allowed_distance:
            if distance_to_shape < minimum_distance:
                nearest_shape_idx = idx
                nearest_corner_idx_in_shape = nearest_corner_idx
                minimum_distance = distance_to_shape
    return nearest_shape_idx, nearest_corner_idx_in_shape, minimum_distance

# finds distance of target_point from a line that passes from line_point at line_angle
def distance_from_line(line_point, line_angle, target_point):
    return abs((target_point[0] - line_point[0])*np.sin(line_angle) - (target_point[1] - line_point[1])*np.cos(line_angle))

mode = "view"
# maintains temporary variables to draw shapes not yet present in the drawings_timeline
state_variables = {} 

# possible modes
# view: simply see the drawings (default) (key: 'v')
# create: create new rectangles on screen (key: 'c')
# translate: translate an existing shape (key: 't')
# rotate: rotate around centroid (key: 'r')
# scale: scale around centroid (key: 'r')
# deform: squish / stretch around an axis (key: 'd')
# perspective: rotate out of plane around an axis lying on the plane through the centroid and then project it back to the plane. (key: 'p')

# Game loop
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if 'active_transformation_data' not in state_variables:
                if event.key == pygame.K_c:
                    mode = 'create'
                elif event.key == pygame.K_v:
                    mode = 'view'
                elif event.key == pygame.K_t:
                    mode = 'translate'
                elif event.key == pygame.K_r:
                    mode = 'rotate'
                elif event.key == pygame.K_s:
                    mode = 'scale'
                elif event.key == pygame.K_d:
                    mode = 'deform'
                elif event.key == pygame.K_y:
                    mode = 'perspective_rotation_along_y'
                elif event.key == pygame.K_x:
                    mode = 'perspective_rotation_along_x'
                elif event.key == pygame.K_z:
                    mods = pygame.key.get_mods()
                    if (mods & pygame.KMOD_CTRL) and (mods & pygame.KMOD_SHIFT):
                        if step < len(drawings_timeline)-1:
                            step += 1
                    elif (mods & pygame.KMOD_CTRL):
                        if step > 0:
                            step -= 1
                state_variables.clear()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if mode == 'create':
                state_variables['rectangle_diagonal'] = [event.pos, event.pos]
                state_variables['active_drawing'] = \
                    Grid(getFourCornerPointsFromDiagonalPoints(*(state_variables['rectangle_diagonal'])), 
                         pygame_context)
            elif mode in ['translate', 'rotate', 'scale', 'deform', 'perspective_rotation_along_y', 'perspective_rotation_along_x']:
                if 'active_corner_data' in state_variables:
                    state_variables['active_transformation_data'] = {
                        'anchor_mouse_position': event.pos
                    }
        elif event.type == pygame.MOUSEBUTTONUP:
            if mode == 'create':
                drawings_timeline = add_shape_to_timeline(state_variables['active_drawing'],
                                      drawings_timeline,
                                      step)
                state_variables.clear()
                step += 1
            elif mode in ['translate', 'rotate', 'scale', 'deform', 'perspective_rotation_along_y', 'perspective_rotation_along_x']:
                if state_variables.get('active_transformation_data', {}).get('transformed_shape', None) is not None:
                    drawings_timeline = drawings_timeline[:step+1]
                    drawings_copy = []
                    for drawing in drawings_timeline[step]:
                        drawings_copy.append(drawing)
                    drawings_timeline.append(drawings_copy)
                    step += 1
                    focus_shape_idx, focus_corner_idx_in_shape = state_variables['active_corner_data']
                    drawings_timeline[step][focus_shape_idx] = state_variables['active_transformation_data']['transformed_shape']
                    del state_variables['active_transformation_data']
        elif event.type == pygame.MOUSEMOTION:
            if mode=='create':
                if 'active_drawing' in state_variables:
                    state_variables['rectangle_diagonal'][1] = event.pos
                    state_variables['active_drawing'] = \
                        Grid(getFourCornerPointsFromDiagonalPoints(*(state_variables['rectangle_diagonal'])), 
                             pygame_context)
            elif mode in ['translate', 'rotate', 'scale', 'deform', 'perspective_rotation_along_y', 'perspective_rotation_along_x']:
                if 'active_transformation_data' in state_variables:
                    current_mouse_position = event.pos
                    anchor_mouse_position = state_variables['active_transformation_data']['anchor_mouse_position']
                    focus_shape_idx, focus_corner_idx_in_shape = state_variables['active_corner_data']
                    focus_shape_centroid = drawings_timeline[step][focus_shape_idx].centroid()
                    state_variables['active_transformation_data']['markings'] = []
                    transformed_shape = None
                    if mode == 'translate':
                        translation_x = current_mouse_position[0] - anchor_mouse_position[0]
                        translation_y = current_mouse_position[1] - anchor_mouse_position[1]
                        transformed_shape = drawings_timeline[step][focus_shape_idx]\
                            .applyTransformation(translationTransformation(translation_x, translation_y))
                    elif mode == 'scale':
                        anchor_distance_from_centroid = euclidean_distance(focus_shape_centroid, anchor_mouse_position)
                        current_distance_from_centroid = euclidean_distance(focus_shape_centroid, current_mouse_position)
                        scale_factor = max(current_distance_from_centroid / anchor_distance_from_centroid, 0.01)
                        transformed_shape = drawings_timeline[step][focus_shape_idx]\
                            .applyTransformation(scaleAroundPointTransformation(focus_shape_centroid, scale_factor))
                    elif mode == 'rotate':
                        anchor_angle = np.arctan2(focus_shape_centroid[1] - anchor_mouse_position[1], focus_shape_centroid[0] - anchor_mouse_position[0])
                        current_angle = np.arctan2(focus_shape_centroid[1] - current_mouse_position[1], focus_shape_centroid[0] - current_mouse_position[0])
                        transformed_shape = drawings_timeline[step][focus_shape_idx]\
                            .applyTransformation(rotationClockwiseAroundPointTransformation(focus_shape_centroid, current_angle - anchor_angle))
                    elif mode == 'deform':
                        axis_angle = np.arctan2(current_mouse_position[1] - anchor_mouse_position[1], current_mouse_position[0] - anchor_mouse_position[0])
                        axis_angle += np.pi / 2
                        anchor_distance = distance_from_line(focus_shape_centroid, axis_angle, anchor_mouse_position)
                        current_distance = distance_from_line(focus_shape_centroid, axis_angle, current_mouse_position)
                        deform_factor = current_distance / anchor_distance
                        transformed_shape = drawings_timeline[step][focus_shape_idx]\
                            .applyTransformation( 
                                deformAroundPointAtAnAngleTransformation(focus_shape_centroid, axis_angle, deform_factor))
                        state_variables['active_transformation_data']['markings'] = [
                            ('dashed_line', current_mouse_position, anchor_mouse_position),
                            ('dashed_line', [focus_shape_centroid[0]+400*np.cos(axis_angle), focus_shape_centroid[1]+400*np.sin(axis_angle)],
                                    [focus_shape_centroid[0]-400*np.cos(axis_angle), focus_shape_centroid[1]-400*np.sin(axis_angle)])
                        ]
                    elif mode in ["perspective_rotation_along_y", 'perspective_rotation_along_x']:
                        axis = mode.split('_')[-1]
                        axis_angle = np.pi / 2 if axis=='y' else 0
                        anchor_distance = distance_from_line(focus_shape_centroid, axis_angle, anchor_mouse_position)
                        current_distance = distance_from_line(focus_shape_centroid, axis_angle, current_mouse_position)
                        if current_distance <= anchor_distance:
                            theta = np.arccos(current_distance / anchor_distance)
                            idx = 0 if axis=='y' else 1
                            if ((anchor_mouse_position[idx] - focus_shape_centroid[idx]) * (current_mouse_position[idx] - focus_shape_centroid[idx])) < 0:
                                theta = np.pi - theta
                            if (current_mouse_position[idx] < anchor_mouse_position[idx]):
                                theta *= -1
                            transformation_function = rotateAlongYAxisAroundPointTransformation if axis=='y' else \
                                    rotateAlongXAxisAroundPointTransformation
                            transformed_shape = drawings_timeline[step][focus_shape_idx]\
                                .applyTransformation( 
                                    transformation_function(focus_shape_centroid, theta, observer_distance))
                            state_variables['active_transformation_data']['markings'] = [
                                ('dashed_line', current_mouse_position, anchor_mouse_position),
                                ('dashed_line', [focus_shape_centroid[0]+400*np.cos(axis_angle), focus_shape_centroid[1]+400*np.sin(axis_angle)],
                                        [focus_shape_centroid[0]-400*np.cos(axis_angle), focus_shape_centroid[1]-400*np.sin(axis_angle)])
                            ]
                    state_variables['active_transformation_data']['markings'].append(('cross', focus_shape_centroid))
                    if transformed_shape is not None:
                        state_variables['active_transformation_data']['transformed_shape'] = transformed_shape
                else:
                    focus_shape_idx, focus_corner_idx_in_shape, _ = find_closest_shape({
                        'point': event.pos,
                        'drawings': drawings_timeline[step],
                        'max_allowed_distance': corner_circle_active_radius
                    })
                    if focus_corner_idx_in_shape is not None:
                        state_variables['active_corner_data'] = (focus_shape_idx, focus_corner_idx_in_shape)
                    else:
                        if 'active_corner_data' in state_variables:
                            del state_variables['active_corner_data']

    # Fill the background
    pygame_context.screen.fill(pygame_context.background_color)

    # display instructions at top left
    instructions_text = "c = create   v = view   t = translate   r = rotate z   s = scale   d = deform   x = rotate x   y = rotate y"
    instructions_text = pygame.font.Font(None, 22).render(instructions_text, True, (128, 0, 0))
    pygame_context.screen.blit(instructions_text, (0, 0))

    # display the current mode at top right
    pretty_mode_names = {"perspective_rotation_along_y": "rotate y", "perspective_rotation_along_x": "rotate x"}
    current_mode_text = f"current mode: {pretty_mode_names.get(mode, mode)}"
    current_mode_text = pygame.font.Font(None, 22).render(current_mode_text, True, (128, 0, 0))
    pygame_context.screen.blit(current_mode_text, (0, 20))

    # draw_demo_v1(pygame_context)

    # draw shapes
    active_transformation_shape = state_variables.get('active_transformation_data', {}).get('transformed_shape', None)
    active_transformation_shape_idx = -1
    if active_transformation_shape is not None:
        active_transformation_shape_idx, _ = state_variables['active_corner_data']
    for idx, drawing in enumerate(drawings_timeline[step]):
        if idx != active_transformation_shape_idx:
            drawing.draw()
    if active_transformation_shape_idx!=-1:
        active_transformation_shape.draw()
    
    if 'active_drawing' in state_variables:
        state_variables['active_drawing'].draw()

    if 'active_corner_data' in state_variables:
        focus_shape_idx, focus_corner_idx_in_shape = state_variables['active_corner_data']
        corner = drawings_timeline[step][focus_shape_idx].four_corners[focus_corner_idx_in_shape]
        if active_transformation_shape is not None:
            corner = active_transformation_shape.four_corners[focus_corner_idx_in_shape]
        pygame.draw.circle(pygame_context.screen, COLORS["black"], 
                           corner, corner_circle_active_radius, 1)
        
    if active_transformation_shape is not None:
        for marking in state_variables['active_transformation_data']['markings']:
            if marking[0]=="cross":
                drawCross(pygame_context.screen, COLORS['black'], marking[1], 5)
            elif marking[0]=="dashed_line":
                drawDashedLine(pygame_context.screen, COLORS['black'], marking[1], marking[2])

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()




