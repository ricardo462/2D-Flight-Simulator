# -*- coding: utf-8 -*-
"""
Created on Fri Oct 23 22:12:16 2020

@author: Ricardo
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

if __name__ == "__main__":

    # Initialize glfw
    if not glfw.init():
        sys.exit()

    width = 600
    height = 600

    window = glfw.create_window(width, height, "2D cars via scene graph", None, None)

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
    
    
    """
    mountain1 = sg.findNode(mountain.model,"mountain")
    mountain1.transform = tr.translate2(mountain1.transform,1.5,0,0)
    """
    
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
        
        
        #mountains.update(dt)
      
        """
        mountain1.transform = tr.translate2(mountain1.transform,posx,0,0)
        sg.drawSceneGraphNode(mountain1, pipeline, "transform")
        """

      
        # Drawing a mountain
        #mountains.printM(pipeline)
        mountains.draw(pipeline)
        
        # Drawing the plane
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