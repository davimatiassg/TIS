import pygame as pg
import ctypes
import fs
import os

class Animation:

    def __init__(self, name, fps, folder, prefix):
        self.name = name
        self.frames = []
        self.valid = False
        self.current = 0
        for f in os.listdir(folder):
            if (f.endswith(".png") and f.startswith(prefix)):
                
                self.frames.append(pg.image.load(f).convert_alpha())
                if len(self.frames) == 1:
                    self.current = self.frames[0]
                    self.valid = True
        self.fps = fps
        

    def play(self):
        if(self.valid):
            self.current = int(fs.loopValue(self. current, 0, len(self.frames), 64/fps))
            return self.frames[self.current]

class Animator:
     def __init__(self, anims, owner):
         self.owner = owner
         self.names = anims
         self.animations = []
         for i in self.names:
             self.animations.append(Animation(self.owner + '_' + i, 16, 'Graphics\\'+self.owner, i + '_'))

    def addAnimation(self, anim):
        if anim in self.names:
            self.names[self.name.indes(anim)] = Animation(self.owner + '_' + anim, 16, 'Graphics\\'+self.owner, anim + '_')
        else:
            self.animations.append(Animation(self.owner + '_' + anim, 16, 'Graphics\\'+self.owner, anim + '_'))
        
    def play(self, a):
        if a in names:
            return self.animations[names.index(a)].play()
