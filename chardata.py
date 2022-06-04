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
	anim = an.Animator(['claws'], [32], 'claws', 'fx_')
	hfx = {
	'damage': [dmg, knk]
	}
	pfx = {
	'move':[[player.hspeed, player.vspeed]]
	}
	return pj.Projection(anim, x, y, di, player, hfx, pfx, atime, False)
def homiatk(player, x, y, di, atime, dmg, knk):
	anim = an.Animator(['homiatk'], [15], 'homiatk', 'fx_')
	hfx = {
	'damage': [dmg, knk]
	}
	pfx = {
	'move':[[player.hspeed, player.vspeed]]
	}
	return pj.Projection(anim, x, y, di, player, hfx, pfx, atime, False)