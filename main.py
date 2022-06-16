#IMPORTS DO JOGO
import pygame as pg
import ctypes
import fs
import math
import animation as an
import random
import chardata as chd
import projection as pj
import cards_txt as ctxt
import time
from tiles import *
#SETUP DA TELA (só mexa no width e height)
pg.init()
clock = pg.time.Clock()
ctypes.windll.user32.SetProcessDPIAware()
window_width = ctypes.windll.user32.GetSystemMetrics(0)
window_height = ctypes.windll.user32.GetSystemMetrics(1)
window = pg.display.set_mode((window_width,window_height),pg.FULLSCREEN)

#window = pg.image.load('Graphics/level_forest/f.png').convert_alpha()

pg.font.init()
fnt_comicsans = [ # FONT SIZES
pg.font.SysFont('Comic Sans MS', 25),
pg.font.SysFont('Comic Sans MS', 30),
pg.font.SysFont('Comic Sans MS', 35),
pg.font.SysFont('Comic Sans MS', 30),
pg.font.SysFont('Comic Sans MS', 45)
]
fnt_comicsans_Vspace = [30,40,50,60,70]

#VARIAVEIS GLOBAIS
room_width = 1600 #1280
room_height = 900 #720
rel_width = window_width - room_width
rel_height = window_height - room_height
raz = window_width/room_width
RODANDO = True
key = [False,False,False,False]       #lista ulitlizada na movimentação do jogador1
act = [False, False]                         #lista ulitlizada nos ataques do jogador1
key2 = [False,False,False,False]     #lista ulitlizada na movimentação do jogador2
act2 = [False, False]                       #lista ulitlizada nos ataques do jogador2
FPS = 65 #ITS 64 BECAUSE YES (dont change)
VERYSMALL = 0.001
VERBIG = 10**5
WHITE = (255,255,255)
BLACK = (0  ,0  ,0  )
RED = (255  ,0  ,0  )
GREEN = (0  ,255  ,0  )
BLUE = (0  ,0  ,255  )
txt_de_22c = "abcdefghijklmnopqrstuv"
VOLUME_DO_JOGO = 1 # 0 a 1

LISTA_DE_CARTAS = []
USED_CARDS = []

for i in ctxt.CARDS_DESCRIPTIONS:
    if i != None:
        LISTA_DE_CARTAS.append(i)

print(LISTA_DE_CARTAS)

#IMPORTANTO SPRITES, SONS e ETC

#spr_homi = [
#pg.image.load('Graphics\spr_homi1.png').convert_alpha(),
#pg.image.load('Graphics\spr_homi2.png').convert_alpha(),
#pg.image.load('Graphics\spr_homi3.png').convert_alpha()]


spr_bloco = pg.image.load('Graphics\sbloco.png').convert_alpha()

spr_cursor = pg.image.load('Graphics\coord.png').convert_alpha()

snd_sound = pg.mixer.Sound("z4.wav")

