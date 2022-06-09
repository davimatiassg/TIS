import pygame as pg
import ctypes
import fs
import os


class Animator:
    def __init__(self, anims, frates, owner, a_type):
        self.owner = owner ## nome do objeto que é animado
        self.names = anims ## nomes de cada uma das animações
        self.current = self.names[0] ## animação tocando atualmente
        self.animations = [] ## lista de objetos da classe "animation" definida abaixo
        self.local = 'Graphics/'+a_type+self.owner
        for i in self.names: ## para cada uma das animações, adiciona uma animação nova
            a_name = self.owner + '_' + i
            self.animations.append(Animation(a_name, frates[self.names.index(i)], self.local, a_type, i + '_'))

    def addAnimation(self, anim, frate): # adicionar uma nova animação, caso necessário
        if anim in self.names:
            self.names[self.name.indes(anim)] = Animation(self.owner + '_' + anim, frate, self.local, a_type, anim + '_')
        else:
            self.animations.append(Animation(self.owner + '_' + anim, frate, self.local, a_type, anim + '_'))

    def getCurrentFrame(self): ## retorna o sprite rodando atualmente
        return self.animations[self.names.index(self.current)].playActualFrame()

    def play(self, a): ##roda uma animação
        if a in self.names:
        	b = self.current
        	self.current = a
        	if b == self.current:
        		return self.animations[self.names.index(a)].play()
        	else:
        		return self.animations[self.names.index(a)].playFrame(0)

    def playFrame(self, a, i): ## retorna um frame específico de uma animação
        if a in self.names:
            self.current = a
            return self.animations[self.names.index(a)].playFrame(i)

    def clearAnim(self):
        self.names = ['blank']
        self.current = self.names[0]
        self.animations = [blankAnim()]
        self.local = ''
        return self

class Animation: ## classe que armazena animações

    def __init__(self, name, fps, folder, a_type, prefix): ##
        self.name = name
        self.frames = []
        self.valid = False
        self.idx = 0
        listd = os.listdir(folder + '/')
        listd.sort(key=fLen)
        for f in listd:
            if (f.endswith(".png") and f.startswith(prefix)):
            	self.frames.append(pg.image.load(folder + '/'+f).convert_alpha())
            	if len(self.frames) == 1:
            		self.valid = True
        self.fps = fps

    def play(self): #roda a animação na velocidade normal
        if(self.valid):
            self.idx = fs.loopAnim(self.idx, 0, len(self.frames)-1, self.fps/65)
            #self.idx = fs.loopValue(self.idx, 0, len(self.frames) - 0.01, self.fps/65)
            print(self.idx)
            return self.frames[int(self.idx)]

    def playFrame(self, i): #retorna um frame específico da animação
        if(self.valid):
            self.idx = int(i)
            return self.frames[int(self.idx)]

    def playActualFrame(self): #retorna o frame atual da animação
        if(self.valid):
            return self.frames[int(self.idx)]

class blankAnim(Animation):
    def __init__(self, *args):
        self.name = 'blank'
        img = pg.Surface((0, 0))
        self.frames = [img]
        self.valid = True
        self.idx = 0
        self.fps = 0

    def play(self):
        return self.frames[0]

    def playFrame(self, i):
        return play(self)

    def playActualFrame(self):
        return play(self)

def fLen(e):
  return len(e)