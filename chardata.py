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
	'spikes': 'spikes'
}

def claws(player, x, y, di, atime, dmg, knk):
	anim = an.Animator(['claws'], [32], 'claws', 'fx_')
	hfx = {
	'damage': [dmg, knk],
	'bleeding': [player.APPLIES_BLEEDING]
	}
	pfx = {
	'move':[[player.hspeed, player.vspeed]]
	}

	return pj.Projection(anim, x, y, di, player, hfx, pfx, atime, False)

def homiatk(player, x, y, di, atime, dmg, knk):
	anim = an.Animator(['homiatk'], [15], 'homiatk', 'fx_')
	hfx = {
	'damage': [dmg, knk],
	'bleeding': [player.APPLIES_BLEEDING]
	}
	pfx = {
	'move':[[player.hspeed, player.vspeed]]
	}
	return pj.Projection(anim, x, y, di, player, hfx, pfx, atime, False)

def fireball(player, x, y, di, atime, dmg, knk):
	anim = an.Animator(['fireball','explode'], [2,1], 'fireball', 'fx_')
	hfx = {
	'damage': [dmg, knk],
	'block_contact': [],
	'explode': []
	}
	pfx = {
	'move':[[ctxt.FIREBALL_SPEED*math.cos((2*math.pi)*di/360), ctxt.FIREBALL_SPEED*math.sin((2*math.pi)*di/360)]]
	}
	return pj.Projection(anim, x, y, di, player, hfx, pfx, atime, False)

def spikes(player, x, y, di, atime, dmg, knk):
	anim = an.Animator(['spikes'], [3/0.8], 'spikes', 'fx_')
	hfx = {
	'damage': [dmg, knk]
	}
	pfx = {
	}
	return pj.Projection(anim, x, y, di, player, hfx, pfx, atime, False)