#OBJETOS / CLASSES / FUNÇÕES
class obj_jogador(object):
    def __init__(self, char, x, y, player_, frates = [8, 12, 16, 16, 32, 20, 32, 8], offset = [0, 0]):
        #Caracteristicas do obj definidas na criação
        self.char = char
        self.player_ = player_
        self.sc = 1.75
        self.offset = offset

        moves = ['idle', 'run', 'jump', 'tkdmg', 'atk', 'D_atk', 'A_atk', 'Crouch']
        #Framerate[8,     12,     16,     16,     32,     20,       32,      8]
        self.anim = an.Animator(moves, frates, char, 'char_')
        self.current_spr = self.anim.play('idle')

        self.hit_box = pg.Rect(x,y,55*self.sc, 55*self.sc)
        self.x = x
        self.y = y
        self.start_x = x
        self.start_y = y

        #Caracteristicas gerais do obj
        self.Hp = 50 #Vida
        self.maxHp = self.Hp
        self.Atk = 4 #Dano
        self.AtkRange = 8 #Range do Atk
        self.hspeed = 0 #velocidade horizontal
        self.vspeed = 0 #velocidade vertical
        self.speed = 0 #velocidade total
        self.direction = 0 #direção (vetores)
        self.max_hspeed = 5 #velocidade horizontal máxima (em módulo)
        self.lower_max_hspeed = 0.9 #"walk speed" máxima (em módulo)
        self.max_vspeed = 5 #velocidade vertical máxima (em módulo)
        self.hacel = 0.14 #aceleração horizontal
        self.jump = 1.6 #aceleração vertical, ou seja, pulo
        self.fric = 0.1 #fricção
        self.grav = 0.075 #gravidade
        self.on_ground = False #boolean: está no chão?
        self.unabletime = 0 #tempo de atordoamento/imobilização restante
        self.invtime = 0 #tempo de invulnerabilidade restante
        self.sprite_index = 0 #index atual do sprite
        self.load_sprite_index = 0 #variavel que serve para loopar o sprite_index
        self.last_direction_moved = 1 #Variavel que guarda a última direção que o jogador quiz se mover
        self.dash_cooldown = 0 #variavel que da um tempo pro dash ser usando dnv
        self.dash_time = 40 #de qnt em qnt tempo o dash pode ser usado
        self.atk_cooldown = 0          #Armazena o tempo restante até poder usar o próximo ataque
        self.atk_delay = 16 # tempo inicial para o próximo ataque, em frames (meio segundo a 64 fps).
        self.knockback = 1.25 #knockback aplicado ao inimigo
        self.knockresi = 1 #resistência ao knockback: 1 = nenhuma resitência; 2 = 50% resistência; 3 = 66% de resistência e assim por diante.
        self.enemy = self #Plottwistico
        self.isAtacking = False  #está atacando?
        self.isCrouch = False #está agachado?
        #CARDs stuff
        self.HAS_FIRE_BALL = False;self.FIRE_BALL_AMMOUNT = 0
        self.APPLIES_BLEEDING = False;self.TIME_BLEEDING = 0;self.BLEEDING_DAMAGE = 0
        self.ATK_WHILE_DASHING = False
        self.ATKESQUIVA = False;self.FIRST_ATK_AFTER_DASH = False
        self.APLIES_MORE_KNOCKBACK = 1
        self.SURVIVAL_ATK_MULTPLIER = 1
        self.SPIKES = False
        self.NO_SEE = False;self.TIME_NO_SEE = 1

    def getPlayerInput(self, klist, alist):
        #marcadores de h i t b o x.
        #window.blit(spr_cursor, (self.hit_box.x + camera.x, self.hit_box.y + camera.y))
        #window.blit(spr_cursor, (self.hit_box.x + self.hit_box.width + camera.x, self.hit_box.y + self.hit_box.height+ camera.y))
        #marcadores de h i t b o x.
        
        if self.unabletime <= 0:
            for j in range(len(klist)): #movimentando o personagem com base no input
            #k = 0 é A
            #k = 1 é D
            #k = 2 é W
            #k = 3 é S
                if j == 3:
                    self.isCrouch = klist[j]
                if klist[j]:
                    if j == 0 and self.hspeed > -self.lower_max_hspeed:
                        self.hspeed -= self.hacel
                        self.last_direction_moved = -1
                    if j == 1 and self.hspeed < self.lower_max_hspeed:
                        self.hspeed += self.hacel
                        self.last_direction_moved = +1                        
                    if self.on_ground == True:
                        if j == 2:
                            self.vspeed -= self.jump
                            if self.SPIKES:
                                self.CARDspikes()
                        

            
            for i in range(len(alist)):
                if alist[i]:
                    if i == 0 and self.dash_cooldown <= 0:
                        self.hspeed += 1.75*self.last_direction_moved
                        self.dash_cooldown = 45
                        
                    if (i == 1 and self.atk_cooldown <= 0) and (abs(self.hspeed) <= self.lower_max_hspeed + 0.1 or self.ATK_WHILE_DASHING == True):
                        self.isAtacking = True
                        self.atk_cooldown = self.atk_delay
                        self.FIRST_ATK_AFTER_DASH = True
                        if(klist[2]):
                            self.UpAtk()
                        elif(self.isCrouch):
                            self.DownAtk()
                        else:
                            if self.HAS_FIRE_BALL and fs.pointDistance(self.x,self.y,self.enemy.x,self.enemy.y) > ctxt.FIREBALL_ATK_RANGE:
                                self.CARDfireball()
                            else:
                                self.DefaultAtk()
                            

    def takeDamage(self, d, knk):
        if self.invtime <= 0 or self.ATKESQUIVA:
            self.hspeed += knk[0]/self.knockresi
            self.vspeed += knk[1]/self.knockresi
            self.Hp -= d
            self.unabletime = int( ( (knk[0]**2 + knk[1]**2)**(1/2) )*10/self.knockresi)
            self.invtime = self.unabletime * 5/3
            if self.NO_SEE == True:
                self.TIME_NO_SEE = ctxt.NO_SEE_COOLDOWN

    def DefaultAtk(self):
        #Normal Attack

        atk_increase_ = 0

        atk_increase_ += (ctxt.ATKESQUIVA_INCREASE)*(self.ATKESQUIVA == True)*(self.FIRST_ATK_AFTER_DASH == True)

        atk_mult = 1*( self.SURVIVAL_ATK_MULTPLIER**(self.Hp/self.maxHp < ctxt.SURVIVAL_MIN_HP) )

        #atk_args = (self, self.hspeed + self.x + self.hit_box.width*0.2 + self.last_direction_moved*(self.hit_box.width + self.AtkRange),
        #    self.y + self.hit_box.height/5, (90 -(90*self.last_direction_moved)), 0.15, (self.Atk + atk_increase_)*atk_mult, self.knockback*self.APLIES_MORE_KNOCKBACK)

        atk_args = (self,self.hit_box.x + self.hit_box.width/2 + self.last_direction_moved*self.AtkRange*15,
            self.y +self.hit_box.height/4, (90 -(90*self.last_direction_moved)), 0.15, (self.Atk + atk_increase_)*atk_mult, self.knockback*self.APLIES_MORE_KNOCKBACK)

        efeitos.append(chd.charAtk(self.char, atk_args))

        self.FIRST_ATK_AFTER_DASH = False
        
    def UpAtk(self):
        #Normal Attack

        atk_increase_ = 0

        atk_increase_ += (ctxt.ATKESQUIVA_INCREASE)*(self.ATKESQUIVA == True)*(self.FIRST_ATK_AFTER_DASH == True)

        atk_mult = 1*( self.SURVIVAL_ATK_MULTPLIER**(self.Hp/self.maxHp < ctxt.SURVIVAL_MIN_HP) )

        #atk_args = (self, self.hspeed + self.x + self.hit_box.width*0.2 + self.last_direction_moved*(self.hit_box.width + self.AtkRange),
        #    self.y + self.hit_box.height/5, (90 -(90*self.last_direction_moved)), 0.15, (self.Atk + atk_increase_)*atk_mult, self.knockback*self.APLIES_MORE_KNOCKBACK)

        atk_args = (self, self.x + self.hit_box.width/2 , self.y - self.hit_box.height*0.5, 90, 0.15, (self.Atk + atk_increase_)*atk_mult, self.knockback*self.APLIES_MORE_KNOCKBACK, 2)

        efeitos.append(chd.charAtk(self.char, atk_args))

        self.FIRST_ATK_AFTER_DASH = False

    def DownAtk(self):
            if(self.on_ground):
                self.UpAtk()
            else:
                #Normal Attack

                atk_increase_ = 0

                atk_increase_ += (ctxt.ATKESQUIVA_INCREASE)*(self.ATKESQUIVA == True)*(self.FIRST_ATK_AFTER_DASH == True)

                atk_mult = 1*( self.SURVIVAL_ATK_MULTPLIER**(self.Hp/self.maxHp < ctxt.SURVIVAL_MIN_HP) )

                #atk_args = (self, self.hspeed + self.x + self.hit_box.width*0.2 + self.last_direction_moved*(self.hit_box.width + self.AtkRange),
                #    self.y + self.hit_box.height/5, (90 -(90*self.last_direction_moved)), 0.15, (self.Atk + atk_increase_)*atk_mult, self.knockback*self.APLIES_MORE_KNOCKBACK)

                atk_args = (self, self.x + self.hit_box.width/2, self.y + self.hit_box.height*1.1, 270, 0.15, (self.Atk + atk_increase_)*atk_mult, self.knockback*self.APLIES_MORE_KNOCKBACK, 2)

                efeitos.append(chd.charAtk(self.char, atk_args))

                self.FIRST_ATK_AFTER_DASH = False

    def CARDfireball(self):
        #FireBall Attack
        atk_args = (self, self.hspeed + self.x + self.hit_box.width*0.2 + self.last_direction_moved*(self.hit_box.width + self.AtkRange),
            self.y + self.hit_box.height/5, (90 -(90*self.last_direction_moved)), ctxt.FIREBALL_ATIME, ctxt.FIREBALL_ATK, ctxt.FIREBALL_KNOCKBACK)
        efeitos.append(chd.charAtk('fireball', atk_args))
        self.atk_cooldown += self.atk_delay/2
        if self.FIRE_BALL_AMMOUNT > 1:
            for i in range(self.FIRE_BALL_AMMOUNT - 1):
                atk_args = (self, self.hspeed + self.x + self.hit_box.width*0.2 + self.last_direction_moved*(self.hit_box.width + self.AtkRange),
                    self.y + self.hit_box.height/5, random.randint(0,359), ctxt.FIREBALL_ATIME, ctxt.FIREBALL_ATK, ctxt.FIREBALL_KNOCKBACK)
                efeitos.append(chd.charAtk('fireball', atk_args))

    def CARDspikes(self):
        #SPIKES
        y_ = self.y
        while True:
            y_ += 5
            collides = fs.collisionList(blocos.tiles,(self.x + self.hit_box.height/2 ,y_))
            if collides[0] == True or y_ >= room_height:
                break;

        if collides[0] == True:
            y_ = collides[1].y - 64
        else:
            y_ = room_height - 64

        atk_args = (self,self.x + self.hit_box.width/2,
            y_, 0, ctxt.SPIKES_ATIME/60, ctxt.SPIKES_DAMAGE, 1.3)
        efeitos.append(chd.charAtk('spikes', atk_args))

    def restart(self):
        self.Hp = self.maxHp
        self.hit_box.x = self.start_x
        self.hit_box.y = self.start_y
        self.TIME_BLEEDING = 0

    def getCollisions(self, tiles):
        hits = []
        for tile in tiles:
            if self.hit_box.colliderect(tile.hit_box):
                hits.append(tile)
        return hits

    def checkCollX(self, t):
        c = self.getCollisions(t)
        for tile in c:
            if self.hspeed >= 0 :
                self.hit_box.x = tile.hit_box.left - self.hit_box.w
                self.hspeed = 0
            elif self.hspeed < 0:
                self.hit_box.x = tile.hit_box.right
                self.hspeed = 0
    def checkCollY(self, t):
        c = self.getCollisions(t)
        self.hit_box.bottom += 1
        self.on_ground = False
        for tile in c:
            if self.vspeed > 0:
                self.on_ground = True
                self.vspeed = 0
                self.hit_box.bottom = tile.hit_box.top
            elif self.vspeed < 0:
                self.vspeed = 0
                self.hit_box.top = tile.hit_box.bottom
    def step(self): #função que executa o cógido geral do jogador
        if self.atk_cooldown >= 1:
            self.atk_cooldown-=1
            b = self.anim.getDuration()*FPS
            if self.atk_cooldown < self.atk_delay-b:
                self.isAtacking = False
        else:
            self.isAtacking = False
        #print('ataca = {}, atk cd = {}'.format(self.isAtacking, self.atk_cooldown))
        if self.invtime > 0: self.invtime -= 1
        if self.unabletime > 0: self.unabletime -= 1
        
        if self.dash_cooldown > 0:
            self.dash_cooldown -= 1
        if self.Hp > 0:
            '''
            #Verificando se ele está no chão (da tela)
            if self.y >= room_height - self.hit_box.height:

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
            for h_ in range(self.hit_box.height+1):
                if h_ % 14 == 0:
                    var_colisao = fs.collisionList(blocos.tiles, (side_ + self.hspeed*dt,self.hit_box.y + h_))

                    if var_colisao[0] == True:

                        collidee = var_colisao[1] #Colidido da collisionList || "collidee" é o colidido

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
                if self.x + self.hspeed*dt >= 0 and self.x + self.hspeed*dt < room_width - self.hit_box.width:
                    self.x += self.hspeed*dt #Atualizando o x normalmente

                else: #Ele sairia da tela :(
                    if fs.sign(self.hspeed*dt) < 0:
                        self.x = 0
                    else:
                        self.x = room_width - self.hit_box.width
                    self.hspeed = 0

            #Verificando se ele está colidindo || VERTICAL

            #escolhendo o lado para checar a colisão (em cima ou em baixo)
            side_ = self.hit_box.y + (self.hit_box.height/2)*(fs.sign(self.vspeed + VERYSMALL) + 1)

            #Passa por cada ponto (menos os da borda) da parte mais em baixo ou em cima do retângulo
            collided_vertically = False
            for w_ in range(self.hit_box.width - 1+1):
                if w_ % 14 == 0:
                    var_colisao = fs.collisionList(blocos.tiles,(self.hit_box.x + w_ + 1,side_ + self.vspeed*dt))

                    if var_colisao[0] == True:
                        collidee = var_colisao[1] #Colidido da collisionList || "collidee" é o colidido

                        #Aproximando ele do pixel mais próximo sem colidir
                        i_ = 0
                        while collidee.hit_box.collidepoint((self.hit_box.x + w_ + 1,side_ + i_)) == False:
                            i_ += fs.sign(self.vspeed*dt)
                        self.y += i_

                        if self.vspeed >= 0:
                            self.on_ground = True #Está no chão
                        self.vspeed = 0 #Vc colidiu, Vc perde sua velocidade

                        #Exiting loop
                        collided_vertically = True
                        break;

            if collided_vertically == False:
                if self.y + self.vspeed*dt <= room_height - self.hit_box.height:
                    self.y += self.vspeed*dt #Atualizando o y normalmente

                else: #Ele ultrapassaria o chão da tela
                    self.y = room_height - self.hit_box.height
            '''

            #Atualizando o x,y da hitbox do jogador

            #self.hit_box.x = self.x
            #self.hit_box.y = self.y

            #Atualizando a velocidade || HORIZONTAL
            self.hspeed = fs.friction(self.hspeed,self.fric)
            if abs(self.hspeed) > self.max_hspeed: self.hspeed = self.max_hspeed*fs.sign(self.hspeed) #max speed

            #Atualizando a velocidade || VERTICAL
            self.vspeed += self.grav

            self.hit_box.x += self.hspeed*dt
            self.checkCollX(blocos.tiles)
            self.hit_box.y += self.vspeed*dt
            self.checkCollY(blocos.tiles)
            self.x = self.hit_box.x
            self.y = self.hit_box.y
            #vetores muahaha
            self.speed = (self.hspeed**2 + self.vspeed**2 )**(1/2)
            self.direction = 360*(1/(2*math.pi))*(self.speed)

            #dash cooldown
            self.dash_cooldown -= 1

            #bleeding
            if self.TIME_BLEEDING > 0:
                if fs.divs(self.TIME_BLEEDING,ctxt.BLEEDING_RATE) == True:
                    self.takeDamage(self.enemy.BLEEDING_DAMAGE,[0,0])
                self.TIME_BLEEDING -= 1

        else: #Player Has Died
            points[self.enemy.player_] += 1
            global Round
            global vez
            Round += 1
            vez = [self.player_,self.enemy.player_]
            jogador1.restart()
            jogador2.restart()
            spawn_cards()

    def draw(self): #função que desenha o jogador na tela
        if self.Hp > 0:
            #Animation loop
            self.current_spr = self.anim.getCurrentFrame()

            if self.unabletime > 0:
                self.current_spr = self.anim.play('tkdmg')
            else:
                if self.isAtacking:
                    if self.on_ground:
                        if self.isCrouch:
                            self.current_spr = self.anim.play('D_atk')
                        else:
                            self.current_spr = self.anim.play('atk')
                    else:
                        self.current_spr = self.anim.play('A_atk')
                else:
                    if self.on_ground:
                        if abs(self.hspeed) > 0:
                            self.current_spr = self.anim.play('run')
                        elif not self.isCrouch:
                            self.current_spr = self.anim.play('idle')
                        else:
                            self.current_spr = self.anim.play('Crouch')
                    else:
                        self.current_spr = self.anim.play('jump')
                    

            sprite_2x = pg.transform.scale(self.current_spr,
            (int(self.current_spr.get_width()*self.sc),int(self.current_spr.get_height()*self.sc)))

            #Vira o sprite de acordo com a direção dele

            sprite_virado = pg.transform.flip(sprite_2x,self.last_direction_moved < 0,False)

            #Being Invisible
            if self.TIME_NO_SEE > 0:
                window.blit(sprite_virado, (self.x + camera.x-self.offset[0], self.y + camera.y-self.offset[1]))
                if self.NO_SEE == True: self.TIME_NO_SEE -= 1
            else:
                self.TIME_NO_SEE = 0

            #Drawing Healthbar
            if self.player_ == 0:
                draw_rectangle(rel_width/2,rel_height/2,
                rel_width/2 + 500,rel_height/2 + 80,(0,100,0))

                draw_rectangle(rel_width/2,rel_height/2,
                rel_width/2 + 500*(self.Hp/self.maxHp),rel_height/2 + 80,GREEN)

                draw_text(self.char,rel_width/2 + 250,rel_height/2 + 40,color_ = BLACK)

            if self.player_ == 1:
                draw_rectangle(rel_width/2 + room_width - 500,rel_height/2,
                rel_width/2 + room_width,rel_height/2 + 80,(0,100,0))
                draw_rectangle(rel_width/2 + room_width - 500*(self.Hp/self.maxHp),
                rel_height/2,rel_width/2 + room_width,rel_height/2 + 80,GREEN)
                draw_text(self.char,rel_width/2 + room_width - 250,rel_height/2 + 40,color_ = BLACK)

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
        window.blit(self.sprite, (self.x + camera.x, self.y + camera.y))

