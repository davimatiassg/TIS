import pygame as pg

CARDS_NOTSTACKABLE = []

#FIREBALL
FIREBALL_ATK_RANGE = 240
FIREBALL_ATIME = 1.2*60 #in frames
FIREBALL_KNOCKBACK = 1.8
FIREBALL_ATK = 3
FIREBALL_SPEED = 15

#ENHANCED_SPEED
ENHANCED_SPEED_PERCENT = 1.25

#BLEEDING
BLEEDING_TIME = 3*60 #in frames
BLEEDING_RATE = 0.6*60 #in frames
BLEEDING_DAMAGE = 1

#ATTACK WHILE DASHING
CARDS_NOTSTACKABLE.append('ATKESQUIVA_INCREASE') #NOT STACKABLE !!!!!!!!!!

#Aumenta o dano do primeiro ataque depois de usar uma esquiva, mas sua esquiva não te deixa invulnerável;
ATKESQUIVA_INCREASE = 2
CARDS_NOTSTACKABLE.append('ATK_WHILE_DASHING') #NOT STACKABLE !!!!!!!!!!

#Dá mais knockback
APLIES_MORE_KNOCKBACK = 1.4

#Recebe menos knockback
RECEIVES_LESS_KNOCKBACK = 1.5

#SURVIVAL (x% de vida -> ataque ++)
SURVIVAL_MIN_HP = 0.2
SURVIVAL_ATK_MULTPLIER = 1.5

#SPIKES
SPIKES_DAMAGE = 4
SPIKES_ATIME = 0.8*60 #in frames

#NO_SEE
NO_SEE_COOLDOWN = 2*60 #in frames
CARDS_NOTSTACKABLE.append('NO_SEE') #NOT STACKABLE !!!!!!!!!!

#DESCRIPTIONS
CARDS_DESCRIPTIONS = {
    None: "Carta Legal.",
    'FIREBALL': "oloco uma bola de fogo",
    'ENHANCED_SPEED': "Você fica {0}% mais    veloz".format(round(100*(ENHANCED_SPEED_PERCENT - 1))),
    'BLEEDING': "Aplica sangramento de {} segundos".format(round(BLEEDING_TIME/60)),
    'ATK_WHILE_DASHING': "Você pode atacar      enquanto da o dash",
    'ATKESQUIVA': "Aumenta o dano do primeiro ataque depois de usar uma esquiva, mas sua esquiva não te deixa invulnerável",
    'APLIES_MORE_KNOCKBACK': "Dá mais Knockback",
    'RECEIVES_LESS_KNOCKBACK': "Recebe menos Knockback",
    'SURVIVAL': "Ataque aumenta em {0}% se você estiver com vida baixa".format(round(100*(SURVIVAL_ATK_MULTPLIER - 1))),
    'SPIKES': "Espinhos surgem no local aonde você pulou",
    'NO_SEE': "Você fica invisível enquanto não leva dano"
}
CARDS_IMAGES = {
    None: "Carta Legal.",
    'FIREBALL': 'Graphics/cards/fireball.png',
    'ENHANCED_SPEED': 'Graphics/cards/speed.png',
    'BLEEDING': 'Graphics/cards/bleeding.png',
    'ATK_WHILE_DASHING': 'Graphics/cards/dashatk.png',
    'ATKESQUIVA': 'Graphics/cards/powerdash.png',
    'APLIES_MORE_KNOCKBACK': 'Graphics/cards/knock.png',
    'RECEIVES_LESS_KNOCKBACK': 'Graphics/cards/knockresi.png',
    'SURVIVAL': 'Graphics/cards/survival.png',
    'SPIKES': 'Graphics/cards/spikes.png',
    'NO_SEE': 'Graphics/cards/nosee.png',
}
