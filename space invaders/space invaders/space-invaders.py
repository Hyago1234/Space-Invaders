import pygame
from pygame.locals import *
import random
import os
import math
from pygame import mixer

pygame.init()
pygame.mixer.pre_init(44100, 16, 2, 4096)

# Configurações 
relogio = pygame.time.Clock()



#janela 
largura = 800
altura = 600
janela = pygame.display.set_mode((largura,altura))
pygame.display.set_caption('Space invaders')
icone = pygame.image.load('icone/spaceship.png')
pygame.display.set_icon(icone)

#background
janela_fundo = pygame.image.load('espaço-de-fundo/plano-de-fundo02.jpeg')
janela_fundo_Y = 0
janela_fundo_X = 0



#Player
player_image = pygame.image.load('nave-espacial/battleship.png')
largura_player = 64
altura_player = 64
playerX = (largura/2) - (largura_player/2)
playerY = (altura/2) - (altura_player/2)
playerX_mudanca = 0
pontos = 0
vidas = 10
derrota = False
vitoria = False
verificador_de_vitoria = 0
kills = 0

# Tiro/ Missil
missil = pygame.image.load('tiro/missile.png')
missil = pygame.transform.scale(missil , (30,30))
vel_y_missil = 0
pos_x_missil = playerX 
pos_y_missil = playerY
vel_x_missil = 0
vel_y_missil = 10
missil_estado = 'pronto'
balas = []

# Vamos usar a variavel bullet_state (pronto ou fogo) para controlar
#tiro_X = 0
#tiro_Y = 0
#tiro = pygame.draw.rect(janela, (255,0,0) , (tiro_X,tiro_Y,10,15))
#tiro_estado = 'pronto'

#Inimigo tipo 01
inimigo_image = pygame.image.load('inimigo01/space.png')
inimigo_image = pygame.transform.scale(inimigo_image , (60,60))
inimigo01_X = 0
inimigo01_Y = 0
largura_inimigo01 = 64
altura_inimigo01 = 64
inimigos_vivos01 = 0
inimigos01 = []
velocidades_inim_01 = []
num_min_inimigos = 1
num_max_inimigos = 3
velocidade_min_inimigo01 = 1
velocidade_max_inimigo01 = 3

# Inimigo tipo 2
inimigo_image02 = pygame.image.load('inimigo02/BigShip3.png')
inimigo_image02 = pygame.transform.scale(inimigo_image02 , (120,120))
laser_inimigo02 = pygame.image.load('tiro/laser-inimigo02.png')
laser_inimigo02 = pygame.transform.scale(laser_inimigo02 , (15,30))
inimigos_vivos02 = 0
inimigos02 = []
#velocidades_inim_02 = []
num_min_inimigos02 = 1
num_max_inimigos02 = 2
velocidade_min_inimigo02 = 1
velocidade_max_inimigo02 = 3


#Menu inicial
menu_inicial = True
tempo_menu = 0
imagem_menuinicial01 = pygame.image.load('background-menu/Space background.png')
imagem_menuinicial02 = pygame.image.load('background-menu/Space background02.png')
imagem_menuinicial03 = pygame.image.load('background-menu/Space background03.png')
imagens_menu_inicial = [imagem_menuinicial01,imagem_menuinicial02,imagem_menuinicial03]
tempo_menu = pygame.time.get_ticks()
conta_imagem = 0
intervalo_menu = 2000

#Tela de vitoria
imagem_tela_vitoria = pygame.image.load('espaço-de-fundo/space-image-bg.png')
imagem_tela_vitoria = pygame.transform.scale(imagem_tela_vitoria , (800,600))

#Texto
pygame.font.init()
fonte_menu01 = pygame.font.Font('fontes/techno_hideo.ttf', 60 )
texto_menu01 = fonte_menu01.render('Space Invaders' , True , (255,0,0))
fonte_menu02 = pygame.font.Font('fontes/Minercraftory.ttf',15)
texto_menu02 = fonte_menu02.render('Aperte espaço para continuar' , True , (255,0,0))
fonte_jogo01 = pygame.font.Font('fontes/Planet Comic.ttf', 20)
fonte_jogo02 = pygame.font.Font('fontes/Planet Comic.ttf', 20)
derrota_menu_fonte = pygame.font.Font('fontes/game_over.ttf' , 200)
derrota_menu_texto = derrota_menu_fonte.render('GAME OVER' , True , (139,0,0))
derrota_menu_fonte02 = pygame.font.Font('fontes/game_over.ttf' , 50)
derrota_menu_texto02 = derrota_menu_fonte02.render(f' 0 Vidas', True , (139,0,0))
vitoria_menu_fonte =  pygame.font.Font('fontes/game_over.ttf' , 200)
vitoria_menu_texto = vitoria_menu_fonte.render('YOU WIN' , True , (224, 214, 13))
vitoria_menu_fonte02 = pygame.font.Font('fontes/game_over.ttf' , 60)
vitoria_menu_texto02 = vitoria_menu_fonte02.render('8000 Pontos' , True , (224, 214, 13))

