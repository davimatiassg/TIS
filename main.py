#IMPORTS DO JOGO
import pygame as pg
import ctypes
import fs
import math

#SETUP DA TELA (só mexa no width e height)
window_width = 1280
window_height = 720
pg.init()
clock = pg.time.Clock()
ctypes.windll.user32.SetProcessDPIAware()
true_res = (int( ctypes.windll.user32.GetSystemMetrics(0)/(1920/(window_width))),
            int( ctypes.windll.user32.GetSystemMetrics(1)/(1080/(window_height))) )
window = pg.display.set_mode(true_res)

pg.font.init()
fnt_comicsans = pg.font.SysFont('Comic Sans MS', 30)

#VARIAVEIS GLOBAIS
RODANDO = True
key = [False,False,False,False] #lista ulitlizada na movimentação do jogador1
key2 = [False,False,False,False] #lista ulitlizada na movimentação do jogador2
FPS = 64 #ITS 64 BECAUSE YES (dont change)
VERYSMALL = 0.001
VERBIG = 10**5
WHITE = (255,255,255)
BLACK = (0  ,0  ,0  )

#IMPORTANTO SPRITES E ETC GRÁFICOS
spr_homi = [
pg.image.load('Graphics\spr_homi1.png').convert_alpha(),
pg.image.load('Graphics\spr_homi2.png').convert_alpha(),
pg.image.load('Graphics\spr_homi3.png').convert_alpha()]

spr_bloco = pg.image.load('Graphics\sbloco.png').convert_alpha()

#OBJETOS / CLASSES / FUNÇÕES
class obj_jogador(object):
    def __init__(self,spr,x,y):
        #Caracteristicas do obj definidas na criação
        self.sprite = spr
        self.hit_box = pg.Rect(x,y,spr[0].get_height(),spr[0].get_width())
        self.x = x
        self.y = y

        #Caracteristicas gerais do obj
        self.hspeed = 0 #velocidade horizontal
        self.vspeed = 0 #velocidade vertical
        self.speed = 0 #velocidade total
        self.direction = 0 #direção (vetores)
        self.max_hspeed = 5 #velocidade horizontal máxima (em módulo)
        self.lower_max_hspeed = 1 #"walk speed" máxima (em módulo)
        self.max_vspeed = 5 #velocidade vertical máxima (em módulo)
        self.hacel = 0.12 #aceleração horizontal
        self.jump = 2 #aceleração vertical, ou seja, pulo
        self.fric = 0.09 #fricção
        self.grav = 0.1 #gravidade
        self.on_ground = False #boolean: está no chão?
        self.sprite_index = 0 #index atual do sprite
        self.load_sprite_index = 0 #variavel que serve para loopar o sprite_index
        self.last_direction_moved = 1 #Variavel que guarda a última direção que o jogador quiz se mover

    def step(self): #função que executa o cógido geral do jogador

        #Verificando se ele está no chão (da tela)
        if self.y >= window_height - self.hit_box.height:

            #self.y = window_height - self.hit_box.height

            if self.vspeed >= 0:
                self.on_ground = True
            else:
                self.on_ground = False

        else:
            self.on_ground = False


