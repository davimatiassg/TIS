import pygame as pg
import ctypes
import fs
import math
import animation as an


class Projection(object): #define uma classe projeção
	def __init__(self, anim, x, y, di, player_owner, on_hit_efx, while_alive_efx, _alive_time, vanish_on_hit):
		self.anim = anim
		self.hitbox = pg.Rect(x,y,self.anim.playFrame(anim.names[0], 0).get_height(), self.anim.playFrame(anim.names[0], 0).get_width()) 						## hitbox da projeção
		self.t = _alive_time * 60		## tempo de atividade, em frames (a 64 fps)
		self.owner = player_owner     							## player que criou (não interage com ele)
		self.on_hit = on_hit_efx 								## dicionário com o nome e atributos dos métodos que serão executados quando acertar um alvo qualquer
		self.passive = while_alive_efx	
		self.dir = di
		self.van = vanish_on_hit						## dicionário com o nome e atributos dos métodos que serão executados enquanto a projeção estiver ativa
		  										## recebe um objeto da classe Animator, criado fora da classe projection


	def draw(self): #função que desenha o obj na tela
		a = pg.transform.rotate(self.anim.play(self.anim.current), self.dir), self.hitbox.x, self.hitbox.y
		return a

	def vanish(self): ## função para desaparecer/desativar
		self.hibox = pg.Rect(0, 0, 0, 0)
		self.on_hit = []
		self.passive = []
		if(self.van):
			self.anim = self.anim.clearAnim()
			self.t = 0
		## (ainda não tá pronta)


	## ## OS EFEITOS A SEGUIR SÃO DEPENDENTES DE CARTAS E TIPO DE ATAQUE ## ##

	def move(self, _dir,  _speed): ## função para mover em uma direção
			self.dir = _dir 						## direção do movimento, em graus de inclinação em relação à direita
			self.s = _speed						## velocidade do movimento
			self.hitbox.x += self.s*math.cos(dir*(2*math.pi/360)) ## atualiza posição no eixo x
			self.hitbox.y += self.s*math.sin(dir*(2*math.pi/360)) ## atualiza posição no eixo y

	def damage(self, dmg, knockback, tg):
		k = []
		k.append(knockback*math.cos(self.dir*2*math.pi/360))
		k.append(knockback*math.sin(self.dir*2*math.pi/360) + 1)
		tg.takeDamage(dmg, k)

	def step(self, plist):
		if(self.t > 0):											## enquanto estiver ativo
			self.t -= 1											## diminua o tempo ativo
			self.anim.play('claws')
			for i in self.passive: 								## para cada string i com o nome de um método que roda passivamente dentro do dicionário
				locals()[i](tuple(self.passive.get(i)))				## procure localmente e execute o método de nome i com os argumentos associados a ele no dicionário
			for i in plist:
				if self.hitbox.colliderect(i.hit_box) and i.player_ != self.owner:
					for j in self.on_hit:
						fullargs = self.on_hit.get(j)
						fullargs.append(i)
						hitfx = getattr(Projection, j)
						hitfx(self, *tuple(fullargs))
												## para cada string j com o nome de um método que roda ao contato dentro do dicionário
						#getattr()[j](*tuple(fullargs))				## procure localmente e execute o método de nome j com os argumentos associados a ele no dicionário
					self.vanish()