
import pygame
import time
import random

pygame.init()
fonte = pygame.font.SysFont("Verdana", 36)

# janela
display = pygame.display.set_mode((1000, 600))
pygame.display.set_caption("jogo#1")
clock = pygame.time.Clock()

# jogador e obstáculos
player = pygame.Rect(300, 300, 40, 40)
inimigo = pygame.Rect(50, 50, 40, 40)
obstaculo = [
    pygame.Rect(150, 450, 120, 20),
    pygame.Rect(400, 400, 150, 20),
    pygame.Rect(650, 350, 120, 20),
    pygame.Rect(250, 250, 100, 20),
    pygame.Rect(500, 200, 150, 20)
]
moeda = pygame.Rect(100, 100, 20, 20)

# variáveis
try:
    fundo = pygame.image.load("imagens/fundo.png")
    fundo = pygame.transform.scale(fundo, (1000, 600))
except Exception as e:
    print(f"Erro ao carregar imagem de fundo: {e}")
    fundo = None  # caso não encontre a imagem, o fundo fica vazio

pontos = 0
velocidade = 5
velocidadeinimigo = 2
gravidade = 1
velocidadey = 0
forc_pulo = -20
chao = False
telacheia = False

# Variáveis do inimigo para física de pulo
velocidadey_inimigo = 0
gravidade_inimigo = 1
forca_pulo_inimigo = -15

# cooldown para o pulo do inimigo
tempo_ultimo_pulo_inimigo = 0
cooldown_pulo_inimigo = 1.0  # segundos

# poder
poder_ativo = False
tempopoder = 5  # segundos de duração
recarga = 30  # segundos de recarga
ultimouso = -recarga  # começa disponível
iniciopoder = 0  # precisa iniciar para controle de tempo


def reiniciar_fase():
    global player, inimigo, moeda, pontos, velocidade, velocidadeinimigo
    global velocidadey, forc_pulo, chao, poder_ativo, ultimouso, iniciopoder
    global velocidadey_inimigo, tempo_ultimo_pulo_inimigo

    player.x, player.y = 300, 300
    inimigo.x, inimigo.y = 50, 50
    moeda.x, moeda.y = random.randint(0, 980), random.randint(0, 580)
    pontos = 0
    velocidade = 5
    velocidadeinimigo = 2
    velocidadey = 0
    forc_pulo = -20
    chao = False
    poder_ativo = False
    ultimouso = -recarga
    iniciopoder = 0
    velocidadey_inimigo = 0
    tempo_ultimo_pulo_inimigo = 0


def draw(agora):
    if fundo:
        display.blit(fundo, (0, 0))
    else:
        display.fill([4, 128, 97])  # cor verde caso não tenha fundo

    cor_jogador = (0, 0, 255) if poder_ativo else (255, 0, 0)
    pygame.draw.rect(display, (57, 227, 23), inimigo)
    pygame.draw.rect(display, cor_jogador, player)
    pygame.draw.rect(display, (255, 255, 0), moeda)
    for o in obstaculo:
        pygame.draw.rect(display, (0, 0, 0), o)

    texto = fonte.render(f"Pontos: {pontos}", True, (255, 255, 255))

    if poder_ativo:
        texto2 = fonte.render("Poder ativo!", True, (0, 255, 0))
    else:
        tempo_recarga_restante = max(0, recarga - (agora - ultimouso))
        texto2 = fonte.render(f"Recarga: {tempo_recarga_restante:.1f}s", True, (255, 255, 255))

    display.blit(texto, (20, 20))
    display.blit(texto2, (20, 60))


# Função para verificar se inimigo está no chão/plataforma
def inimigo_esta_no_chao():
    # chão da tela
    if inimigo.bottom >= 600:
        return True

    # obstáculos logo abaixo (com margem de 5 px)
    for o in obstaculo:
        if (
            inimigo.bottom >= o.top - 5 and inimigo.bottom <= o.top + 5
            and inimigo.right > o.left and inimigo.left < o.right
            and velocidadey_inimigo >= 0
        ):
            return True
    return False