class obj_camera(object):
    def __init__(self):
        #Caracteristicas do obj definidas na criação
        self.x = rel_width/2
        self.y = rel_height/2

        #Caracteristicas gerais do obj
        self.screen_shake_time = 0
        self.screen_shake_intensity = 20

    def draw(self): #função que desenha o obj na tela
        #window.blit(spr_hit[0], (self.x, self.y))

        #Desenhando bordas
        draw_rectangle(0,0,rel_width/2,window_height,color_ = BLACK)
        draw_rectangle(window_width - rel_width/2,0,window_width,window_height,color_ = BLACK)
        draw_rectangle(0,window_height - rel_height/2,window_width,window_height,color_ = BLACK)
        draw_rectangle(rel_width/2,0,window_width - rel_width/2,rel_height/2,color_ = BLACK)

        #STEP :O
        if self.screen_shake_time > 0:
            self.screen_shake_time -= 1
            self.x += random.randint(-self.screen_shake_intensity,self.screen_shake_intensity)
            self.y += random.randint(-self.screen_shake_intensity,self.screen_shake_intensity)

            self.x = fs.clamp(self.x,rel_width/2 - 30,rel_width/2 + 30)
            self.y = fs.clamp(self.y,rel_height/2 - 30,rel_height/2 + 30)
        else:
            self.x = rel_width/2
            self.y = rel_height/2

    def screenShake(self,_screen_shake_time,intensity_ = 20):
        self.screen_shake_time = _screen_shake_time
        self.screen_shake_intensity = intensity_