#Atualizando o x,y do jogador com base na velocidade e no lag ( dt )

        #Verificando se ele está colidindo || HORIZONTAL

        #escolhendo o lado para checar a colisão (esquerda ou direita)
        side_ = self.hit_box.x + self.hit_box.width/2*(fs.sign(self.hspeed + VERYSMALL) + 1)

        #Passa por cada ponto (menos os da borda) da parte mais esquerda ou direita do retângulo
        collided_horizontally = False
        for h_ in range(self.hit_box.height):
            var_colisao = fs.collision_list(blocos, (side_ + self.hspeed*dt,self.hit_box.y + h_))

            if var_colisao[0] == True:

                collidee = var_colisao[1] #Colidido da collision_list || "collidee" é o colidido

                #Aproximando ele do pixel mais próximo sem colidir
                i_ = 0
                while collidee.hit_box.collidepoint((side_ + i_,self.hit_box.y + h_)) == False:
                    i_ += fs.sign(self.hspeed*dt)
                self.x += i_

                self.hspeed = 0 #Vc colidiu, Vc perde sua velocidade

                #Exiting loop
                collided_horizontally = True
                break;

        if collided_horizontally == False:
            if self.x + self.hspeed*dt >= 0 and self.x + self.hspeed*dt < window_width - self.hit_box.width:
                self.x += self.hspeed*dt #Atualizando o x normalmente

            else: #Ele sairia da tela :(
                if fs.sign(self.hspeed*dt) < 0:
                    self.x = 0
                else:
                    self.x = window_width - self.hit_box.width

        #Verificando se ele está colidindo || VERTICAL

        #escolhendo o lado para checar a colisão (em cima ou em baixo)
        side_ = self.hit_box.y + (self.hit_box.height/2)*(fs.sign(self.vspeed + VERYSMALL) + 1)

        #Passa por cada ponto (menos os da borda) da parte mais em baixo ou em cima do retângulo
        collided_vertically = False
        for w_ in range(self.hit_box.width - 1):
            var_colisao = fs.collision_list(blocos,(self.hit_box.x + w_ + 1,side_ + self.vspeed*dt))

            if var_colisao[0] == True:
                collidee = var_colisao[1] #Colidido da collision_list || "collidee" é o colidido

                #Aproximando ele do pixel mais próximo sem colidir
                i_ = 0
                while collidee.hit_box.collidepoint((self.hit_box.x + w_ + 1,side_ + i_)) == False:
                    i_ += fs.sign(self.vspeed*dt)
                self.y += i_

                if self.vspeed > 0:
                    self.on_ground = True #Está no chão
                self.vspeed = 0 #Vc colidiu, Vc perde sua velocidade

                #Exiting loop
                collided_vertically = True
                break;

        if collided_vertically == False:
            if self.y + self.vspeed*dt <= window_height - self.hit_box.height:
                self.y += self.vspeed*dt #Atualizando o y normalmente

            else: #Ele ultrapassaria o chão da tela
                self.y = window_height - self.hit_box.height


        #Atualizando o x,y da hitbox do jogador
        self.hit_box.x = self.x
        self.hit_box.y = self.y

        #Atualizando a velocidade || HORIZONTAL
        self.hspeed = fs.friction(self.hspeed,self.fric)
        if abs(self.hspeed) > self.max_hspeed: self.hspeed = self.max_hspeed*fs.sign(self.hspeed) #max speed

        #Atualizando a velocidade || VERTICAL
        if self.on_ground == False:
            self.vspeed += self.grav
        else:
            #certificando que o obj não está acelerando em direção ao chão
            if self.vspeed > 0: self.vspeed = 0

        if abs(self.hspeed) > self.max_hspeed: self.hspeed = self.max_hspeed*fs.sign(self.hspeed) #max speed

        #vetores muahaha
        self.speed = (self.hspeed**2 + self.vspeed**2 )**(1/2)
        self.direction = 360*(1/(2*math.pi))*(self.speed)

    def draw(self): #função que desenha o jogador na tela

        #Animation loop
        if abs(self.hspeed) > 0:
            self.load_sprite_index = fs.loop_value(self.load_sprite_index,0,len(self.sprite) - VERYSMALL,10/FPS)
            self.sprite_index = int(self.load_sprite_index)
        else:
            self.sprite_index = 0

        window.blit(self.sprite[self.sprite_index], (self.x, self.y))

class obj_bloco(object):
    def __init__(self,spr,x,y):
        #Caracteristicas do obj definidas na criação
        self.sprite = spr
        self.hit_box = pg.Rect(x,y,spr.get_height(),spr.get_width())
        self.x = x
        self.y = y

        #Caracteristicas gerais do obj
        #nehuma por enquanto :(

    def draw(self): #função que desenha o obj na tela
        window.blit(self.sprite, (self.x, self.y))

