import pygame as pg
import ctypes
import fs
import math
import animation as an
import cards_txt as ctxt


class Projection(object): #define uma classe projeção
	def __init__(self, anim, x, y, di, player_owner, on_hit_efx, while_alive_efx, _alive_time, vanish_on_hit, sc = 1):
		self.scale = sc 
		self.anim = anim
		a = player_owner.anim.getCurrentFrame()

		tx = self.anim.playFrame(anim.names[0], 0).get_height()
		ty = self.anim.playFrame(anim.names[0], 0).get_width()
		self.hitbox = pg.Rect(x + a.get_width()/2 , y + a.get_height()/2,tx, ty) 						## hitbox da projeção
		self.t = _alive_time * 60		## tempo de atividade, em frames (a 64 fps)
		self.owner = player_owner     							## player que criou (não interage com ele)
		self.on_hit = on_hit_efx 								## dicionário com o nome e atributos dos métodos que serão executados quando acertar um alvo qualquer
		self.passive = while_alive_efx
		self.dir = di
		self.van = vanish_on_hit						## dicionário com o nome e atributos dos métodos que serão executados enquanto a projeção estiver ativa
		  										## recebe um objeto da classe Animator, criado fora da classe projection


	def draw(self): #função que desenha o obj na tela
		spr = self.anim.play(self.anim.current)
		a = pg.transform.rotate(pg.transform.scale(spr,(int(spr.get_width()*1.5),int(spr.get_height()*1.5))), self.dir)

		new_rect = a.get_rect(center = a.get_rect(topleft = (self.hitbox.x, self.hitbox.y - self.hitbox.height/6)).center)
		return a, new_rect.x, new_rect.y

	def vanish(self): ## função para desaparecer/desativar
		self.on_hit = []
		self.passive = []
		if(self.van):
			self.anim = self.anim.clearAnim()
			self.hitbox = pg.Rect(0, 0, 0, 0)
			self.t = 0
		## (ainda não tá pronta)


	## ## OS EFEITOS A SEGUIR SÃO DEPENDENTES DE CARTAS E TIPO DE ATAQUE ## ##

	def move(self, _speed): ## função para mover em uma direção
		## direção do movimento, em graus de inclinação em relação à direita
		## velocidade do movimento
		self.hitbox.x += _speed[0] ## atualiza posição no eixo x
		self.hitbox.y += _speed[1] ## atualiza posição no eixo y

	def damage(self, dmg, knockback, tg):
		if tg != None:
			k = []
			k.append(knockback*math.cos(self.dir*2*math.pi/360))
			k.append(knockback*math.sin(self.dir*2*math.pi/360) + 1)
			tg.takeDamage(dmg, k)

	def lifesteal(self, player, dmg, tg):
		if player.Hp < player.maxHp:
			player.Hp += dmg/4
			if player.Hp > player.maxHp:
				player.Hp = player.maxHp
				
	def explode(self,*args):
		self.anim.play('explode')
		self.t = args[0]

	def bleeding(self, applies_, tg):
		if applies_ == True: tg.TIME_BLEEDING = ctxt.BLEEDING_TIME

	def block_contact(self,*args):
		return 0

	def step(self, plist, is_colliding):
		if(self.t > 0):											## enquanto estiver ativo
			self.t -= 1											## diminua o tempo ativo
			self.anim.play(self.anim.animations[0].name)
			for i in self.passive:
				fullargs = self.passive.get(i)
				hitfx = getattr(Projection, i)						## para cada string i com o nome de um método que roda passivamente dentro do dicionário
				hitfx(self, *tuple(fullargs))				## procure localmente e execute o método de nome i com os argumentos associados a ele no dicionário
			for i in plist:
				if self.hitbox.colliderect(i.hit_box) and i.player_ != self.owner.player_:
					for j in self.on_hit:
						fullargs = self.on_hit.get(j)
						fullargs.append(i)
						hitfx = getattr(Projection, j)
						hitfx(self, *tuple(fullargs))
					self.vanish()

			#COLLIDING WITH BLOCKS
			if is_colliding and ('block_contact' in self.on_hit):
				for j in self.on_hit:
					fullargs = self.on_hit.get(j)
					fullargs.append(None) #its colliding with the player "None"
					hitfx = getattr(Projection, j)
					hitfx(self, *tuple(fullargs))

				self.vanish()

												## para cada string j com o nome de um método que roda ao contato dentro do dicionário
						#getattr()[j](*tuple(fullargs))				## procure localmente e execute o método de nome j com os argumentos associados a ele no dicionário
