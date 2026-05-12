import pygame
import random
import sys
import time

pygame.init()

# звук
coin_sound = None
gameover_sound = None

try:
    coin_sound = pygame.mixer.Sound("sounds/coin.wav")
    gameover_sound = pygame.mixer.Sound("sounds/gameover.wav")
except:
    print("⚠️ Звуки не найдены")

# 📱 экран телефона
GAME_WIDTH, GAME_HEIGHT = 360, 640
SCREEN_WIDTH, SCREEN_HEIGHT = 500, 800

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Som Game")

game_screen = pygame.Surface((GAME_WIDTH, GAME_HEIGHT))

font = pygame.font.SysFont("Arial", 22)

# ================= STATES =================
LOCK = 0
RULES = 1
GAME = 2

state = LOCK

# ================= GAME =================
player = pygame.Rect(150, 580, 60, 20)
speed = 6

coins = []
score = 0
lives = 3

fall_speed = 2
spawn_timer = 0

clock = pygame.time.Clock()

# монеты
coin_types = [
    {"value": 1, "color": (255, 215, 0)},
    {"value": 3, "color": (0, 150, 255)},
    {"value": 5, "color": (0, 255, 0)},
    {"value": 10, "color": (255, 0, 0)},
]


# ================= BLUR =================
def blur(surface, scale=0.08):
    size = surface.get_size()
    small = pygame.transform.smoothscale(surface, (int(size[0]*scale), int(size[1]*scale)))
    return pygame.transform.smoothscale(small, size)


# ================= LOCK SCREEN =================
def draw_lock():
    game_screen.fill((10, 10, 10))

    big = pygame.font.SysFont("Arial", 60)
    small = pygame.font.SysFont("Arial", 20)

    time_text = big.render(time.strftime("%H:%M"), True, (255, 255, 255))
    game_screen.blit(time_text, (GAME_WIDTH//2 - time_text.get_width()//2, 200))

    txt = small.render("Click to unlock", True, (180, 180, 180))
    game_screen.blit(txt, (GAME_WIDTH//2 - txt.get_width()//2, 500))


# ================= RULES =================
rules = [
    ((255, 215, 0), "1 сом"),
    ((0, 150, 255), "3 сома"),
    ((0, 255, 0), "5 сомов"),
    ((255, 0, 0), "10 сомов"),
]


def draw_rules():
    game_screen.fill((245, 245, 245))

    title = font.render("📜 RULES", True, (0, 0, 0))
    game_screen.blit(title, (130, 40))

    y = 120

    for color, text in rules:
        pygame.draw.circle(game_screen, color, (60, y + 10), 8)
        txt = font.render(text, True, (0, 0, 0))
        game_screen.blit(txt, (80, y))
        y += 50

    extra = [
        "❤️ 3 жизни",
        "❌ Пропустил = -1 жизнь",
        "🎯 Собирай монеты",
        "",
        "👉 Click to start"
    ]

    for i, t in enumerate(extra):
        txt = font.render(t, True, (0, 0, 0))
        game_screen.blit(txt, (60, y + i * 35))


# ================= GAME =================
def spawn_coin():
    c = random.choice(coin_types)
    rect = pygame.Rect(random.randint(20, GAME_WIDTH - 40), 30, 30, 30)
    coins.append({"rect": rect, "value": c["value"], "color": c["color"]})


def draw_game():
    global spawn_timer, score, lives, state

    game_screen.fill((255, 255, 255))

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] and player.x > 0:
        player.x -= speed
    if keys[pygame.K_RIGHT] and player.x < GAME_WIDTH - player.width:
        player.x += speed

    spawn_timer += 1
    if spawn_timer > 180:
        spawn_coin()
        spawn_timer = 0

    for coin in coins[:]:
        coin["rect"].y += fall_speed

        if player.colliderect(coin["rect"]):
            score += coin["value"]
            coins.remove(coin)
            if coin_sound:
                coin_sound.play()

        elif coin["rect"].y > GAME_HEIGHT:
            coins.remove(coin)
            lives -= 1
            if lives <= 0:
                state = RULES
                lives = 3
                score = 0
                coins.clear()

    pygame.draw.rect(game_screen, (0, 0, 0), player)

    for coin in coins:
        pygame.draw.circle(
            game_screen,
            coin["color"],
            (coin["rect"].x, coin["rect"].y),
            15
        )

    game_screen.blit(font.render(f"💰 {score} сом", True, (0, 0, 0)), (10, 10))
    game_screen.blit(font.render(f"❤️ {lives}", True, (255, 0, 0)), (10, 40))


# ================= LOOP =================
while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:

            if state == LOCK:
                state = RULES

            elif state == RULES:
                state = GAME

    # ================= STATE DRAW =================
    if state == LOCK:
        draw_lock()

    elif state == RULES:
        draw_rules()

    elif state == GAME:
        draw_game()

    # ================= PHONE FRAME =================
    screen.fill((40, 40, 40))

    x = (SCREEN_WIDTH - GAME_WIDTH) // 2
    y = (SCREEN_HEIGHT - GAME_HEIGHT) // 2

    pygame.draw.rect(
        screen,
        (0, 0, 0),
        (x - 10, y - 10, GAME_WIDTH + 20, GAME_HEIGHT + 20),
        border_radius=30
    )

    screen.blit(game_screen, (x, y))

    pygame.display.update()
    clock.tick(60)