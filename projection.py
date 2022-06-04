import pygame as pg
import ctypes
import fs
import math
import animation as an


plist = []
def getpList(pl):
	plist = pl

class projection(object): #define uma classe projeção
	def __init__(self, anim, x, y, player_owner, on_hit_efx, while_alive_efx, _alive_time):
		self.anim = anim
		self.hitbox = pg.Rect(x,y,self.anim.playFrame(anim.names[0], 0).get_height(), self.anim.playFrame(anim.names[0], 0).get_width()) 						## hitbox da projeção
		self.t = _alive_time * 64		## tempo de atividade, em frames (a 64 fps)
		self.owner = player_owner     							## player que criou (não interage com ele)
		self.on_hit = on_hit_efx 								## dicionário com o nome e atributos dos métodos que serão executados quando acertar um alvo qualquer
		self.passive = while_alive_efx	
		self.targets = plist						## dicionário com o nome e atributos dos métodos que serão executados enquanto a projeção estiver ativa
		  										## recebe um objeto da classe Animator, criado fora da classe projection
	def step(self):
		if(self.t > 0):											## enquanto estiver ativo
			self.t -= 1											## diminua o tempo ativo
			self.anim.play('claws')
			for i in self.passive: 								## para cada string i com o nome de um método que roda passivamente dentro do dicionário
				locals()[i](tuple(self.passive.get(i)))				## procure localmente e execute o método de nome i com os argumentos associados a ele no dicionário

			if self.hitbox.collidelist(fs.getAllRects()) != -1: ## caso a hitbox colida com algum outro Rect
				for i in self.targets:
					if player_owner != i.player and self.hitbox.colliderect(i.hit_box):
						for j in self.on_hit:
							fullargs = self.on_hit.get(j)
							fullargs.append(i)						## para cada string j com o nome de um método que roda ao contato dentro do dicionário
							locals()[j](tuple(fullargs))				## procure localmente e execute o método de nome j com os argumentos associados a ele no dicionário
					self.vanish()
		else:
			self.vanish()

	def draw(self): #função que desenha o obj na tela
		window.blit(self.anim.play('claws'), (self.hitbox.x, self.hitbox.y))

	def vanish(self): ## função para desaparecer/desativar
		pass ## (ainda não tá pronta)


	## ## OS EFEITOS A SEGUIR SÃO DEPENDENTES DE CARTAS E TIPO DE ATAQUE ## ##

	def move(self, _dir, _stpos, _speed): ## função para mover em uma direção
			self.d = _dir 						## direção do movimento, em graus de inclinação em relação à direita
			self.s = _speed						## velocidade do movimento
			self.hitbox.x += self.s*math.cos(d*(2*math.pi/360)) ## atualiza posição no eixo x
			self.hitbox.y += self.s*math.sin(d*(2*math.pi/360)) ## atualiza posição no eixo y

	def damage(self, dmg, knockback, tg):
		tg.takeDamage(dmg, knockback)