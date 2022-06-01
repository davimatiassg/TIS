#IMPORTS DO JOGO
import pygame as pg
import ctypes
import fs

#SETUP DA TELA (só mexa no width e height)
window_width = 1280
window_height = 720
pg.init()
clock = pg.time.Clock()
ctypes.windll.user32.SetProcessDPIAware()
true_res = (int( ctypes.windll.user32.GetSystemMetrics(0)/(1920/(window_width))),
            int( ctypes.windll.user32.GetSystemMetrics(1)/(1080/(window_height))) )
window = pg.display.set_mode(true_res)

#VARIAVEIS GLOBAIS
RODANDO = True
key = [False,False,False,False] #lista ulitlizada na movimentação do jogador
FPS = 64 #ITS 63 BECAUSE YES (dont change)
VERYSMALL = 0.001
VERBIG = 10**5

#IMPORTANTO SPRITES E ETC GRÁFICOS
spr_homi = [
pg.image.load('Graphics\spr_homi1.png').convert_alpha(),
pg.image.load('Graphics\spr_homi2.png').convert_alpha(),
pg.image.load('Graphics\spr_homi3.png').convert_alpha()]

spr_bloco = pg.image.load('Graphics\sbloco.png').convert_alpha()

#OBJETOS / CLASSES
class obj_jogador(object):
    def __init__(self,spr,x,y):
        #Caracteristicas do obj definidas na criação
        self.sprite = spr
        self.hit_box = pg.Rect(x,y,spr[0].get_height(),spr[0].get_width())
        self.x = x
        self.y = y

        #Caracteristicas gerais do obj
        self.hspd = 0 #velocidade horizontal
        self.vspd = 0 #velocidade vertical
        self.max_hspd = 5 #velocidade horizontal máxima (em módulo)
        self.lower_max_hspd = 1 #"walk speed" máxima (em módulo)
        self.max_vspd = 5 #velocidade vertical máxima (em módulo)
        self.hacel = 0.12 #aceleração horizontal
        self.jump = 2 #aceleração vertical, ou seja, pulo
        self.fric = 0.09 #fricção
        self.grav = 0.1 #gravidade
        self.on_ground = False #boolean: está no chão?
        self.sprite_index = 0 #index atual do sprite
        self.load_sprite_index = 0 #variavel que serve para loopar o sprite_index



    def step(self): #função que executa o cógido geral do jogador

        #Verificando se ele está no chão (da tela)
        if self.y >= window_height - self.hit_box.height:

            #self.y = window_height - self.hit_box.height

            if self.vspd >= 0:
                self.on_ground = True
            else:
                self.on_ground = False

        else:
            self.on_ground = False