class carta(object):
    def __init__(self,x,y,tipo_,id_):
        #Caracteristicas do obj definidas na criação
        self.x = x
        self.y = y
        self.id_ = id_
        self.width = 320
        self.height = 460
        self.card_sprite = pg.Rect(self.x,self.y,self.width,self.height)
        self.sprite = pg.image.load(ctxt.CARDS_IMAGES.get(tipo_)).convert_alpha()
        self.tipo_ = tipo_
        self.txt = ctxt.CARDS_DESCRIPTIONS.get(tipo_)

        #Caracteristicas gerais do obj
        self.sc = 1.2 #\in [1,2)

        #Ajeitando o texto
        for i in range(len(self.txt)):
            if (i + 1) % 23 == 0: # ~22 caracteres por linha
                self.txt = self.txt[:i] + "\n" + self.txt[i:]

    def draw(self): #função que desenha o obj na tela

        #Desenhando o fundo da carta
        self.card_sprite.width = self.width*(1 + (self.sc - 1)*(card_selected == self.id_))
        self.card_sprite.height = self.height*(1 + (self.sc - 1)*(card_selected == self.id_))
        self.card_sprite.x = self.x - self.width*(self.sc - 1)*(card_selected == self.id_)/2
        self.card_sprite.y = self.y - self.height*(self.sc - 1)*(card_selected == self.id_)/2
        pg.draw.rect(window , WHITE ,self.card_sprite)

        #Desenhando a imagem da carta
        if self.sprite != None:

            #Modifica as dimensões do sprite
            sprite_sc = pg.transform.scale(self.sprite,
            (int(self.sprite.get_width()*self.card_sprite.width/self.width),
            int(self.sprite.get_height()*self.card_sprite.height/self.height)))

            window.blit(sprite_sc, (self.card_sprite.x + self.card_sprite.width/2 - sprite_sc.get_width()/2,
            self.card_sprite.y + self.card_sprite.height/3.2 - sprite_sc.get_height()/2))

        #Desenhando a descrição da carta
        fnt_sc = int((self.card_sprite.width/self.width) + (2 - self.sc)) - 1

        draw_text(self.txt,self.card_sprite.x + self.card_sprite.width/2,
        self.card_sprite.y + self.card_sprite.height/2 + 70,
        color_ = BLACK,font_ = fnt_comicsans[fnt_sc])

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
        self.s_index = 0

    def step(self):
        if self.alive_time > 0:
            self.alive_time -= 1

            self.x += self.speed*math.cos(self.direction*(2*math.pi/360))
            self.y += self.speed*math.sin(self.direction*(2*math.pi/360))

        else:
            efeitos.remove(self)
            efeitos_deposito.append(self)

    def draw(self):
        if type([1]) is type(self.sprite):
            self.s_index =  fs.loopValue(self.s_index,0,len(self.sprite) - VERYSMALL,1/5)
            window.blit(self.sprite[int(self.s_index)], (self.x + camera.x, self.y + camera.y))
        else:
            window.blit(self.sprite, (self.x + camera.x, self.y + camera.y))

