import pygame

COLORS = {
    "red": (255, 0, 0),
    "yellow": (200, 200, 0),
    "black": (0, 0, 0)
}

# this class holds the context defining the pygame screen like height, width, etc.
class PyGameContext:
    def __init__(self, 
                 width=500, 
                 height=500,
                 background_color = (255, 255, 255)):
        pygame.init()

        self.width = width
        self.height = height
        self.background_color = background_color

        # Create the Pygame window
        self.screen = pygame.display.set_mode((width, height))

