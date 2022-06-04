import pygame as pg
import animation as an
import projection as pj

def charAtk(a, t):
	return globals()[char_atk.get(a)](*t)

char_atk = {
	'wherewolf':'claws',
	'homi':'homiatk'
}

def claws(player, x, y, atime, dmg, knk):
	anim = an.Animator(['claws'], 'claws', 'fx_')
	fx = {
	'damage': [dmg, knk]
	}
	return( pj.projection(anim, x, y, player, fx, [], atime))
def homiatk():
	pass