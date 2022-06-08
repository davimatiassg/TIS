import pygame as pg
import animation as an
import projection as pj
import cards_txt as ctxt

def charAtk(a, t):
	return globals()[char_atk.get(a)](*t)

char_atk = {
	'wherewolf':'claws',
	'homi':'homiatk',
	'fireball':'fireball'
}

def claws(player, x, y, di, atime, dmg, knk):
	anim = an.Animator(['claws'], [32], 'claws', 'fx_')
	hfx = {
	'damage': [dmg, knk],
	'bleeding': [player.APPLIES_BLEEDING],
	'lifesteal':[player, dmg]
	}
	pfx = {
	'move':[[player.hspeed, player.vspeed]]
	}

	return pj.Projection(anim, x, y, di, player, hfx, pfx, atime, False, 1.5)

def homiatk(player, x, y, di, atime, dmg, knk):
	anim = an.Animator(['homiatk'], [15], 'homiatk', 'fx_')
	hfx = {
	'damage': [dmg, knk],
	'bleeding': [player.APPLIES_BLEEDING]
	}
	pfx = {
	'move':[[player.hspeed, player.vspeed]]
	}
	return pj.Projection(anim, x, y, di, player, hfx, pfx, atime, False, 1.5)

def fireball(player, x, y, di, atime, dmg, knk):
	anim = an.Animator(['fireball','explode'], [9,35], 'fireball', 'fx_')
	hfx = {
	'damage': [dmg, knk],
	'block_contact': [],
	'explode': [23]
	}
	pfx = {
	'move':[[ctxt.FIREBALL_SPEED*player.last_direction_moved, 0]]
	}
	return pj.Projection(anim, x, y, di, player, hfx, pfx, atime, False, 2)