def draw_text(txt_,x_,y_,font_ = fnt_comicsans[4],color_ = WHITE,centered_ = True):
    if "\n" in txt_:

        #IT HAS LINE BREAKS; (╯°□°)╯︵ ┻━┻

        if centered_ == True: #Centraliza o texto
            x_ -= font_.size(txt_de_22c)[0]/2
            y_ -= font_.size(txt_de_22c)[1]/2

        #Escrevendo cada linha
        i_ = 0 #n line
        str_ = "" #current string with no line breaks

        for i in range(len(txt_)):
            if txt_[i] == "\n" or i == len(txt_) - 1:
                if i == len(txt_) - 1: str_ += txt_[i]

                #Each time there is a line break in string -> draw all the string before the line break
                text_surface = font_.render(str_, False, color_)
                window.blit(text_surface,(x_,y_ + fnt_comicsans_Vspace[fnt_comicsans.index(font_)]*i_))

                i_ += 1 #adding n'th line
                str_ = "" #Resets the "current string with no line breaks"
            else:
                str_ += txt_[i] #Adding to the "current string with no line breaks"

    else:

        #NO LINE BREAKS; LIFE IS GOOD

        if centered_ == True: #Centraliza o texto
            x_ -= font_.size(txt_)[0]/2
            y_ -= font_.size(txt_)[1]/2

        text_surface = font_.render(txt_, False, color_)
        window.blit(text_surface,(x_,y_))

