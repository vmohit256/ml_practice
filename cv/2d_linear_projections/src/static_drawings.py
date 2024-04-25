# contains static drawings

from src.pygame_utils import PyGameContext, COLORS
from src.shapes import Quadrilateral, Grid
from src.transformations import *

# draws all transformations demo
def draw_demo_v1(pygame_context):
    # Draw the arbitrary quadrilateral
    q = Quadrilateral([[40, 40], [120, 40], [80, 80], [60, 80]], COLORS["red"], pygame_context) # weird quadrilateral
    q = Quadrilateral([[10, 10], [50, 10], [50, 50], [10, 50]], COLORS["red"], pygame_context) # square
    q = Grid([[10, 10], [50, 10], [50, 50], [10, 50]], pygame_context)

    q.draw()

    # translation
    t1 = q.applyTransformation(translationTransformation(100, 0))
    t1.draw()

    # translation + rotation
    t2 = t1\
        .applyTransformation(translationTransformation(100, 0))
    
    t2 = t2\
        .applyTransformation( 
            rotationClockwiseAroundPointTransformation(t2.centroid(), np.pi / 4))
    t2.draw()

    # translation + rotation + scaling
    t3 = t2\
        .applyTransformation(translationTransformation(100, 150))
    t3 = t3\
        .applyTransformation( 
            scaleAroundPointTransformation(t3.centroid(), 3))
    t3.draw()

    # translation + rotation + scaling + deformation along an axis
    t4 = t3\
        .applyTransformation(translationTransformation(250, 0))
    t4 = t4\
        .applyTransformation( 
            deformAroundPointAtAnAngleTransformation(t4.centroid(), np.pi / 4, 1/2))
    t4.draw()

    t4point1 = t4\
        .applyTransformation(translationTransformation(-400, 200))
    t4point1 = t4point1\
        .applyTransformation(scaleAroundPointTransformation(t4point1.centroid(), 2))
    t4point1 = t4point1\
        .applyTransformation( 
            rotationClockwiseAroundPointTransformation(t4point1.centroid(), np.pi / 4))
    t4point1.draw()

    # translation + rotation + scaling + deformation along an axis + rotate along y-axis
    # like looking at the screen from left
    t5 = t4point1.applyTransformation(translationTransformation(400, 0))
    t5 = t5.applyTransformation(
            rotateAlongYAxisAroundPointTransformation(t5.centroid(), np.pi / 3, 400))
    t5.draw()

    # translation + rotation + scaling + deformation along an axis + rotate along x-axis
    # like looking at the screen from above
    t6 = t4point1\
        .applyTransformation(translationTransformation(0, 250))
    t6 = t6.applyTransformation(
            rotateAlongXAxisAroundPointTransformation(t6.centroid(), np.pi / 6, 400))
    t6.draw()

    # everything combined
    # like looking at the screen from above and left
    t7 = t5\
        .applyTransformation(translationTransformation(0, 250))
    t7 = t7.applyTransformation(
            rotateAlongXAxisAroundPointTransformation(t7.centroid(), np.pi / 6, 400))
    t7.draw()