#Musicas
pygame.mixer.init()
menu_musica = pygame.mixer.music.load('musicas/bgm_1.mp3')
pygame.mixer.music.play(-1)
tiro_som = mixer.Sound('musicas/tiro_som.wav')
explosao_musica = pygame.mixer.Sound('musicas/Explosion.wav')
buff_musica = pygame.mixer.Sound('musicas/Powerup.wav')
colisao_inimigo_musica = pygame.mixer.Sound('musicas/explosion9.wav')

#Buffs
coracao_buff = pygame.image.load('buffs/coracao.png')
coracao_buff = pygame.transform.scale(coracao_buff , (60,60))
numero_coracoes = 0
coracoes_buff = []
coracao_tela = 0
controle_spawns = []
# Funções
def player(playerX,playerY):
    janela.blit(player_image,(playerX,playerY))

def inimigo01(inimigo01_X,inimigo01_Y):
    janela.blit(inimigo_image, (inimigo01_X,inimigo01_Y))

def tiro(X,Y):
    global missil_estado
    missil_estado = 'fogo'
    janela.blit(missil , (X + 17,Y - 30))
def respaw_inimigo01():
    y = 0
    x = random.randint(1,740)
    return [x,y]
def respaw_inimigo02():
    y = 0
    x = random.randint(1, 680)
    return [x,y]
def iscollision(inimigo01_X,inimigo01_Y, pos_x_missil,pos_y_missil):
    distance = math.sqrt(math.pow(inimigo01_X - pos_x_missil ,2) + math.pow(inimigo01_Y - pos_y_missil,2))
    if distance < 50:
        return True
    else:
        return False
def colisaonave(inimigo01_X , inimigo01_Y , pos_x_missil , pos_y_missil):
    distance = math.sqrt(math.pow(inimigo01_X - pos_x_missil ,2) + math.pow(inimigo01_Y - pos_y_missil,2))
    if distance < 64:
        return True
    else:
        return False
def colisaonave02(inimigo02_X,inimigo02_Y,playerX,playerY):
    distance = math.sqrt(math.pow(inimigo02_X - playerX ,2) + math.pow(inimigo02_Y - playerY,2))
    if distance < 120:
        return True
    else:
        return False
def gerar_buff():
    return[random.randint(0,740),0]
def reinicializar():
    #Variaveis do player
    global vidas
    global playerX
    global playerY
    global pontos
    global playerX_mudanca
    global kills
    #Variaveis do missil
    global vel_x_missil
    global vel_y_missil
    global pos_x_missil
    global pos_y_missil
    global missil_estado
    global balas
    #Variaveis inimigo01
    global inimigo01_X
    global inimigo01_Y
    global largura_inimigo01
    global altura_inimigo01
    global inimigos_vivos01
    global inimigos01
    global velocidades_inim_01
    global num_min_inimigos
    global num_max_inimigos
    global velocidade_max_inimigo01
    global velocidade_min_inimigo01
    #Variaveis inimigo02
    global inimigos02
    global num_max_inimigos02
    global num_min_inimigos02
    global velocidade_max_inimigo02
    global velocidade_min_inimigo02
    #Variaveis buffs
    global numero_coracoes
    global coracoes_buff
    global coracao_tela
    global controle_spawns 
    #Variaveis menu
    global tempo_menu
    global intervalo_menu
    # Variaveis de controle 
    global verificador_de_vitoria
    #Variaveis do player
    vidas = 10
    playerX = (largura/2) - (largura_player/2)
    playerY = (altura/2) - (altura_player/2)
    playerX_mudanca = 0
    pontos = 0
    kills = 0
    #Variaveis do missil
    vel_y_missil = 0
    pos_x_missil = playerX 
    pos_y_missil = playerY
    vel_x_missil = 0
    vel_y_missil = 10
    missil_estado = 'pronto'
    balas = []
    #Variaveis inimigo 01
    inimigo01_X = 0
    inimigo01_Y = 0
    largura_inimigo01 = 64
    altura_inimigo01 = 64
    inimigos_vivos01 = 0
    inimigos01 = []
    velocidades_inim_01 = []
    num_min_inimigos = 1
    num_max_inimigos = 3
    velocidade_min_inimigo01 = 1
    velocidade_max_inimigo01 = 3
    #Variaveis inimigo 02
    inimigos02 = []
    num_min_inimigos02 = 1
    num_max_inimigos02 = 2
    velocidade_min_inimigo02 = 1
    velocidade_max_inimigo02 = 3
    #Variaveis buffs
    numero_coracoes = 0
    coracoes_buff = []
    coracao_tela = 0
    controle_spawns = []
    #Variaveis menu
    tempo_menu = pygame.time.get_ticks()
    intervalo_menu = tempo_menu + 1000
    # Variaveis de controle 
    verificador_de_vitoria = 0