def draw_rectangle(x1,y1,x2,y2,color_ = WHITE):
    pg.draw.rect(window,color_,(x1,y1,(x2 - x1),(y2 - y1)))

def create_effect(efeito_1,efeito_2):
    if len(efeitos_deposito) > 0:
        #Se ja tem um efeito salvo na memoria re-utltilize ele
        efeitos_deposito[0].__init__(efeito_2)

        efeitos.append(efeitos_deposito[0])
        efeitos_deposito.pop(0)
    else:
        #cria um efeito novo
        efeitos.append(chd.charAtk(efeito_1,efeito_2))

def create_projection(anim, x, y, player_owner, on_hit_efx, while_alive_efx, _alive_time):
    if len(efeitos_deposito) > 0:
        #Se ja tem um efeito salvo na memoria re-utltilize ele
        efeito_reciclado = efeitos_deposito[0]
        efeito_reciclado.anim = anim
        efeito_reciclado.hitbox = pg.Rect(x,y,self.anim.playFrame(anim.names[0], 0).get_height(), self.anim.playFrame(anim.names[0], 0).get_width())
        efeito_reciclado.t = _alive_time * 64		## tempo de atividade, em frames (a 64 fps)
        efeito_reciclado.owner = player_owner     		## player que criou (não interage com ele)
        efeito_reciclado.on_hit = on_hit_efx 		## dicionário com o nome e atributos dos métodos que serão executados quando acertar um alvo qualquer
        efeito_reciclado.passive = while_alive_efx
        efeito_reciclado.targets = plist

        efeitos_deposito.pop(0)
        efeitos.append(efeito_reciclado)
    else:
        #cria um efeito novo
        efeitos.append(pj.Projection(anim, x, y, player_owner, on_hit_efx, while_alive_efx, _alive_time))

def play_sound(snd_,loops_ = 0,volume_ = VOLUME_DO_JOGO,fade_out_ = 0):
    snd_.play(loops = loops_)
    snd_.set_volume(VOLUME_DO_JOGO)
    if fade_out_ > 0:
        snd_.fadeout(fade_out_)

def stop_sound(snd_):
    snd_.stop()

def listPlayers():
    return playerList

def spawn_cards():

    USED_CARDS.clear()

    def choose_card_type():
        #ESCOLHE UMA CARTA ALEATORIA

        choosen_card = None

        while True:
            choosen_card = LISTA_DE_CARTAS[random.randint(0,len(LISTA_DE_CARTAS) - 1)]
            if (choosen_card in USED_CARDS) == False:
                USED_CARDS.append(choosen_card)
                return choosen_card

    if len(cartas_deposito) == 0:
        cartas.append(carta(room_width/2 - 700 + camera.x,200 + camera.y,choose_card_type(),0))
        cartas.append(carta(room_width/2 - 160 + camera.x,200 + camera.y,choose_card_type(),1))
        cartas.append(carta(room_width/2 + 700 - 320 + camera.x,200 + camera.y,choose_card_type(),2))
    else:
        #Reciclando as cartas
        for c in range(len(cartas_deposito)):
            if c == 0:
                cartas_deposito[c].__init__(room_width/2 - 700 + camera.x,200 + camera.y,choose_card_type(),0)
            if c == 1:
                cartas_deposito[c].__init__(room_width/2 - 160 + camera.x,200 + camera.y,choose_card_type(),1)
            if c == 2:
                cartas_deposito[c].__init__(room_width/2 + 700 - 320 + camera.x,200 + camera.y,choose_card_type(),2)

            cartas.append(cartas_deposito[c])

        cartas_deposito.clear()

