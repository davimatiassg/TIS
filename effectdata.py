import pygame as pg
import animation as an
import projection as pj
import cards_txt as ctxt
import math

def fxSpawn(a, t):
	return globals()[efx.get(a)](*t)

efx = {
	'wherewolf':'claws',
	'homi':'homiatk',
	'fireball':'fireball',
	'wug':'missile',
	'spikes': 'spikes',
	'iceball': 'iceball'
}

def claws(player, x, y, di, atime, dmg, knk, s = 1, bonusFX = {}):
	anim = an.Animator(['claws'], [32], 'claws', 'fx_')
	scale = 1.5
	hfx = {
	'damage': [dmg, knk],
	'lifesteal':[player, dmg]
	}
	hfx.update(bonusFX)
	pfx = {
	'move':[[player.hspeed*8, player.vspeed*8]]
	}

	return pj.Projection(anim, x, y, di, player, hfx, pfx, atime, False, s*scale)

def homiatk(player, x, y, di, atime, dmg, knk, s = 1, bonusFX = {}):
	anim = an.Animator(['homiatk'], [15], 'homiatk', 'fx_')
	scale = 1.5
	hfx = {
	'damage': [dmg, knk]
	}
	hfx.update(bonusFX)
	pfx = {
	'move':[[player.hspeed*8, player.vspeed*8]]
	}
	return pj.Projection(anim, x, y - 15, di, player, hfx, pfx, atime, False, s*scale)

def fireball(player, x, y, di, atime, dmg, knk, s = 1, bonusFX = {}):
	anim = an.Animator(['fireball','explode'], [9,35], 'fireball', 'fx_')
	scale = 1.6
	hfx = {
	'damage': [dmg, knk],
	'block_contact': [],
	'explode': [23]
	}
	#hfx.update(bonusFX)
	pfx = {
	'move':[[ctxt.FIREBALL_SPEED*math.cos((2*math.pi)*di/360), ctxt.FIREBALL_SPEED*math.sin((2*math.pi)*di/360)]]
	}
	return pj.Projection(anim, x, y, di, player, hfx, pfx, atime, False, s*scale)

def iceball(player, x, y, di, atime, dmg, knk, s = 1, bonusFX = {}):
	anim = an.Animator(['iceball','explode'], [9,50], 'iceball', 'fx_')
	scale = 2
	hfx = {
	'block_contact': [],
	'explode': [14],
	'freeze': [ctxt.ICE_SLOW, ctxt.ICE_TIME]
	}
	#hfx.update(bonusFX)
	pfx = {
	'move':[[ctxt.ICEBALL_SPEED*math.cos((2*math.pi)*di/360), ctxt.ICEBALL_SPEED*math.sin((2*math.pi)*di/360)]]
	}
	return pj.Projection(anim, x, y, di, player, hfx, pfx, atime, False, s*scale)

def missile(player, x, y, di, atime, dmg, knk, s = 1, bonusFX = {}):
	anim = an.Animator(['missile','explode'], [12,35], 'missile', 'fx_')
	scale = 2
	hfx = {
	'damage': [dmg, knk],
	'block_contact': [],
	'explode': [23]
	}
	hfx.update(bonusFX)
	pfx = {
	'move':[[ctxt.FIREBALL_SPEED*math.cos((2*math.pi)*di/360), ctxt.FIREBALL_SPEED*math.sin((2*math.pi)*di/360)]]
	}
	return pj.Projection(anim, x, y, di, player, hfx, pfx, 1, False, s*scale)

def spikes(player, x, y, di, atime, dmg, knk, s = 1, bonusFX = {}):
	anim = an.Animator(['spikes'], [12], 'spikes', 'fx_')
	scale = 2
	hfx = {
	'damage': [dmg, knk]
	}
	hfx.update(bonusFX)
	pfx = {
	}
	return pj.Projection(anim, x, y, di, player, hfx, pfx, atime, False, s*scale)
