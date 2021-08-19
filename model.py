# -*- coding: utf-8 -*-
"""
Created on Fri Oct 23 22:05:05 2020

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

class Mountain:

    def __init__(self,day):
        if day:
            (r,g,b) = (0,np.random.uniform(0.4,1,1),0)
        else:
            (r,g,b) = (np.random.uniform(0.2,0.7),np.random.uniform(0,0.3),0)
        gpuTriangle = es.toGPUShape(bs.createColorTriangle(r,g,b))
        
        mountain = sg.SceneGraphNode("mountain")
        mountain.transform = tr.translate2(mountain.transform,1.5,0,0)
        
        mountain.childs += [gpuTriangle]
        self.model = mountain
        
    def draw(self, pipeline):
        sg.drawSceneGraphNode(self.model, pipeline, "transform")
        
    def update(self,dt):
        self.model.transform = tr.translate2(self.model.transform,-dt,0,0)

class Mountains:
    
    def __init__(self):
        self.mountains = np.array([])
        
        
    def draw(self, pipeline):
        for k in self.mountains:
            k.draw(pipeline)
    
    def create(self,day):
        if len(self.mountains) >=10:
            return
        num = np.random.random()
        if num <0.05:
            self.mountains = np.append(self.mountains, Mountain(day))
            
    def delete(self):
        remain_mountains = np.array([])
        for i in self.mountains:
            matrix = i.model.transform
            x = matrix[0,3]
            if x>-1.5:
                remain_mountains = np.append(remain_mountains,i)
                
        self.mountains = remain_mountains
        
   
        
    def update(self, dt):
        for k in self.mountains:
            k.update(dt)
            
    def getMountains(self):
        return self.mountains
    
    def one(self):
        self.mountains = Mountain()
        
    def printM(self,pipeline):
        self.mountains.draw(pipeline)
        
class Sky:
    def __init__(self):
        gpuLightBlueQuad = es.toGPUShape(bs.createColorQuad(0,0.7,0.8))
        gpuOrangeQuad = es.toGPUShape(bs.createColorQuad(1,0.5,0))
        
        sky =sg.SceneGraphNode(("sky"))
        sky.transform = tr.scale(2,2,1)
        sky.transform = tr.translate2(sky.transform,0,0.5,0)
        sky.childs += [gpuLightBlueQuad]
        
        self.model = sky
        self.lightBlueQuad = gpuLightBlueQuad
        self.orangeQuad = gpuOrangeQuad
    
    def draw(self,pipeline):
        sg.drawSceneGraphNode(self.model, pipeline, "transform")
    
    def update(self, day):
        node = sg.findNode(self.model, "sky")
        
        if day:
            node.childs = [self.lightBlueQuad]
        else:
            node.childs = [self.orangeQuad]
        
class Sun:
    
    def __init__(self):
        gpuYellowCircle = es.toGPUShape(bs.createColorCircle(40, 1, 1, 0))
        
        sun = sg.SceneGraphNode("sun")
        sun.transform = tr.translate(0, -0.5, 0)
        sun.childs += [gpuYellowCircle]
        
        self.model = sun
        
    def draw(self, pipeline):
        sg.drawSceneGraphNode(self.model, pipeline, "transform")
        
class Cloud:
    
    def __init__(self):
        
        gpuCircle = es.toGPUShape(bs.createColorCircle(40, 0.9, 0.9, 0.9))
        
        cloud = sg.SceneGraphNode("cloud")
        
        
        circles = []
        for i in range(15):
            numbers = []
            for j in range(3):
                numbers.append(np.random.uniform(0.3,1))
            for j in range(3):
                numbers.append(np.random.uniform(0,0.2))
            
            circles += [sg.SceneGraphNode("circle" + str(i))]
            circles[i].transform = tr.translate3(*numbers)
            circles[i].childs += [gpuCircle]
            
        y = np.random.uniform(0,0.5)
        cloud.transform = tr.translate3(1,0.3,1,1.5,y,0)
    
        for i in range(5):
            cloud.childs += [circles[i]]
            
        self.model = cloud
        
    def draw(self, pipeline):
        sg.drawSceneGraphNode(self.model, pipeline, "transform")
        
    def update(self,dt):
        self.model.transform = tr.translate2(self.model.transform,-dt,0,0)
        
class Clouds:
    
    def __init__(self):
        self.clouds = np.array([])
        
        
    def draw(self, pipeline):
        for k in self.clouds:
            k.draw(pipeline)
    
    def create(self):
        if len(self.clouds) >=10:
            return
        num = np.random.random()
        if num <0.004:
            self.clouds = np.append(self.clouds, Cloud())
            
    def delete(self):
        remain_clouds = np.array([])
        for i in self.clouds:
            matrix = i.model.transform
            x = matrix[0,3]
            if x>-1.5:
                remain_clouds = np.append(remain_clouds,i)
                
        self.clouds = remain_clouds
        
    def update(self, dt):
        for k in self.clouds:
            k.update(dt)
            
    
    
    
      


        

class Plane:
    
    def __init__(self):
    
        gpuGrayQuad = es.toGPUShape(bs.createColorQuad(0.7,0.7,0.7))
        gpuBlueQuad = es.toGPUShape(bs.createColorQuad(0,0,1))
        gpuGrayETriangle = es.toGPUShape(bs.createColorETriangle(0.7,0.7,0.7))
        gpuGrayRectangleTriangle = es.toGPUShape(bs.createColorRectangleTriangle(0.7,0.7,0.7))
        gpuBlueRectangleTriangle = es.toGPUShape(bs.createColorRectangleTriangle(0,0,1))
        gpuDarkGrayQuad = es.toGPUShape(bs.createColorQuad(0.6,0.6,0.6))
        
        # Creating a window
        window = sg.SceneGraphNode("window")
        window.transform = tr.scale(-0.1,0.15,0)
        window.childs += [gpuBlueQuad]
        
        # Instanciating 3 windows
        frontWindow = sg.SceneGraphNode("frontWindow")
        frontWindow.transform = tr.translate(0.4,0.1,0)
        frontWindow.childs += [window]
    
        mediumWindow = sg.SceneGraphNode("backWindow")
        mediumWindow.transform = tr.translate(0.1,0.1,0)
        mediumWindow.childs += [window]
    
        backWindow = sg.SceneGraphNode("backWindow")
        backWindow.transform = tr.translate(-0.1,0.1,0)
        backWindow.childs += [window]
        
        # Creating a triangular window
        scaledTriangularWindow =sg.SceneGraphNode("ScaledTriangularWindow")
        scaledTriangularWindow.transform = tr.uniformScale(0.2)
        scaledTriangularWindow.childs += [gpuBlueRectangleTriangle]
        
        triangularWindow = sg.SceneGraphNode("triangularWindow")
        triangularWindow.transform = tr.translate(0.6,0.12,0)
        triangularWindow.childs += [scaledTriangularWindow]
        
        # Creating the back wing of the plane
        
        backWing = sg.SceneGraphNode("backWing")
        backWing.transform = tr.translate(-1.17,1.3,0)
        backWing.childs += [gpuGrayRectangleTriangle]    
    
        wing = sg.SceneGraphNode("wing")
        wing.transform = tr.uniformScale(0.3)
        wing.childs += [backWing]
    
    
        # Creating the side wing of the plane
        scaledSideWing = sg.SceneGraphNode("rotatedSideWing")
        scaledSideWing.transform = tr.scale(0.2,0.6,0)
        scaledSideWing.childs += [gpuDarkGrayQuad]
    
        rotatedSideWing = sg.SceneGraphNode("rotatedSideWing")
        rotatedSideWing.transform = tr.rotationZ(np.pi/1.65)
        rotatedSideWing.childs += [scaledSideWing]
        
        sideWing = sg.SceneGraphNode("sideWing")
        sideWing.transform = tr.translate(0.05,-0.1,0)
        sideWing.childs += [rotatedSideWing]
        
        # Creating the cabin of the plane
        
        rotatedCabin = sg.SceneGraphNode("rotatedCabin")
        rotatedCabin.transform = tr.rotationZ(np.pi/6)
        rotatedCabin.childs += [gpuGrayETriangle]
            
        scaledCabin = sg.SceneGraphNode("scaledCabin")
        scaledCabin.transform = tr.uniformScale(0.5)
        scaledCabin.childs += [rotatedCabin]
        
        cabin = sg.SceneGraphNode("cabin")
        cabin.transform = tr.translate(0.59,0.09,0)
        cabin.childs += [scaledCabin]   
        
    
        # Creating the chasis of the plane
        chasis = sg.SceneGraphNode("chasis")
        chasis.transform = tr.scale(1,0.5,1)
        chasis.childs += [gpuGrayQuad]
    
    
        plane = sg.SceneGraphNode("plane")
        plane.transform = tr.uniformScale(0.3)
        plane.childs += [chasis]
        plane.childs += [cabin]
        plane.childs += [backWindow]
        plane.childs += [mediumWindow]
        plane.childs += [frontWindow]
        plane.childs += [triangularWindow]
        plane.childs += [wing]
        plane.childs += [sideWing]
    
        self.model = plane
        self.angle = 0.01 
        self.velocity = 0
        self.freeFall = False
        self.time = 0
        self.ground = True
        self.RPM = 0
        self.on = True
        self.explosion = False

        
    def draw(self, pipeline):
        sg.drawSceneGraphNode(self.model, pipeline, "transform")

    def moveRight(self):
        self.model.transform = tr.translate2(self.model.transform,0.1,0,0)
    
    def moveLeft(self):
        self.model.transform = tr.translate2(self.model.transform,-0.1,0,0)

    def moveUp(self):
        self.model.transform = tr.translate2(self.model.transform,0,0.1,0)

    def moveDown(self):
        self.model.transform = tr.translate2(self.model.transform,0,-0.1,0)
        
    def headUp(self):
        if self.on:
            if self.ground:
                if self.getHeight() >= -0.435 and self.velocity>=50:
                    self.angle += 0.04
                    self.model.transform = tr.rotationZ3(self.model.transform,self.angle)
            else:
                self.angle += 0.04
                self.model.transform = tr.rotationZ3(self.model.transform,self.angle)
             
    def headDown(self):
        if self.on:
            if self.ground:
                if self.getHeight() >= -0.435 and self.velocity>=50:
                    self.angle += 0.04
                    self.model.transform = tr.rotationZ3(self.model.transform,self.angle)
            else:
                self.angle -=0.04
                self.model.transform = tr.rotationZ3(self.model.transform,self.angle)
        
        
    def accelerate(self):
        if self.on:
            if self.velocity <= 360:
                self.velocity +=0.5
                
    def accelerateRPM(self,angle):
        if self.on:
            if angle>-np.pi*1.7:
                self.RPM +=10
                
        
    def decelerateRPM(self,angle):
        if angle<=0:
            self.RPM -=1
    
    def decelerate(self):
        if self.on:
            self.velocity -=0.2
        
    def friction(self):
        if self.velocity > 0:
            self.velocity -= 0.02
            if self.velocity > 340:
                self.velocity -= 5
        elif self.velocity <0:
            self.velocity += 0.02
        
        if self.getHeight()>0.65:
            if self.velocity >= 0:
                self.velocity -= np.sin(self.angle)
        # Gravity
        if self.angle <= 0:
            self.velocity += np.sin(-self.angle)*0.5
    
    def getVelocity(self):
        return self.velocity
    
    def getHeight(self):
        return self.model.transform[1,3]
    
    def getRPM(self):
        return self.RPM
    
    def getAngle(self):
        return self.angle
    
    def update(self):
        g = 9.8
        if not self.explosion:
            if self.getHeight()<= -0.43:
                self.ground = True
            else:
                self.ground = False
            if self.velocity >=50:
                self.freeFall = False
                self.model.transform = tr.translate2(self.model.transform,0,0.00005*np.sin(self.angle)*self.velocity,0)
            
            elif self.model.transform[1,3] >= -0.43 and self.velocity < 50:
                if not self.freeFall:
                    self.time = 0
                self.freeFall = True
                dy = 0.5*g*self.time**2
                self.model.transform = tr.translate2(self.model.transform,0,-dy ,0)
                self.time += 0.0001
        
        if self.explosion:
            if self.velocity >= 0:
                if self.velocity <= 2:
                    self.velocity = 0
                self.velocity -= 1
            if self.getHeight() >= -0.43:
                self.model.transform = tr.translate2(self.model.transform,0,-0.01,0)
            
    
    def explode(self, explosion):
        if self.getHeight() <= -0.4311:
            explosion.explode(-0.7,self.getHeight())
            self.on = False
            self.explosion = True
            
        if self.velocity >= 320:
            num = random.random()
            if num*self.velocity >333: 
                explosion.explode(-0.7,self.getHeight())
                self.on = False
                self.explosion = True
        
class Board:
    
    def __init__(self):
        gpuRectangle = es.toGPUShape(bs.createColorQuad(0, 0, 0))
        
        board = sg.SceneGraphNode("board")
        board.transform = tr.translate3(2, 0.5, 1, 0, -0.75, 0)
        board.childs += [gpuRectangle]
        self.model = board
        
    def draw(self,pipeline):
        sg.drawSceneGraphNode(self.model, pipeline, "transform")
        
        
        
class Circle:
    def __init__(self,x,y):
        
        gpuCircle = es.toGPUShape(bs.createColorCircle(40,0.9,0.9,0.9))
        circle = sg.SceneGraphNode("circle")
        circle.transform = tr.uniformScale(0.3)
        circle.transform = tr.translate2(circle.transform,x,y,0)
        circle.childs += [gpuCircle]
        self.model = circle
    
    def draw(self,pipeline):
        sg.drawSceneGraphNode(self.model, pipeline, "transform")
        
    
        
class CircleInstrument:
    def __init__(self,x,y,limits=[]):
        
        gpuBlackRectangle = es.toGPUShape(bs.createColorQuad(0,0,0))
        gpuRedRectangle = es.toGPUShape(bs.createColorQuad(1,0,0))
        gpuGrayCircle = es.toGPUShape(bs.createColorCircle(40,1,1,1))
        
        # Creating the main circle
        circle = sg.SceneGraphNode("circle")
        circle.childs += [gpuGrayCircle]
        
        indices =[]
        # Creating the indices
        for i in range(18):
            indices.append(sg.SceneGraphNode("indice"+str(i)))
            #indices[i].transform = tr.scale(2,0.2,1)
            #indices[i].transform = tr.translate2(indices[i].transform,0,0.3,0)
            if i in limits:
                indices[i].childs += [gpuRedRectangle]
            else:
                indices[i].childs += [gpuBlackRectangle]
            
        # Creating the needle
        needle = Needle()
        needle.model.transform = tr.translate2(needle.model.transform,0,0.25,0)
        
        
        # Assembling the circle instrument
        circleInstrument = sg.SceneGraphNode("circleInstrument")
        circleInstrument.transform = tr.translate2(circle.transform,x/0.3,y/0.3,0)
        circleInstrument.childs += [circle]       
        for i in range(18):
            circleInstrument.childs += [indices[i]]
        circleInstrument.childs += [needle.model]
        
        # Rotating the indices
        for i in range(18):
            node = sg.findNode(circleInstrument,"indice"+str(i))
            node.transform = tr.rotationZ2(node.transform,-i*np.pi/9)
        
        # Scaling instrument
        scaledInstrument = sg.SceneGraphNode("scaledInstrument")
        scaledInstrument.transform = tr.uniformScale(0.3)
        scaledInstrument.childs += [circleInstrument]
        
        
    
        self.model = scaledInstrument
        self.angle = 0
        self.on = True
                
    def draw(self, pipeline):
        sg.drawSceneGraphNode(self.model, pipeline, "transform")
        
    def updateVelocity(self, velocity):
        if self.on:
            node = sg.findNode(self.model,"needle")
            self.angle = -velocity*np.pi/(180)
            node.transform = tr.rotationZ4(node.transform,self.angle,0.2,0.1,0.5)
        
    def updateHeight(self,height):
        if self.on:
            node = sg.findNode(self.model, "needle")
            angle = self.heightAngle(height)
            node.transform = tr.rotationZ4(node.transform,-angle,0.2,0.1,0.5)
        
   
    def heightAngle(self,height):
        m = (2*np.pi)/1.33
        return m*(height+0.43)
    
    def getAngle(self):
        return self.angle
    
class Needle:
    def __init__(self):
        gpuRedTriangle = es.toGPUShape(bs.createColorTriangle(1,0,0))
        
        needle = sg.SceneGraphNode("needle")
        needle.transform = tr.scale(0.1,0.5,1)
        needle.childs += [gpuRedTriangle]
        self.model = needle
    
    def draw(self,pipeline):
        sg.drawSceneGraphNode(self.model, pipeline, "transform")
        
class RectangularInstrument:
    def __init__(self,x,y,sx,sy,limits =[]):
        gpuGrayRectangle = es.toGPUShape(bs.createColorQuad(0.9,0.9,0.9))
        gpuBlackRectangle = es.toGPUShape(bs.createColorQuad(0,0,0))
        gpuRedRectangle = es.toGPUShape(bs.createColorQuad(1,0,0))
        
        
        #Creating a border
        rightBorder = sg.SceneGraphNode("rightBorder")
        rightBorder.transform = tr.scale(0.01,1,1)
        rightBorder.transform = tr.translate2(rightBorder.transform,0.55,0,0)
        rightBorder.childs += [gpuBlackRectangle]
        
        leftBorder = sg.SceneGraphNode("leftBorder")
        leftBorder.transform = tr.scale(0.01,1,1)
        leftBorder.transform = tr.translate2(leftBorder.transform,-0.55,0,0)
        leftBorder.childs += [gpuBlackRectangle]
        
        upBorder = sg.SceneGraphNode("upBorder")
        upBorder.transform = tr.scale(1.1,0.01,1)
        upBorder.transform = tr.translate2(upBorder.transform,0,0.505,0)
        upBorder.childs += [gpuBlackRectangle]
        
        downBorder = sg.SceneGraphNode("downBorder")
        downBorder.transform = tr.scale(1.1,0.01,1)
        downBorder.transform = tr.translate2(downBorder.transform,0,-0.505,0)
        downBorder.childs += [gpuBlackRectangle]
        
        indices = []
        for i in range(6):
            indice = sg.SceneGraphNode("indice"+str(i))
            indice.transform = tr.scale(0.8,0.03,1)
            if i in limits:
                indice.childs += [gpuRedRectangle]
            else:
                indice.childs += [gpuBlackRectangle]
            indices += [indice]
            
        needle = sg.SceneGraphNode("needle")
        needle.transform = tr.scale(0.8,0.05,1)
        needle.childs += [gpuRedRectangle]
           
        
        scaledRectangle = sg.SceneGraphNode("scaledRectangle")
        scaledRectangle.childs += [gpuGrayRectangle]
        
        base = sg.SceneGraphNode("base")
        base.transform = tr.scale(sx,sy,1)
        base.transform = tr.translate2(base.transform,x,y,0)
        base.childs += [rightBorder]
        base.childs += [leftBorder]
        base.childs += [upBorder]
        base.childs += [downBorder]
        base.childs += [scaledRectangle]
        for i in range(6):
            indices[i].transform = tr.translate2(indices[i].transform,0,0.4-0.16*i,0)
            base.childs += [indices[i]]
        base.childs += [needle]

        
        self.model = base
        self.on = True
        
    def draw(self,pipeline):
        sg.drawSceneGraphNode(self.model, pipeline, "transform")
        
    
    def updateHeight(self,height):
        if self.on:
            if height >=0.9:
                Height = 0.43
            elif height <= -0.43:
                Height = -0.43
            else:
                Height = self.functionHeight(height)
            node = sg.findNode(self.model,"needle")
            node.transform = tr.translate3(0.8,0.05,1,0, Height,0)
        
    def updatePitching(self,angle):
        if self.on:
            (x,y) = self.functionAngle(angle)
            node = sg.findNode(self.model, "needle")
            node.transform = tr.translate3(0.1,0.1,1,x,y,0)
        

        
    def functionHeight(self,height):
        m = 0.86/1.33
        return m*(height+0.43)-0.43
    
    def functionAngle(self, angle):
        y = 0.43*np.sin(angle)
        x = 0.35*np.cos(angle)
        return (x,y)
    
    
class Button:
    
    def __init__(self,x,y,name):
        
        gpuRedQuad = es.toGPUShape(bs.createColorQuad(1,0,0))
        gpuGreenQuad = es.toGPUShape(bs.createColorQuad(0,1,0))
        
        button = sg.SceneGraphNode(name)
        button.transform = tr.translate3(0.3,0.3,1,x,y,0)
        button.childs += [gpuGreenQuad]
        self.model = button
        self.gpuRedQuad = gpuRedQuad
        self.gpuGreenQuad = gpuGreenQuad
        
    def draw(self, pipeline):
        sg.drawSceneGraphNode(self.model, pipeline, "transform")
        
    def on(self):
        node = sg.findNode(self.model,"button")
        node.childs = [self.gpuGreenQuad]
        
    def off(self):
        node = sg.findNode(self.model,"button")
        node.childs = [self.gpuRedQuad]
        

class PanelButton:
    
    def __init__(self,x,y):
        
        gpuGrayQuad = es.toGPUShape(bs.createColorQuad(0.5,0.5,0.5))
        
        grayPanel = sg.SceneGraphNode("grayPanel")
        grayPanel.transform = tr.scale(0.55,1.3,0)
        grayPanel.childs += [gpuGrayQuad]
        
        motor = Button(0,0.4,"motor")
        gassoline = Button(0,0,"gassoline")
        controlButton = Button(0,-0.4,"panelButton")
        
        panel = sg.SceneGraphNode("panel")
        panel.transform = tr.translate3(0.3,0.25,1,x,y,0)
        panel.childs += [grayPanel]
        panel.childs += [motor.model, gassoline.model, controlButton.model]
        
        self.model = panel
        self.gpuRedQuad = es.toGPUShape(bs.createColorQuad(1,0,0))
        self.gpuGreenQuad = es.toGPUShape(bs.createColorQuad(0,1,0))
        self.stateMotor = True
        self.stateGassoline = True
        self.statePanelButton = True
    
    def draw(self,pipeline):
        sg.drawSceneGraphNode(self.model, pipeline, "transform")
        
    def on(self,button, plane, instruments):
        node = sg.findNode(self.model,button)
        node.childs = [self.gpuGreenQuad]
        
        if button == "motor" or button == "gassoline":
            plane.on = True
            
        elif button == "panelButton":
            plane.RPM = 0
            for i in range(len(instruments)):
                instruments[i].on = True
        
    def off(self, button, plane, instruments):
        node = sg.findNode(self.model, button)
        node.childs = [self.gpuRedQuad]
        
        if button == "motor" or button == "gassoline":
            plane.on = False
        
        elif button == "panelButton":
            for i in range(len(instruments)):
                instruments[i].on = False
            
        
    def changeState(self, button, plane, instruments):
        if self.state(button):
            self.off(button, plane, instruments)
        else:
            self.on(button, plane, instruments)
        
    
    def state(self, button):
        if button == "motor":
            state = self.stateMotor
            self.stateMotor = not self.stateMotor

        elif button == "gassoline":
            state = self.stateGassoline
            self.stateGassoline = not self.stateGassoline

        elif button == "panelButton":
            state = self.statePanelButton
            self.statePanelButton = not self.statePanelButton
        
        return state

class Explosion:
    
    def __init__(self):
        
        gpuRedTriangle = es.toGPUShape(bs.createColorTriangle(1,0,0))
        gpuYellowTriangle = es.toGPUShape(bs.createColorTriangle(1,1,0))
        
        redExplosion = sg.SceneGraphNode("redExplosion")
        yellowExplosion = sg.SceneGraphNode("yellowExplosion")
        yellowExplosion.transform = tr.uniformScale(0.7)
              
        
        redTriangles = []
        yellowTriangles = []
        for i in range(15):
            numbers = []
            angle = np.random.uniform(0,2*np.pi)
            
            redTriangle = sg.SceneGraphNode("redTriangle")
            redTriangle.transform = tr.rotationZ(angle)
            redTriangle.childs += [gpuRedTriangle]
            
            yellowTriangle = sg.SceneGraphNode("yellowTriangle")
            yellowTriangle.transform = tr.rotationZ(angle)
            yellowTriangle.childs += [gpuYellowTriangle]
            
            for j in range(3):
                numbers.append(np.random.uniform(0.3,1))
            for j in range(3):
                numbers.append(np.random.uniform(0,0.2))
            
            redTriangles += [sg.SceneGraphNode("redTriangle" + str(i))]
            redTriangles[i].transform = tr.translate3(*numbers)
            
            yellowTriangles += [sg.SceneGraphNode("yellowTriangle" + str(i))]
            yellowTriangles[i].transform = tr.translate3(*numbers)
            
            redTriangles[i].childs += [redTriangle]
            yellowTriangles[i].childs += [yellowTriangle]
          
        
            
        for i in range(5):
            redExplosion.childs += [redTriangles[i]]
            yellowExplosion.childs += [yellowTriangles[i]]
            
        explosion = sg.SceneGraphNode("explosion")
        explosion.childs += [redExplosion]
        explosion.childs += [yellowExplosion]
    
    
        self.model = explosion
        self.explosion = False
        
    def draw(self,pipeline):
        if self.explosion:
            sg.drawSceneGraphNode(self.model, pipeline, "transform")
            
    def explode(self, x, y):
        self.model.transform = tr.translate(x, y, 0)
        self.explosion = True
        
    def update(self,x,y):
        self.model.transform = tr.translate(x,y,0)
        
        