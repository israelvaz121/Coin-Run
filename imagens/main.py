import pygame
import time
import random

# Inicialização
pygame.init()
fonte = pygame.font.SysFont("Verdana", 36)

# Janela
LARGURA, ALTURA = 1000, 600
display = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Coin Run")
clock = pygame.time.Clock()

# Jogador
player = pygame.Rect(300, 300, 40, 40)

# Plataformas
plataformas = [
    pygame.Rect(150, 450, 120, 90),
    pygame.Rect(400, 400, 150, 90),
    pygame.Rect(500, 200, 140, 90),
    pygame.Rect(250, 250, 150, 90),
    pygame.Rect(650, 350, 170, 90),
]

# Imagens
try:
    plataforma_img = pygame.image.load("C:/Users/Heitor Vaz/.vscode/projeto/imagens/asd.png").convert_alpha()
except Exception as e:
    print(f"Erro ao carregar imagem da plataforma: {e}")
    plataforma_img = None

try:
    moeda_img = pygame.image.load("C:/Users/Heitor Vaz/.vscode/projeto/imagens/coin2.png").convert_alpha()
    moeda_img = pygame.transform.scale(moeda_img, (40, 40))
except Exception as e:
    print(f"Erro ao carregar imagem da moeda: {e}")
    moeda_img = None

try:
    fundo = pygame.image.load("C:/Users/Heitor Vaz/.vscode/projeto/imagens/fundo.png")
    fundo = pygame.transform.scale(fundo, (LARGURA, ALTURA))
except Exception as e:
    print(f"Erro ao carregar imagem de fundo: {e}")
    fundo = None

# Moeda
moeda_rect = pygame.Rect(100, 100, 40, 40)

# Variáveis
pontos = 0
velocidade = 5
gravidade = 1
velocidadey = 0
forca_pulo = -20
chao = False
telacheia = False

# Poder
poder_ativo = False
tempopoder = 5
recarga = 30
ultimouso = -recarga
iniciopoder = 0

# Função de desenho
def draw():
    display.blit(fundo, (0, 0)) if fundo else display.fill((4, 128, 97))

    cor_jogador = (0, 0, 255) if poder_ativo else (255, 0, 0)
    pygame.draw.rect(display, cor_jogador, player)

    if moeda_img:
        display.blit(moeda_img, moeda_rect.topleft)
    else:
        pygame.draw.rect(display, (255, 255, 0), moeda_rect)

    for plat in plataformas:
        if plataforma_img:
            plat_img = pygame.transform.scale(plataforma_img, (plat.width, plat.height))
            display.blit(plat_img, plat.topleft)
        else:
            pygame.draw.rect(display, (0, 0, 0), plat)

    texto = fonte.render(f"Pontos: {pontos}", True, (255, 255, 255))
    display.blit(texto, (20, 20))

    if poder_ativo:
        status = "Poder ativo!"
        cor = (0, 255, 0)
    else:
        restante = max(0, recarga - (time.time() - ultimouso))
        status = f"Recarga: {restante:.1f}s"
        cor = (255, 255, 255)

    texto2 = fonte.render(status, True, cor)
    display.blit(texto2, (20, 60))

# Loop principal
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
                modo = pygame.FULLSCREEN if telacheia else 0
                display = pygame.display.set_mode((LARGURA, ALTURA), modo)
                if fundo:
                    fundo = pygame.transform.scale(fundo, (LARGURA, ALTURA))

            if event.key == pygame.K_SPACE and chao:
                velocidadey = forca_pulo

            if event.key == pygame.K_q and not poder_ativo and agora - ultimouso >= recarga:
                poder_ativo = True
                iniciopoder = ultimouso = agora
                forca_pulo = -27
                velocidade = 8

    # Desativar poder após o tempo
    if poder_ativo and agora - iniciopoder >= tempopoder:
        poder_ativo = False
        forca_pulo = -20
        velocidade = 5

    # Movimento lateral
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        player.x -= velocidade
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        player.x += velocidade

    # Física
    velocidadey += gravidade
    player.y += velocidadey

    # Impede sair da tela
    player.x = max(0, min(player.x, LARGURA - player.width))
    player.y = max(0, min(player.y, ALTURA - player.height))

    # Verifica se está no chão
    if player.y + player.height >= ALTURA:
        player.y = ALTURA - player.height
        velocidadey = 0
        chao = True
    else:
        chao = False

    # Colisão com plataformas
    for plat in plataformas:
        if player.colliderect(plat):
            if velocidadey > 0 and player.bottom <= plat.bottom:
                player.bottom = plat.top
                velocidadey = 0
                chao = True

    # Coleta da moeda
    if player.colliderect(moeda_rect):
        pontos += 1

        # Gera nova posição até não colidir com plataformas
        while True:
            moeda_rect.x = random.randint(0, LARGURA - moeda_rect.width)
            moeda_rect.y = random.randint(0, ALTURA - moeda_rect.height)

            # Verifica se a moeda colide com alguma plataforma
            colidiu = False
            for plat in plataformas:
                if moeda_rect.colliderect(plat):
                    colidiu = True
                    break

            if not colidiu:
                break  # moeda em posição segura

    # Desenho
    draw()
    pygame.display.update()

pygame.quit()