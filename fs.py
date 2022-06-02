#FUNÇÕES

def sign(value_): #RETORNA O SINAL DO VALOR PASSADO
    if value_ != 0:
        return value_/abs(value_)
    return 0 #0 se n for nem positivo nem negativo

def pointDistance(x1,y1,x2,y2): #RETORNA A DISTANCIA ENTRE DOIS PONTOS
    return ((x1 - x2)**2 + (y1 - y2)**2)**(1/2)

def friction(speed_,friction_): #RETORNA A VELOCIDADE DPS DE APLICADA UMA FRICÇÃO
    if abs(speed_) > friction_:
        return speed_ - friction_*sign(speed_)
    else:
        return 0

def collisionList(collidee_list,tuple_xy):

    #RETORNA UMA LISTA COM [TA COLIDINDO OU NÃO?, QUEM EU TO COLIDINDO]

    #Verifica se ta colidindo com cada elemento de collidee_list
    for collidee_ in collidee_list:
        if collidee_.hit_box.collidepoint(tuple_xy) == True:
            return [True,collidee_] #Se ta colidindo com pelomenos 1

    return [False,-1]

<<<<<<< HEAD
def loopValue(value_,min_,max_,_speed):
=======
#Loops values
def loop_value(value_,min_,max_,_speed):
>>>>>>> d4d4526bd5c25ed4ca4f82450d9c65cdcc453195
    if value_ + _speed <= max_:
        return value_ + _speed
    else:
        return min_