class effect(object):
    def __init__(self,spr,x,y,alive_time,
    speed_ = 0,direction_ = 0):
        #Caracteristicas do obj definidas na criação
        self.sprite = spr
        self.x = x
        self.y = y
        self.alive_time = alive_time #Em frames
        self.speed = speed_
        self.direction = direction_

        #Caracteristicas gerais do obj
    def step(self):
        if self.alive_time > 0:
            self.alive_time -= 1

            self.x += self.speed*math.cos(self.direction*(2*math.pi/360))
            self.y += self.speed*math.sin(self.direction*(2*math.pi/360))

        else:
            efeitos.remove(self)
            efeitos_deposito.append(self)

    def draw(self):
        window.blit(self.sprite, (self.x, self.y))

def draw_text(txt_,x_,y_,
font_ = fnt_comicsans,color_ = WHITE,centered_ = True):
    if centered_ == True: #Centraliza o texto
        x_ -= font_.size(txt_)[0]/2
        y_ -= font_.size(txt_)[1]/2

    text_surface = font_.render(txt_, False, color_)
    window.blit(text_surface,(x_,y_))

def create_effect(sprite_,x_,y_,alive_time_,speed_ = 0,direction_ = 0):
    if len(efeitos_deposito) > 0:
        #Se ja tem um efeito salvo na memoria re-utltilize ele
        efeito_reciclado = efeitos_deposito[0]

        efeito_reciclado.sprite = sprite_
        efeito_reciclado.x = x_
        efeito_reciclado.y = y_
        efeito_reciclado.alive_time = alive_time_
        efeito_reciclado.speed = speed_
        efeito_reciclado.direction = direction_

        efeitos_deposito.pop(0)
        efeitos.append(efeito_reciclado)
    else:
        #cria um efeito novo
        efeitos.append(effect(sprite_,x_,y_,alive_time_,speed_ = speed_,direction_ = direction_))

#CRIANDO OS BLOCOS
blocos = []
blocos.append(obj_bloco(spr_bloco,256,window_height - spr_bloco.get_height()))
blocos.append(obj_bloco(spr_bloco,256,window_height - 64 - spr_bloco.get_height()))
blocos.append(obj_bloco(spr_bloco,256,window_height - 128 - spr_bloco.get_height()))
blocos.append(obj_bloco(spr_bloco,256 + 64,window_height - 128 - spr_bloco.get_height()))
blocos.append(obj_bloco(spr_bloco,256 + 64*2,window_height - 128 - spr_bloco.get_height()))
blocos.append(obj_bloco(spr_bloco,window_width - 256 + 50,window_height - 256 - spr_bloco.get_height()))

#CRIANDO ADEMAIS
efeitos = []
efeitos_deposito = []

#CRIANDO OS JOAGDORES
jogador1 = obj_jogador(spr_homi,0,0)
jogador2 = obj_jogador(spr_homi,100,0)
dash = False
dash2 = False