def apply_card_effect(player_,card_):
    if card_.tipo_ == "FIREBALL":
        player_.HAS_FIRE_BALL = True
        player_.FIRE_BALL_AMMOUNT += 1
    if card_.tipo_ == "ENHANCED_SPEED":
        player_.lower_max_hspeed *= ctxt.ENHANCED_SPEED_PERCENT
        player_.max_hspeed *= ctxt.ENHANCED_SPEED_PERCENT
        player_.hacel *= ctxt.ENHANCED_SPEED_PERCENT
    if card_.tipo_ == "BLEEDING":
        player_.APPLIES_BLEEDING = True
        player_.BLEEDING_DAMAGE += ctxt.BLEEDING_DAMAGE
    if card_.tipo_ == "ATK_WHILE_DASHING":
        player_.ATK_WHILE_DASHING = True
    if card_.tipo_ == "ATKESQUIVA":
        player_.ATKESQUIVA = True
    if card_.tipo_ == "APLIES_MORE_KNOCKBACK":
        player_.APLIES_MORE_KNOCKBACK *= ctxt.APLIES_MORE_KNOCKBACK
    if card_.tipo_ == "RECEIVES_LESS_KNOCKBACK":
        player_.knockresi *= ctxt.RECEIVES_LESS_KNOCKBACK
    if card_.tipo_ == "SURVIVAL":
        player_.SURVIVAL_ATK_MULTPLIER *= ctxt.SURVIVAL_ATK_MULTPLIER
    if card_.tipo_ == "SPIKES":
        player_.SPIKES = True
    if card_.tipo_ == "NO_SEE":
        player_.NO_SEE = True

    return 0

def escolhendo_cartas(player_):
    global card_selected

    #Aplicando o efeito das Cartas
    apply_card_effect(player_,cartas[card_selected])

    if len(vez) > 1:
        #Escolhendo a Carta
        cartas_deposito.append(cartas[card_selected])
        cartas.pop(card_selected)

        for c in cartas: #Re-indexando as cartas
            c.id_ = cartas.index(c)

        card_selected = 0 #Choosing new card_selected

        #Passando a vez
        vez.pop(0)

    else: #Os jogadores ja escolheram as cartas

        #Deletando as cartas
        for c in cartas:
            cartas_deposito.append(c)
        cartas.clear()

#CRIANDO OS BLOCOS
blocos = TileMap('forest', rel_width, rel_height)
bg = pg.transform.scale(pg.image.load('Graphics/background/'+'forest'+'.png').convert(),(window_width - rel_width - 64, window_height - rel_height-64))

#CRIANDO ADEMAIS

camera = obj_camera()

efeitos = []
efeitos_deposito = []
cartas = []
cartas_deposito = []
spawn_cards() #COMENTE E DESCOMENTE PARA SPAWNAR AS CARTAS
card_selected = 0
vez = [0,1] #lista que armazena a ordem de escolha de cartas
points = [0,0]
Round = 0

#CRIANDO OS JOGADORES
#wug args [8, 12, 16, 16, 48, 48, 48, 8], [54, 128]
#homi args [8, 12, 16, 16, 32, 20, 32, 8], [0, 15]
jogador1 = obj_jogador('wug',250,450,0, [8, 12, 16, 16, 28, 48, 48, 8], [54, 128])
jogador1.atk_delay = 24
jogador2 = obj_jogador('wherewolf',room_width - 250,450,1)
playerList = [jogador1, jogador2]
jogador1.enemy = jogador2
jogador2.enemy = jogador1

dash = False;attack = False
dash2 = False;attack2 = False

last_time = time.time()

pg.mouse.set_visible(False)