# Loop do jogo
run = True
while run:
    relogio.tick(80)
    #Menu inicial 
    while menu_inicial:
        relogio.tick(80)
        janela.fill((255,255,255))
        tempo_menu = pygame.time.get_ticks()
        if tempo_menu in range(intervalo_menu,intervalo_menu + 200) and tempo_menu != 0:
            conta_imagem += 1
            intervalo_menu += 2000
        if conta_imagem > 2:
            conta_imagem = 0
        janela.blit(imagens_menu_inicial[conta_imagem] , (0,0))
        janela.blit(texto_menu01 , (130,200))
        janela.blit(texto_menu02, (240,500))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                menu_inicial = False
                pygame.time.wait(1000)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    menu_inicial = False
                    pygame.time.wait(1000)
        pygame.display.update()
        janela.fill((0,0,150))
    if run == False:
        break
    # plano de fundo dinamico
    janela.blit(janela_fundo,(janela_fundo_X,janela_fundo_Y))
    rel_y = janela_fundo_Y % janela_fundo.get_rect().height
    janela.blit(janela_fundo , (0, rel_y - janela_fundo.get_rect().height))
    if rel_y < 600:
        janela.blit(janela_fundo , (0, rel_y))
    janela_fundo_Y += 1
    # Leitura dos inputs
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                tiro_som.play()
                balas.append([playerX + 15,playerY - 30])
    #Movimentação do jogador
    if pygame.key.get_pressed()[K_d]:
        playerX += 10
    if pygame.key.get_pressed()[K_a]:
        playerX -= 10
    if pygame.key.get_pressed()[K_s]:
        playerY += 10
    if pygame.key.get_pressed()[K_w]:
        playerY -= 10
    #limitação do movimento do jogador em X
    if playerX < 0:
        playerX = 0
    elif playerX > (largura - largura_player):
        playerX = largura - largura_player
    #limitação do movimento do jogador em Y
    if playerY < 0:
        playerY = 0
    if playerY > (altura - altura_player):
        playerY = altura - altura_player
    # Tiro movimento
    #if missil_estado == 'fogo':
    #    tiro(pos_x_missil , pos_y_missil)
    #    pos_y_missil -= vel_y_missil
    if kills > 25:
        num_min_inimigos = 3
        num_max_inimigos = 4
        velocidade_min_inimigo01 = 3
        velocidade_max_inimigo01 = 4
    if kills > 40:
        num_min_inimigos = 4
        num_max_inimigos = 4
        velocidade_min_inimigo01 = 4
        velocidade_max_inimigo01 = 4
    # Gerando o inimigo01 e o jogador    
    janela.blit(player_image,(playerX,playerY))
    numero_inimigos_01 = random.randint(num_min_inimigos,num_max_inimigos)
    if inimigos_vivos01 == 0:
        inimigos_vivos01 = numero_inimigos_01
        for i in range(0,numero_inimigos_01):
            inimigos01.append(respaw_inimigo01())
            inimigos01[i].append(random.randint(velocidade_min_inimigo01,velocidade_max_inimigo01))
    for elemento in inimigos01:
        janela.blit(inimigo_image , (elemento[0],elemento[1]))
        elemento[1] += elemento[2]
        if elemento[1] > 600:
            vidas -= 1
            inimigos01.remove(elemento)
            explosao_musica.play()
    if len(inimigos01) == 0:
        inimigos_vivos01 = 0
    #Gerando o inimgio 02
    if kills > 10 and inimigos_vivos02==0:
        numero_inimigos_02 = random.randint(num_min_inimigos02,num_max_inimigos02)
    else:
        numero_inimigos_02 = 0
    if inimigos_vivos02 == 0:
        inimigos_vivos02 = numero_inimigos_02
        for i in range(0,numero_inimigos_02):
            inimigos02.append(respaw_inimigo02())
            inimigos02[i].append(2)
            inimigos02[i].append(random.randint(velocidade_min_inimigo02,velocidade_max_inimigo02))
    for elemento in inimigos02:
        janela.blit(inimigo_image02 , (elemento[0],elemento[1]))
        elemento[1] += elemento[2]
        if elemento[1] > 600:
            vidas -= 1
            explosao_musica.play()
            inimigos02.remove(elemento)
    if len(inimigos02) == 0:
        inimigos_vivos02 = 0
    # Colisao inimigo 02 com os misseis
    for inimigo02 in inimigos02:
        for tiros in balas:
            colisao = colisaonave02(inimigo02[0],inimigo02[1],tiros[0],tiros[1])
            if colisao:
                inimigo02[2] -= 1
                balas.remove(tiros)
                colisao_inimigo_musica.play()
        if inimigo02 in inimigos02:
            if colisaonave02(inimigo02[0],inimigo02[1],playerX,playerY):
                vidas -= 1
                inimigos02.remove(inimigo02)
                explosao_musica.play()
        if inimigo02 in inimigos02:
            if inimigo02[2] == 0:
                pontos += 200
                inimigos02.remove(inimigo02)
    # Gerando buffs
    coracao_tela = len(coracoes_buff)
    if kills%10==0 and kills!=0 and coracao_tela == 0 and (kills not in controle_spawns):
        numero_coracoes = 1
        controle_spawns.append(kills)
    if numero_coracoes != 0:
        coracoes_buff.append(gerar_buff())
        numero_coracoes = 0
    for coracoes in coracoes_buff:
        janela.blit(coracao_buff , (coracoes[0] , coracoes[1]))
        coracoes[1] += 3
        if coracoes in coracoes_buff:
            if coracoes[1] > 600:
                coracoes_buff.remove(coracoes)
        if iscollision(coracoes[0],coracoes[1], playerX , playerY):
            buff_musica.play()
            vidas += 1
            coracoes_buff.remove(coracoes)
    for elemento in balas:
        janela.blit(missil , (elemento[0],elemento[1]))
        elemento[1] -= vel_y_missil
        if elemento[1] < 0:
            balas.remove(elemento)
    # Colisao inimigo 01 com espaço nave
    for inimigo in inimigos01:
        for tiros in balas:
            colisao = iscollision(inimigo[0],inimigo[1],tiros[0],tiros[1])
            if colisao:
                colisao_inimigo_musica.play()
                pontos += 100
                kills += 1
                inimigos01.remove(inimigo)
                balas.remove(tiros)
        if inimigo in inimigos01:
            if colisaonave(inimigo[0],inimigo[1],playerX,playerY):
                explosao_musica.play()
                vidas -= 1
                inimigos01.remove(inimigo)
    # Desenhando as vidas e o pontos na tela
    janela.blit(fonte_jogo01.render(f'Pontos: {pontos}' , True , (255,255,255)) , (0,0))
    janela.blit(fonte_jogo02.render(f'Vidas: {vidas}' , True , (255,255,255)), (0,20))
    janela.blit(fonte_jogo02.render(f'Kills: {kills}' , True , (255,255,255)) , (0,40))
    # Vitoria menu
    if pontos >= 8000:
        vitoria = True
    while vitoria:
        relogio.tick(80)
        janela.fill((0,0,255))
        janela.blit(imagem_tela_vitoria , (0,0))
        janela.blit(vitoria_menu_texto , (220,30))
        janela.blit(vitoria_menu_texto02 , (330,altura/2 - 50))
        janela.blit(vitoria_menu_fonte02.render('Pressione backspace para retornar ao menu', True , (224, 214, 13)) , (largura/2 - 230 , 550))
        if verificador_de_vitoria == 0:
            verificador_de_vitoria += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                vitoria = False
                pygame.time.wait(1000)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    vitoria = False
                    menu_inicial = True
                    reinicializar()
                    pygame.time.wait(1000)
        pygame.display.update()
    # deerota menu
    if vidas <= 0:
        derrota = True
    while derrota and verificador_de_vitoria==0:
        relogio.tick(80)
        janela.fill((0,0,0))
        janela.blit(derrota_menu_texto , (160, 50))
        janela.blit(derrota_menu_texto02 , (largura/2 - 50, altura/2 - 50))
        janela.blit(derrota_menu_fonte02.render('Pressione backspace para retornar ao menu', True , (139,0,0)) , (largura/2 - 200 , 550))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                derrota = False
                pygame.time.wait(1000)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    derrota = False
                    menu_inicial = True
                    reinicializar()
                    pygame.time.wait(1000)
        pygame.display.update()
    pygame.display.update()