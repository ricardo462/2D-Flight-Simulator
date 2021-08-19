# -*- coding: utf-8 -*-
"""
Created on Tue Oct 20 18:49:45 2020

@author: ricar
"""



import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np
import sys
import time
import random

import transformations as tr
import basic_shapes as bs
import scene_graph as sg
import easy_shaders as es

from model import *
from vista import *

# A class to control the application
class Controller:
    def __init__(self):
        self.leftClickOn = False
        self.theta = 0.0
        self.mousePos = (0.0, 0.0)


# we will use the global controller as communication with the callback function
controller = Controller()


def cursor_pos_callback(window, x, y):
    global controller
    controller.mousePos = (x,y)


def mouse_button_callback(window, button, action, mods):

    global controller

    """
    glfw.MOUSE_BUTTON_1: left click
    glfw.MOUSE_BUTTON_2: right click
    glfw.MOUSE_BUTTON_3: scroll click
    """

    if (action == glfw.PRESS or action == glfw.REPEAT):
     
        (x,y) = (glfw.get_cursor_pos(window))
        
        if 510 <= x <= 538 and 485 <= y <= 505:
            panelButton.changeState("motor",plane, [velocimeter,revolutions, height, pitching])
            
        elif 510 <= x <= 538 and 514 <= y <= 535:
            panelButton.changeState("gassoline", plane, [velocimeter,revolutions, height, pitching])
        
        elif 510 <= x <= 538 and 543 <= y <= 566:
            panelButton.changeState("panelButton",plane, [velocimeter,revolutions, height, pitching])
            
    elif (action ==glfw.RELEASE):
        if (button == glfw.MOUSE_BUTTON_1):
            controller.leftClickOn = False


def scroll_callback(window, x, y):

    print("Mouse scroll:", x, y)



def on_key(window, key, scancode, action, mods):

    #if action != glfw.PRESS:
     #  return

    if key == glfw.KEY_ESCAPE:
        sys.exit()     
    
    elif key == glfw.KEY_W:
        plane.accelerate()            
        plane.accelerateRPM(revolutions.getAngle())
    elif key == glfw.KEY_S:
        plane.decelerate()
        
    elif key == glfw.KEY_UP:
        plane.headUp()

    elif key == glfw.KEY_DOWN:
        plane.headDown()
        
    elif key == glfw.KEY_R:
        panelButton.off("gassoline")
        
    elif key == glfw.KEY_G:
        panelButton.on("gassoline")
        
    


        

    
    
if __name__ == "__main__":

    # Initialize glfw
    if not glfw.init():
        sys.exit()

    width = 600
    height = 600

    window = glfw.create_window(width, height, "Flight simulator", None, None)

    if not window:
        glfw.terminate()
        sys.exit()

    glfw.make_context_current(window)

    # Connecting the callback function 'on_key' to handle keyboard events
    glfw.set_key_callback(window, on_key)
    
    
    # Connecting callback functions to handle mouse events:
    # - Cursor moving over the window
    # - Mouse buttons input
    # - Mouse scroll
    glfw.set_cursor_pos_callback(window, cursor_pos_callback)
    glfw.set_mouse_button_callback(window, mouse_button_callback)
    glfw.set_scroll_callback(window, scroll_callback)

    # Assembling the shader program (pipeline) with both shaders
    pipeline = es.SimpleTransformShaderProgram()
    
    # Telling OpenGL to use our shader program
    glUseProgram(pipeline.shaderProgram)

    # Setting up the clear screen color
    glClearColor(0.85, 0.85, 0.85, 1.0)

    # Creating shapes on GPU memory
    plane = Plane()
    plane.model.transform = tr.translate2(plane.model.transform,-0.7,-0.43,0)
    
    mountains = Mountains()
    clouds = Clouds()
    day = True
    
    mountains.create(day)
    clouds.create()
    board = Board()
    sky = Sky()
    sun = Sun()
    velocimeter = CircleInstrument(-0.7,-0.75,[0,1,2,3,15,16,17])
    revolutions = CircleInstrument(-0.1,-0.75,[15,16,17])
    height = RectangularInstrument(-0.4,-0.75,0.1,0.3,[0,1])
    pitching = RectangularInstrument(0.38,-0.75,0.38,0.3)
    panelButton = PanelButton(0.75,-0.75)
    explosion = Explosion()
    
    
    # Our shapes here are always fully painted
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
    
    t0 = glfw.get_time()
    #mountains.one()
   
    
    while not glfw.window_should_close(window):
        # Using GLFW to check for input events
        glfw.poll_events()

        # Clearing the screen in both, color and depth
        glClear(GL_COLOR_BUFFER_BIT)

        

        mountains.delete()
        number = random.random()
        if number < 0.001:
            day = not day
        mountains.create(day)
        mountains.update(plane.getVelocity()*0.0001*np.cos(plane.angle))
        clouds.delete()
        clouds.create()
        clouds.update(plane.getVelocity()*0.0001*np.cos(plane.angle))
        sky.update(day)
        sky.draw(pipeline)
        sun.draw(pipeline)
        mountains.draw(pipeline)
        plane.update()
        plane.draw(pipeline)
        plane.explode(explosion)
        explosion.update(-0.7, plane.getHeight())
        explosion.draw(pipeline)
        board.draw(pipeline)
        velocimeter.draw(pipeline)
        velocimeter.updateVelocity(plane.getVelocity())
        revolutions.updateVelocity(plane.getRPM())
        revolutions.draw(pipeline)
        plane.decelerateRPM(revolutions.getAngle())
        plane.friction()
        height.draw(pipeline)
        height.updateHeight(plane.getHeight())
        pitching.draw(pipeline)
        pitching.updatePitching(plane.getAngle())
        panelButton.draw(pipeline)
        clouds.draw(pipeline)
        
       
        
        
        

        # Once the render is done, buffers are swapped, showing only the complete scene.
        glfw.swap_buffers(window)
        
        
        
    
    glfw.terminate()
