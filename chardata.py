#Wug

WUG_FRAME_RATES = [8, 12, 16, 16, 48, 48, 48, 8]

WUG_SPRITE_OFFSET = [54, 128]

WUG_STATS = {
'F_rate':WUG_FRAME_RATES,
'Spr_offset':WUG_SPRITE_OFFSET,
'AtkRange': 2, 
'atk_delay': 30,
'dash_time': 20,
'knockback': 1.2
}


#homi

HOMI_FRAME_RATES = [8, 12, 16, 16, 32, 20, 32, 8]

HOMI_SPRITE_OFFSET= [0, 15]

HOMI_STATS = {
'F_rate': HOMI_FRAME_RATES,
'Spr_offset':HOMI_SPRITE_OFFSET,
'AtkRange': 5, 
'atk_delay': 12,
'dash_time': 15,
'knockback': 1.15
}

#wherewolf

WOLF_FRAME_RATES = [8, 12, 16, 16, 32, 20, 32, 8]

WOLF_SPRITE_OFFSET = [0, 0]

WOLF_STATS = {
'F_rate': WOLF_FRAME_RATES,
'Spr_offset':WOLF_SPRITE_OFFSET,
'AtkRange': 5, 
'atk_delay': 16,
'maxHp': 55,
'Hp': 55
}




CharacterSelection = {
'wherewolf': WOLF_STATS, 
'wug': WUG_STATS, 
'homi': HOMI_STATS
}


def GetCharAtributes(a):
	print(a)
	return CharacterSelection.get(a)