# loop do jogo
gameloop = True
while gameloop:
    clock.tick(60)
    agora = time.time()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameloop = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F11:
                telacheia = not telacheia
                if telacheia:
                    display = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                else:
                    display = pygame.display.set_mode((1000, 600))

            if event.key == pygame.K_SPACE and chao:
                velocidadey = forc_pulo

            if event.key == pygame.K_q:
                if not poder_ativo and agora - ultimouso >= recarga:
                    poder_ativo = True
                    iniciopoder = agora
                    ultimouso = agora
                    forc_pulo = -27
                    velocidade = 8

    if poder_ativo and agora - iniciopoder >= tempopoder:
        poder_ativo = False
        forc_pulo = -20
        velocidade = 5

    keys = pygame.key.get_pressed()
    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        player.x -= velocidade
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        player.x += velocidade

    # Limites da tela jogador
    if player.left < 0:
        player.left = 0
    if player.right > 1000:
        player.right = 1000
    if player.top < 0:
        player.top = 0
    if player.bottom > 600:
        player.bottom = 600

    # gravidade jogador
    velocidadey += gravidade
    player.y += velocidadey

    # colisão com chão jogador
    if player.y + player.height >= 600:
        player.y = 600 - player.height
        velocidadey = 0
        chao = True
    else:
        chao = False

    # colisão com obstáculos jogador
    for o in obstaculo:
        if player.colliderect(o):
            if player.y + player.height > o.y and velocidadey > 0:
                player.y = o.y - player.height
                velocidadey = 0
                chao = True

    # pegar moeda
    if player.colliderect(moeda):
        pontos += 1
        print(f"Pontos: {pontos}")
        moeda.x = random.randint(0, 980)
        moeda.y = random.randint(0, 580)

    # movimentação inimigo (segue jogador)
    if inimigo.x < player.x:
        inimigo.x += velocidadeinimigo
    elif inimigo.x > player.x:
        inimigo.x -= velocidadeinimigo

    # Limites da tela inimigo
    if inimigo.left < 0:
        inimigo.left = 0
    if inimigo.right > 1000:
        inimigo.right = 1000
    if inimigo.top < 0:
        inimigo.top = 0
    if inimigo.bottom > 600:
        inimigo.bottom = 600

    # Atualiza flag inimigo no chão
    inimigo_chao = inimigo_esta_no_chao()

    # Lógica de pulo do inimigo com cooldown para evitar tremelicado
    altura_max_pulo = 60
    distancia_frontal = 50
    inimigo_pular = False

    if inimigo_chao and (agora - tempo_ultimo_pulo_inimigo) >= cooldown_pulo_inimigo:
        for o in obstaculo:
            alinhado = abs(inimigo.centerx - o.centerx) < distancia_frontal
            acima = o.y < inimigo.y and (inimigo.y - o.y) < altura_max_pulo

            if alinhado and acima:
                inimigo_pular = True
                break

    if inimigo_pular and inimigo_chao:
        velocidadey_inimigo = forca_pulo_inimigo
        tempo_ultimo_pulo_inimigo = agora  # registra o tempo do pulo

    # gravidade inimigo
    velocidadey_inimigo += gravidade_inimigo
    inimigo.y += velocidadey_inimigo

    # colisão com chão inimigo
    if inimigo.y + inimigo.height >= 600:
        inimigo.y = 600 - inimigo.height
        velocidadey_inimigo = 0
        inimigo_chao = True
    else:
        # inimigo_chao já foi definido pela função inimigo_esta_no_chao()
        pass

    # colisão com obstáculos inimigo
    for o in obstaculo:
        if inimigo.colliderect(o):
            if inimigo.y + inimigo.height > o.y and velocidadey_inimigo > 0:
                inimigo.y = o.y - inimigo.height
                velocidadey_inimigo = 0
                inimigo_chao = True

    # colisão inimigo e jogador
    if inimigo.colliderect(player):
        pygame.time.delay(500)
        reiniciar_fase()

    draw(agora)
    pygame.display.update()

pygame.quit()