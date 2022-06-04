import pygame as pg
import animation as an
import projection as pj

def charAtk(a, t):
	return globals()[char_atk.get(a)](*t)

char_atk = {
	'wherewolf':'claws',
	'homi':'homiatk'
}

def claws(player, x, y, di, atime, dmg, knk):
	anim = an.Animator(['claws'], [20], 'claws', 'fx_')
	fx = {
	'damage': [dmg, knk]
	}
	return pj.Projection(anim, x, y, di, player, fx, [], atime, False)
def homiatk():
	pass