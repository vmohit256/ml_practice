
import copy
import numpy as np

class Transformation:
    def __init__(self, matrix):
        self.matrix = copy.deepcopy(matrix)
    
    def transformAll(self, points):
        # points is a numpy array of shape [n, 2]
        homogenous_points = np.hstack((points, np.ones((points.shape[0], 1)))).T
        transformed_points = (self.matrix @ homogenous_points).T
        return transformed_points

    def transform(self, point):
        homogeneous_point = np.array(list(point) + [1])
        transformed_point = self.matrix @ homogeneous_point
        if transformed_point[2] != 0:
            transformed_point = transformed_point / transformed_point[2]
        return transformed_point


# IMPORTANT: assumes that transformations[0] is applied first, then transformations[1], then transformations[2] and so on
def chainTransformations(transformations):
    matrix = None
    for transformation in transformations:
        if matrix is None:
            matrix = transformation.matrix
        else:
            matrix = transformation.matrix @ matrix
    return Transformation(matrix)

def translationTransformation(tx, ty):
    matrix = np.array([[1, 0, tx], 
                        [0, 1, ty], 
                        [0, 0, 1]])
    return Transformation(matrix)

def rotateClockwiseAroundOriginTransformation(theta):
    matrix = np.array([[np.cos(theta), -np.sin(theta), 0], 
                        [np.sin(theta), np.cos(theta), 0], 
                        [0, 0, 1]])
    return Transformation(matrix)

def rotationClockwiseAroundPointTransformation(point, theta):
    recenter_around_origin = translationTransformation(*[-v for v in point])
    rotate_clockwise_around_origin = rotateClockwiseAroundOriginTransformation(theta)
    relocate_to_original_position = translationTransformation(*point)
    return chainTransformations([recenter_around_origin, rotate_clockwise_around_origin, relocate_to_original_position])

def scaleAroundOriginTransformation(scale_factor):
    matrix = np.array([[scale_factor, 0, 0], 
                        [0, scale_factor, 0], 
                        [0, 0, 1]])
    return Transformation(matrix)

def scaleAroundPointTransformation(point, scale_factor):
    recenter_around_origin = translationTransformation(*[-v for v in point])
    scale_around_origin = scaleAroundOriginTransformation(scale_factor)
    relocate_to_original_position = translationTransformation(*point)
    return chainTransformations([recenter_around_origin, scale_around_origin, relocate_to_original_position])

def deformAlongYAxisTransformation(deform_factor):
    # for deform_factor < 1 it squishes it and for deform factor > 1 is stretches shapes along y-axis
    matrix = np.array([[1, 0, 0], 
                        [0, deform_factor, 0], 
                        [0, 0, 1]])
    return Transformation(matrix)

def deformAroundPointAtAnAngleTransformation(point, theta, deform_factor):
    recenter_around_origin = translationTransformation(*[-v for v in point])
    rotate_clockwise_around_origin = rotateClockwiseAroundOriginTransformation(theta)
    deform_along_y_axis = deformAlongYAxisTransformation(deform_factor)
    rotate_back_around_origin = rotateClockwiseAroundOriginTransformation(-theta)
    relocate_to_original_position = translationTransformation(*point)
    return chainTransformations([recenter_around_origin, rotate_clockwise_around_origin, 
                                 deform_along_y_axis, 
                                 rotate_back_around_origin, relocate_to_original_position])

# imagine an observer is at point (0, 0, d) in 3d on z-axis 
# observing a rectangle on the x-y plane centered on origin
# now, rotate the rectangle around the y-axis and project it back onto
# the x-y plane to get the perspective projection formula below
def rotateAlongYAxisTransformation(theta, observer_distance):
    matrix = np.array([[np.cos(theta), 0, 0], 
                        [0, 1, 0], 
                        [np.sin(theta) / observer_distance, 0, 1]])
    return Transformation(matrix)

def rotateAlongYAxisAroundPointTransformation(point, theta, observer_distance):
    recenter_around_origin = translationTransformation(*[-v for v in point])
    rotate_along_y_axis = rotateAlongYAxisTransformation(theta, observer_distance)
    relocate_to_original_position = translationTransformation(*point)
    return chainTransformations([recenter_around_origin, rotate_along_y_axis, relocate_to_original_position])

def rotateAlongXAxisTransformation(theta, observer_distance):
    matrix = np.array([[1, 0, 0], 
                        [0, np.cos(theta), 0], 
                        [0, np.sin(theta) / observer_distance, 1]])
    return Transformation(matrix)

def rotateAlongXAxisAroundPointTransformation(point, theta, observer_distance):
    recenter_around_origin = translationTransformation(*[-v for v in point])
    rotate_along_x_axis = rotateAlongXAxisTransformation(theta, observer_distance)
    relocate_to_original_position = translationTransformation(*point)
    return chainTransformations([recenter_around_origin, rotate_along_x_axis, relocate_to_original_position])