import pygame as pg
import animation as an
import projection as pj
import cards_txt as ctxt
import math

def charAtk(a, t):
	return globals()[char_atk.get(a)](*t)

char_atk = {
	'wherewolf':'claws',
	'homi':'homiatk',
	'fireball':'fireball',
	'wug':'missile',
	'spikes': 'spikes'
}

def claws(player, x, y, di, atime, dmg, knk, size = 1.5):
	anim = an.Animator(['claws'], [32], 'claws', 'fx_')
	hfx = {
	'damage': [dmg, knk],
	'bleeding': [player.APPLIES_BLEEDING],
	'lifesteal':[player, dmg],
	'bleeding': [player.APPLIES_BLEEDING]
	}
	pfx = {
	'move':[[player.hspeed*8, player.vspeed*8]]
	}

	return pj.Projection(anim, x, y, di, player, hfx, pfx, atime, False, size)

def homiatk(player, x, y, di, atime, dmg, knk, size = 1.5):
	anim = an.Animator(['homiatk'], [15], 'homiatk', 'fx_')
	hfx = {
	'damage': [dmg, knk],
	'bleeding': [player.APPLIES_BLEEDING]
	}
	pfx = {
	'move':[[player.hspeed*8, player.vspeed*8]]
	}
	return pj.Projection(anim, x, y - 15, di, player, hfx, pfx, atime, False, size)

def fireball(player, x, y, di, atime, dmg, knk, s = 2):
	anim = an.Animator(['fireball','explode'], [9,35], 'fireball', 'fx_')
	hfx = {
	'damage': [dmg, knk],
	'block_contact': [],
	'explode': [23]
	}
	pfx = {
	'move':[[ctxt.FIREBALL_SPEED*math.cos((2*math.pi)*di/360), ctxt.FIREBALL_SPEED*math.sin((2*math.pi)*di/360)]]
	}
	return pj.Projection(anim, x, y, di, player, hfx, pfx, atime, False, s)

def missile(player, x, y, di, atime, dmg, knk, s = 2):
	anim = an.Animator(['missile','explode'], [12,35], 'missile', 'fx_')
	hfx = {
	'damage': [dmg, knk],
	'block_contact': [],
	'explode': [23]
	}
	pfx = {
	'move':[[ctxt.FIREBALL_SPEED*math.cos((2*math.pi)*di/360), ctxt.FIREBALL_SPEED*-1*math.sin((2*math.pi)*di/360)]]
	}
	return pj.Projection(anim, x, y, di, player, hfx, pfx, 1, False, s)

def spikes(player, x, y, di, atime, dmg, knk, s = 2):
	anim = an.Animator(['spikes'], [12], 'spikes', 'fx_')
	hfx = {
	'damage': [dmg, knk]
	}
	pfx = {
	}
	return pj.Projection(anim, x, y, di, player, hfx, pfx, atime, False, s)
