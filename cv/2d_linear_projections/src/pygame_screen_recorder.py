"""
Based on https://github.com/solzilberman/pygame_screen_recorder/blob/master/pygame_screen_recorder/pygame_screen_recorder.py

But it keeps the frames in memory only and writes to files in the end to save time on I/O
"""

import imageio 
import os 
import pygame
import io, time

class pygame_screen_recorder:
    def __init__(self, outfile, fps = 10):
        self.outfile = outfile
        self.recorded_frames = []
        self.fps = fps
        self.start_time = time.time()
        self.time_of_last_capture = time.time()

    def click(self, screen):
        if (time.time() - self.time_of_last_capture) > 1 / self.fps:
            image_buffer = io.BytesIO()
            pygame.image.save(screen, image_buffer)
            self.recorded_frames.append(imageio.imread(image_buffer))
            self.time_of_last_capture = time.time()

    def save(self):
        num_seconds = time.time() - self.start_time
        print (f"Saving recording of duration: {num_seconds} seconds with {len(self.recorded_frames) / num_seconds} FPS")
        save_start_time = time.time()
        imageio.mimsave(self.outfile, self.recorded_frames)
        print (f"Saved the recording in {(time.time() - save_start_time) / 60} minutes")