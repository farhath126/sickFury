import sys
import pygame
from PIL import Image
from core.events import *
from hal.base import DisplayDriver, InputDriver

class PCDisplay(DisplayDriver):
    def __init__(self, width=256, height=128, scale=3):
        self.width = width
        self.height = height
        self.scale = scale
        self.screen = None

    def init(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.width * self.scale, self.height * self.scale))
        pygame.display.set_caption("SickFury Pager - PC Sim")

    def draw_image(self, image: Image.Image):
        if self.screen is None:
            return

        # Convert PIL image to Pygame surface
        # Ensure image is RGB
        if image.mode != "RGB":
            image = image.convert("RGB")
            
        data = image.tobytes()
        py_image = pygame.image.fromstring(data, image.size, "RGB")
        
        # Scale up for readability on PC
        scaled_image = pygame.transform.scale(py_image, 
                                            (self.width * self.scale, self.height * self.scale))
        
        self.screen.blit(scaled_image, (0, 0))
        pygame.display.flip()

    def clear(self):
        if self.screen:
            self.screen.fill((0, 0, 0))
            pygame.display.flip()

class PCInput(InputDriver):
    def init(self):
        # Pygame init is handled in Display, but we can double check
        if not pygame.get_init():
            pygame.init()

    def get_events(self):
        events = []
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                events.append(EVT_QUIT)
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    events.append(EVT_BTN_A) # Scroll / Next
                elif event.key == pygame.K_DOWN:
                    events.append(EVT_BTN_A) # Also Next for convenience in PC sim? No, let's strict 2 button sim.
                    # Actually, if we want "Next", UP/DOWN both doing Next is confusing if we map them physically.
                    # Let's map UP -> A, DOWN -> A (Next)
                    # ENTER -> B (Select)
                    # ESCHEW BACK from keyboard if we want to force 2-button flow?
                    pass 
                elif event.key == pygame.K_RETURN:
                    events.append(EVT_BTN_B)
                elif event.key == pygame.K_z: # Alt for B
                    events.append(EVT_BTN_B)
                elif event.key == pygame.K_x: # Alt for A
                    events.append(EVT_BTN_A)
                elif event.key == pygame.K_ESCAPE:
                    # Keep legacy back for emergencies/dev validation
                    events.append(EVT_BTN_BACK)
                elif event.key == pygame.K_RIGHT:
                     events.append(EVT_KNOB_CW)
                elif event.key == pygame.K_LEFT:
                     events.append(EVT_KNOB_CCW)
        
        return events