while RODANDO: #game loop

    dt = clock.tick(FPS) #SETS THE FPS

    pg.display.set_caption("{}".format(clock.get_fps())) #mostra o fps no título da tela

    window.fill((25, 25, 25)) #fundo da tela fica cinza escuro

    draw_text("ROUND 1",window_width/2,64,color_ = (255,0,0))

    #---CODIGO DO JOGADOR
    jogador1.step()
    jogador1.draw()

    jogador2.step()
    jogador2.draw()

    for k in range(len(key)): #movimentando o personagem com base no input
        #k = 0 é A
        #k = 1 é D
        #k = 2 é W
        #k = 3 é S
        if key[k]:
            if k == 0 and jogador1.hspeed > -jogador1.lower_max_hspeed:
                jogador1.hspeed -= jogador1.hacel
                jogador1.last_direction_moved = -1
            if k == 1 and jogador1.hspeed < jogador1.lower_max_hspeed:
                jogador1.hspeed += jogador1.hacel
                jogador1.last_direction_moved = +1

            if jogador1.on_ground == True:
                if k == 2: jogador1.vspeed -= jogador1.jump

            if k == 3: jogador1.y += 0

    for k in range(len(key2)): #movimentando o personagem com base no input
        #k = 0 é A
        #k = 1 é D
        #k = 2 é W
        #k = 3 é S
        if key2[k]:
            if k == 0 and jogador2.hspeed > -jogador2.lower_max_hspeed:
                jogador2.hspeed -= jogador2.hacel
                jogador2.last_direction_moved = -1
            if k == 1 and jogador2.hspeed < jogador2.lower_max_hspeed:
                jogador2.hspeed += jogador2.hacel
                jogador2.last_direction_moved = +1

            if jogador2.on_ground == True:
                if k == 2: jogador2.vspeed -= jogador2.jump

            if k == 3: jogador2.y += 0

    if dash == True:
        jogador1.hspeed += 1.75*jogador1.last_direction_moved

        dir_ = 180*(jogador1.hspeed > 0)

        create_effect(spr_homi[0],jogador1.x,jogador1.y,
        8,speed_ = 10,direction_ = dir_)

        create_effect(spr_homi[0],jogador1.x + 10*fs.sign(jogador1.hspeed),jogador1.y,
        8,speed_ = 9,direction_ = dir_)

        create_effect(spr_homi[0],jogador1.x + 20*fs.sign(jogador1.hspeed),jogador1.y,
        8,speed_ = 8,direction_ = dir_)

        dash = False

    if dash2 == True:
        jogador2.hspeed += 1.75*jogador2.last_direction_moved

        dir_ = 180*(jogador2.hspeed > 0)

        create_effect(spr_homi[0],jogador2.x,jogador2.y,
        8,speed_ = 10,direction_ = dir_)

        create_effect(spr_homi[0],jogador2.x + 10*fs.sign(jogador2.hspeed),jogador2.y,
        8,speed_ = 9,direction_ = dir_)

        create_effect(spr_homi[0],jogador2.x + 20*fs.sign(jogador2.hspeed),jogador2.y,
        8,speed_ = 8,direction_ = dir_)

        dash2 = False

    #---CODIGOS ALEATORIOS
    for f in efeitos:
        f.step()
        f.draw()

    #---CODIGO DOS BLOCOS
    for b in blocos:
        b.draw()


    #FIM DOS DESENHOS NA TELA
    pg.display.flip() #mostra td oq foi desenhado dentro desse loop

    #um loop que passa por tds os eventos registrados pelo pygame
    #Tipos de eventos: clicar no mouse, apertar algo no teclado, fechar a janela e etc...
    for eventos in pg.event.get():

        #APERTOU A TECLA
        if eventos.type == pg.KEYDOWN:

            if eventos.key == pg.K_a:
                key[0] = True
            if eventos.key == pg.K_d:
                key[1] = True
            if eventos.key == pg.K_w:
                key[2] = True
            if eventos.key == pg.K_s:
                key[3] = True
            if eventos.key == pg.K_q:
                dash = True

            if eventos.key == pg.K_LEFT:
                key2[0] = True
            if eventos.key == pg.K_RIGHT:
                key2[1] = True
            if eventos.key == pg.K_UP:
                key2[2] = True
            if eventos.key == pg.K_DOWN:
                key2[3] = True
            if eventos.key == pg.K_KP1:
                dash2 = True

        #SOLTOU A TECLA
        if eventos.type == pg.KEYUP:

            if eventos.key == pg.K_a:
                key[0] = False
            if eventos.key == pg.K_d:
                key[1] = False
            if eventos.key == pg.K_w:
                key[2] = False
            if eventos.key == pg.K_s:
                key[3] = False

            if eventos.key == pg.K_LEFT:
                key2[0] = False
            if eventos.key == pg.K_RIGHT:
                key2[1] = False
            if eventos.key == pg.K_UP:
                key2[2] = False
            if eventos.key == pg.K_DOWN:
                key2[3] = False
            if eventos.key == pg.K_KP1:
                dash2 = False

        #FECHOU A JANELA
        if eventos.type == pg.QUIT:
            RODANDO = False

#FIM
print("jogo finalizado")