#Atualizando o x,y do jogador com base na velocidade e no lag ( dt )

        #Verificando se ele está colidindo || HORIZONTAL

        #escolhendo o lado para checar a colisão (esquerda ou direita)
        side_ = self.hit_box.x + self.hit_box.width/2*(fs.sign(self.hspd + VERYSMALL) + 1)

        #Passa por cada ponto (menos os da borda) da parte mais esquerda ou direita do retângulo
        collided_horizontally = False
        for h_ in range(self.hit_box.height):
            var_colisao = fs.collision_list(blocos,(side_ + self.hspd*dt,self.hit_box.y + h_))

            if var_colisao[0] == True:

                collidee = var_colisao[1] #Colidido da collision_list || "collidee" é o colidido

                #Aproximando ele do pixel mais próximo sem colidir
                i_ = 0
                while collidee.hit_box.collidepoint((side_ + i_,self.hit_box.y + h_)) == False:
                    i_ += fs.sign(self.hspd*dt)
                self.x += i_

                self.hspd = 0 #Vc colidiu, Vc perde sua velocidade

                #Exiting loop
                collided_horizontally = True
                break;

        if collided_horizontally == False:
            if self.x + self.hspd*dt >= 0 and self.x + self.hspd*dt < window_width - self.hit_box.width:
                self.x += self.hspd*dt #Atualizando o x normalmente

            else: #Ele sairia da tela :(
                if fs.sign(self.hspd*dt) < 0:
                    self.x = 0
                else:
                    self.x = window_width - self.hit_box.width

        #Verificando se ele está colidindo || VERTICAL

        #escolhendo o lado para checar a colisão (em cima ou em baixo)
        side_ = self.hit_box.y + (self.hit_box.height/2)*(fs.sign(self.vspd + VERYSMALL) + 1)

        #Passa por cada ponto (menos os da borda) da parte mais em baixo ou em cima do retângulo
        collided_vertically = False
        for w_ in range(self.hit_box.width - 1):
            var_colisao = fs.collision_list(blocos,(self.hit_box.x + w_ + 1,side_ + self.vspd*dt))

            if var_colisao[0] == True:
                collidee = var_colisao[1] #Colidido da collision_list || "collidee" é o colidido

                #Aproximando ele do pixel mais próximo sem colidir
                i_ = 0
                while collidee.hit_box.collidepoint((self.hit_box.x + w_ + 1,side_ + i_)) == False:
                    i_ += fs.sign(self.vspd*dt)
                self.y += i_

                if self.vspd > 0:
                    self.on_ground = True #Está no chão
                self.vspd = 0 #Vc colidiu, Vc perde sua velocidade

                #Exiting loop
                collided_vertically = True
                break;

        if collided_vertically == False:
            if self.y + self.vspd*dt <= window_height - self.hit_box.height:
                self.y += self.vspd*dt #Atualizando o y normalmente

            else: #Ele ultrapassaria o chão da tela
                self.y = window_height - self.hit_box.height


        #Atualizando o x,y da hitbox do jogador
        self.hit_box.x = self.x
        self.hit_box.y = self.y

        #Atualizando a velocidade || HORIZONTAL
        self.hspd = fs.friction(self.hspd,self.fric)
        if abs(self.hspd) > self.max_hspd: self.hspd = self.max_hspd*fs.sign(self.hspd) #max speed

        #Atualizando a velocidade || VERTICAL
        if self.on_ground == False:
            self.vspd += self.grav
        else:
            #certificando que o obj não está acelerando em direção ao chão
            if self.vspd > 0: self.vspd = 0

        if abs(self.hspd) > self.max_hspd: self.hspd = self.max_hspd*fs.sign(self.hspd) #max speed


    def draw(self): #função que desenha o jogador na tela

        #Animation loop
        if abs(self.hspd) > 0:
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

#CRIANDO OS BLOCOS
blocos = []
blocos.append(obj_bloco(spr_bloco,256,window_height - spr_bloco.get_height()))
blocos.append(obj_bloco(spr_bloco,256,window_height - 64 - spr_bloco.get_height()))
blocos.append(obj_bloco(spr_bloco,256,window_height - 128 - spr_bloco.get_height()))
blocos.append(obj_bloco(spr_bloco,256 + 64,window_height - 128 - spr_bloco.get_height()))
blocos.append(obj_bloco(spr_bloco,256 + 64*2,window_height - 128 - spr_bloco.get_height()))
blocos.append(obj_bloco(spr_bloco,window_width - 256 + 50,window_height - 256 - spr_bloco.get_height()))

#CRIANDO OS JOAGDORES
jogador1 = obj_jogador(spr_homi,0,0)
dash = False

while RODANDO: #game loop

    dt = clock.tick(FPS) #SETS THE FPS

    pg.display.set_caption("{}".format(clock.get_fps())) #mostra o fps no título da tela

    window.fill((25, 25, 25)) #fundo da tela fica cinza escuro


    #---CODIGO DO JOGADOR
    jogador1.step()
    jogador1.draw()

    for k in range(len(key)): #movimentando o personagem com base no input
        #k = 0 é A
        #k = 1 é D
        #k = 2 é W
        #k = 3 é S
        if key[k]:
            if k == 0 and jogador1.hspd > -jogador1.lower_max_hspd:
                jogador1.hspd -= jogador1.hacel
            if k == 1 and jogador1.hspd < jogador1.lower_max_hspd:
                jogador1.hspd += jogador1.hacel

            if jogador1.on_ground == True:
                if k == 2: jogador1.vspd -= jogador1.jump

            if k == 3: jogador1.y += 0

    if dash == True:
        jogador1.hspd += 1.75*fs.sign(jogador1.hspd)
        dash = False


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

        #FECHOU A JANELA
        if eventos.type == pg.QUIT:
            RODANDO = False

#FIM
print("jogo finalizado")