while RODANDO: #game loop

    dt = clock.tick(FPS) #SETS THE FPS

    #dt_ = time.time() - last_time
    #last_time = time.time()

    window.fill((25, 25, 25)) #fundo da tela fica cinza escuro
    window.blit(bg, (rel_width/2 + 32, rel_height/2 + 60)) #fundo da tela fica cinza escuro
    window.blit(*(blocos.draw_map_mesh(window, rel_width/2, rel_height/2)))
    #draw_text(str(int(200*dt_)/200),rel_width/2 + room_width/2,rel_height/2 + 230,color_ = (255,0,0))

    #pg.display.set_caption("{}".format(clock.get_fps())) #mostra o fps no título da tela
    #print(clock.get_fps())

    draw_text("ROUND " + str(Round),rel_width/2 + room_width/2,rel_height/2 + 64,color_ = (255,0,0))
    draw_text(str(points[0]) + " | " + str(points[1]),rel_width/2 + room_width/2,rel_height/2 + 130,color_ = (255,0,0))

    draw_text(str(int(clock.get_fps()*100)/100),rel_width/2 + room_width/2,rel_height/2 + 190,color_ = (255,0,0),font_ = fnt_comicsans[1])

    #---CODIGO DO JOGADOR

    jogador1.step()                                     #Função de cógido geral "step" do jogador1
    jogador1.getPlayerInput(key, act)         #Função para realizar o controle do jogador 1 com base nas inputs do teclado
    jogador1.draw()                                     #Função de desenhar do jogador1
    jogador2.getPlayerInput(key2, act2)       #Função para realizar o controle do jogador 2 com base nas inputs do teclado
    jogador2.step()                                     #Função de cógido geral "step" do jogador2
    jogador2.draw()                                     #Função de desenhar do jogador2


    if act[0] == True:
        #Joga o player horizontalmente pra ultima direção que ele se moveu
        dir_ = 180*(jogador1.hspeed > 0)

        #Dexa um trail pra trás
        #create_effect(jogador1.anim.getCurrentFrame(),jogador1.x,jogador1.y,
        #8,speed_ = 10,direction_ = dir_)

        #create_effect(jogador1.anim.getCurrentFrame(),jogador1.x + 10*fs.sign(jogador1.hspeed),jogador1.y,
        #8,speed_ = 9,direction_ = dir_)

        #create_effect(jogador1.anim.getCurrentFrame(),jogador1.x + 20*fs.sign(jogador1.hspeed),jogador1.y,
        #8,speed_ = 8,direction_ = dir_)

        #Só vai poder usar o dash dnv dps de um tempinho :(

        act[0] = False
        jogador1.dash_cooldown = jogador1.dash_time
        dash = False


    if act2[0] == True:
        #Joga o player horizontalmente pra ultima direção que ele se moveu
        dir_ = 180*(jogador2.hspeed > 0)

        #Dexa um trail pra trás
        #create_effect(jogador2.anim.getCurrentFrame(),jogador2.x,jogador2.y,
        #8,speed_ = 10,direction_ = dir_)

        #create_effect(jogador2.anim.getCurrentFrame(),jogador2.x + 10*fs.sign(jogador2.hspeed),jogador2.y,
        #8,speed_ = 9,direction_ = dir_)

        #create_effect(jogador2.anim.getCurrentFrame(),jogador2.x + 20*fs.sign(jogador2.hspeed),jogador2.y,
        #8,speed_ = 8,direction_ = dir_)
        #Só vai poder usar o dash dnv dps de um tempinho :(

        act2[0] = False


    if act[1] == True:
        act[1] = False


    if act2[1] == True:
        act2[1] = False

        jogador2.dash_cooldown = jogador2.dash_time
        dash2 = False



    #---CODIGO DOS BLOCOS
    #Função de desenhar do bloco

    #---CODIGOS ALEATORIOS
    for f in efeitos:
        #Função de cógido geral "step" do efeito
        if(str(type(f)) == "<class 'projection.Projection'>"):
            f.step(playerList,fs.collisionList_hitbox(blocos.tiles,f.hitbox)[0])

            if(f.t > 0):
                tup = list(f.draw())
                window.blit(tup[0], (tup[1] + camera.x, tup[2] + camera.y))
                
                #marcadores de h i t b o x.
                #window.blit(spr_cursor, (tup[1] + camera.x, tup[2] + camera.y))
                #window.blit(spr_cursor, (tup[1] + camera.x + tup[0].get_width(), tup[2] + tup[0].get_height() + camera.y))
                #marcadores de h i t b o x.
                
            else:
                efeitos.remove(f)
                f.vanish()
                efeitos_deposito.append(f)
        else:
            f.draw() #Função de desenhar do efeito

    camera.draw() #Função de desenhar da camera

    for c in cartas:
        c.draw() #Função de desenhar a carta


    #FIM DOS DESENHOS NA TELA
    #p = pg.transform.scale(window, (window.get_width() *raz, window.get_height() * raz))
    #gamewindow.blit(window, (0, 0))
    pg.display.flip() #mostra td oq foi desenhado dentro desse loop

    #um loop que passa por tds os eventos registrados pelo pygame
    #Tipos de eventos: clicar no mouse, apertar algo no teclado, fechar a janela e etc...
    for eventos in pg.event.get():

        #APERTOU A TECLA
        if eventos.type == pg.KEYDOWN:

            #PLAYER1

            if eventos.key == pg.K_a:
                if len(cartas) > 0 and vez[0] == 0:
                    card_selected = fs.loopValue(card_selected,0,len(cartas) - 1,-1)
                else:
                    key[0] = True

            if eventos.key == pg.K_d:
                if len(cartas) > 0 and vez[0] == 0:
                    card_selected = fs.loopValue(card_selected,0,len(cartas) - 1,+1)
                else:
                    key[1] = True

            if eventos.key == pg.K_w: key[2] = True
            if eventos.key == pg.K_s: key[3] = True

            #DASH KEY / SELECT CARD
            if eventos.key == pg.K_r:
                if len(cartas) > 0 and vez[0] == 0:
                    escolhendo_cartas(jogador1)
                else:
                    act[0] = True

            #ATTACK KEY
            if eventos.key == pg.K_t:
                attack = True
                act[1] = True

            #PLAYER2

            if eventos.key == pg.K_LEFT:
                if len(cartas) > 0 and vez[0] == 1:
                    card_selected = fs.loopValue(card_selected,0,len(cartas) - 1,-1)
                else:
                    key2[0] = True

            if eventos.key == pg.K_RIGHT:
                if len(cartas) > 0 and vez[0] == 1:
                    card_selected = fs.loopValue(card_selected,0,len(cartas) - 1,+1)
                else:
                    key2[1] = True

            if eventos.key == pg.K_UP: key2[2] = True
            if eventos.key == pg.K_DOWN: key2[3] = True

            #DASH KEY / SELECT CARD
            if eventos.key == pg.K_KP2:
                if len(cartas) > 0 and vez[0] == 1:
                    escolhendo_cartas(jogador2)
                else:
                    act2[0] = True

            #ATTACK KEY
            if eventos.key == pg.K_KP3:
                attack2 = True
                act2[1] = True

            #GERAL

            #Ending Game
            if eventos.key == pg.K_ESCAPE:
                RODANDO = False

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

        #FECHOU A JANELA
        if eventos.type == pg.QUIT:
            RODANDO = False
        

#FIM
print("jogo finalizado")
