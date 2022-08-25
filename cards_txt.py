import pygame as pg

CARDS_NOTSTACKABLE = []

#FIREBALL
FIREBALL_ATK_RANGE = 240*2
FIREBALL_ATIME = 1.2*60 #in frames
FIREBALL_KNOCKBACK = 1.2
FIREBALL_ATK = 2
FIREBALL_SPEED = 14

#ENHANCED_SPEED
ENHANCED_SPEED_PERCENT = 1.25

#BLEEDING
BLEEDING_TIME = 2*60 #in frames
BLEEDING_RATE = 24 #in frames
BLEEDING_DAMAGE = 0.6

#ATTACK WHILE DASHING
#CARDS_NOTSTACKABLE.append('ATKESQUIVA_INCREASE') #NOT STACKABLE !!!!!!!!!!

#Aumenta o dano do primeiro ataque depois de usar uma esquiva, mas sua esquiva não te deixa invulnerável;
ATKESQUIVA_INCREASE = 1.25
CARDS_NOTSTACKABLE.append('ATK_WHILE_DASHING') #NOT STACKABLE !!!!!!!!!!

#Dá mais knockback
APLIES_MORE_KNOCKBACK = 1.35

#Recebe menos knockback
RECEIVES_LESS_KNOCKBACK = 1.6
RECEIVES_LESS_DAMAGE = 0.15

#SURVIVAL (x% de vida -> ataque ++)
SURVIVAL_MIN_HP = 0.2
SURVIVAL_ATK_MULTPLIER = 1.5

#SPIKES
SPIKES_DAMAGE = 4
SPIKES_ATIME = 0.8*60 #in frames

#NO_SEE
NO_SEE_COOLDOWN = 2*60 #in frames
CARDS_NOTSTACKABLE.append('NO_SEE') #NOT STACKABLE !!!!!!!!!!

#ICEFORM
ICE_CHANCE = 0.2 #in frames
ICE_TIME = 0.6*60
ICE_SLOW = 0.3
ICEBALL_ATIME = 1.2*60 #in frames
ICEBALL_SPEED = 7

#ANTIGRAV
ANTIG_ATK = 0.2*60

#HARDATK
HARDATK = 1
#DESCRIPTIONS
CARDS_DESCRIPTIONS = {
    None: "Carta Legal.",
    'FIREBALL': 'Atacar longe de inimigos invoca uma bola de fogo.',
    'ENHANCED_SPEED': "Você fica {0}% mais veloz.".format(round(100*(ENHANCED_SPEED_PERCENT - 1))),
    'BLEEDING': "Ataques fazem inimigos sangrarem por {} segundos.".format(round(BLEEDING_TIME/60)),
    'ATK_WHILE_DASHING': "Você pode atacar enquanto usa a esquiva.",
    'ATKESQUIVA': "Aumenta o dano do primeiro ataque depois de usar uma esquiva, mas sua esquiva não te deixa invulnerável.",
    'APLIES_MORE_KNOCKBACK': "Ataques aplicam {}% a mais repulsão.".format(round(100*(APLIES_MORE_KNOCKBACK - 1))),
    'RECEIVES_LESS_KNOCKBACK': "Recebe {}% a menos repulsão e {}% a menos de dano.".format(round(100*(RECEIVES_LESS_KNOCKBACK-1)), round(100*RECEIVES_LESS_DAMAGE)),
    'SURVIVAL': "Ataque aumenta em {}% se você estiver com vida baixa.".format(round(100*(SURVIVAL_ATK_MULTPLIER - 1))),
    'SPIKES': "Espinhos surgem no local aonde você pulou.",
    'NO_SEE': "Você fica invisível enquanto não levar dano.",
    'DJUMP':  "Ganha um pulo extra mas seu pulo fica mais fraco.",
    'ICEFORM': "{}% de chance de lançar uma bola congelante, que desacelera o alvo por {} segundo(s)".format(round(100*ICE_CHANCE), ICE_TIME/60),
    'ANTIGRAV':'Ataques paralizam por mais tempo e deixam o alvo em gravidade zero por {} segundo(s)'.format(ANTIG_ATK/60),
    'HARDATK':'Ataques causam mais {} ponto(s) de dano'.format(HARDATK)
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
    'DJUMP': 'Graphics/cards/doublejump.png',
    'ICEFORM':'Graphics/cards/icebeam.png',
    'ANTIGRAV':'Graphics/cards/antigrav.png',
    'HARDATK':'Graphics/cards/axe.png'
}
