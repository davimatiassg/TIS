#INTRODUÇÃO A SPRITES E ULTILIZAÇÃO DE OBJETOS
import pygame as pg
import ctypes

width = 1200
height = 675

pg.init()

#window = pg.display.set_mode((width, height)) #Width, Height
clock = pg.time.Clock()

ctypes.windll.user32.SetProcessDPIAware()
true_res = (int( ctypes.windll.user32.GetSystemMetrics(0)/(1920/(width))),
            int( ctypes.windll.user32.GetSystemMetrics(1)/(1080/(height))) )
window = pg.display.set_mode(true_res)

RODANDO = True

key = [False,False,False,False]

spr_sla = pg.image.load('Graphics\sla2x.png') #importa uma imagem pro jogo

def sign(value_):
    if value_ != 0:
        return value_/abs(value_)

    return 0

def point_distance(x1,y1,x2,y2):
    return ((x1 - x2)**2 + (y1 - y2)**2)**(1/2)

def friction(speed_,friction_):
    if abs(speed_) > friction_:
        return speed_ - friction_*sign(speed_)
    else:
        return 0

def collision(coord_,spd_,list_,h_ou_v):
    return False


class obj_jogador(object):
    def __init__(self,spr,x,y):
        self.sprite = spr
        self.coll_box = pg.Rect(x,y,spr.get_height(),spr.get_width())
        self.x = x
        self.y = y

        self.hspd = 0
        self.vspd = 0
        self.hacel = 0.17
        self.jump = 2
        self.fric = 0.12
        self.grav = 0.1
        self.on_ground = False

    def step(self):

        self.hspd = friction(self.hspd,self.fric)

        if self.y > height - self.sprite.get_height():
            self.on_ground = True
            self.y = height - self.sprite.get_height()
        else:
            self.on_ground = False

        if self.on_ground == False:
            self.vspd += self.grav
        else:
            if self.vspd > 0:
                self.vspd = 0

        self.x += self.hspd*dt
        self.y += self.vspd*dt

        self.coll_box.x = self.x
        self.coll_box.y = self.y

    def draw(self):
        window.blit(self.sprite, (self.x, self.y))


blocos = []

jogador1 = obj_jogador(spr_sla,0,0)

while RODANDO: #game loop

    dt = clock.tick(64)

    pg.display.set_caption("{}".format(clock.get_fps()))

    window.fill((50, 50, 50)) #cinza escuro

    jogador1.step()
    jogador1.draw()

    for k in range(len(key)):
        if key[k]:
            if k == 0: jogador1.hspd -= jogador1.hacel
            if k == 1: jogador1.hspd += jogador1.hacel
            if jogador1.on_ground == True:
                if k == 2: jogador1.vspd -= jogador1.jump
            if k == 3: jogador1.y += 0

    pg.display.flip() #mostra td oq foi desenhado dentro desse loop

    #um loop que passa por tds os eventos registrados pelo pygame
    #Tipos de eventos: clicar no mouse, apertar algo no teclado, fechar a janela e etc...
    for eventos in pg.event.get():

        if eventos.type == pg.KEYDOWN:

            if eventos.key == pg.K_a:
                key[0] = True
            if eventos.key == pg.K_d:
                key[1] = True
            if eventos.key == pg.K_w:
                key[2] = True
            if eventos.key == pg.K_s:
                key[3] = True

        if eventos.type == pg.KEYUP:

            if eventos.key == pg.K_a:
                key[0] = False
            if eventos.key == pg.K_d:
                key[1] = False
            if eventos.key == pg.K_w:
                key[2] = False
            if eventos.key == pg.K_s:
                key[3] = False

        if eventos.type == pg.QUIT: #evento de fechar a janela
            RODANDO = False


print("jogo finalizado")
