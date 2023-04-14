import pygame
from  random import randint
import sys

pygame.init()
pygame.font.init()
pygame.mixer.init()

screen = pygame.display.set_mode((800, 400))
normal_font = pygame.font.Font("Game_Files/freesansbold.ttf", 60)
normal_font_small = pygame.font.Font("Game_Files/freesansbold.ttf", 30)
pixel_font = pygame.font.Font("Game_Files/pixel.ttf", 60)

icon = pygame.image.load("Game_files/Icon.png")
pygame.display.set_icon(icon)
pygame.display.set_caption("Subaqua")

clock = pygame.time.Clock()

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)

text = normal_font.render("Press space to start.", True, red)
text_rect = text.get_rect(center = (400, 60))

ocean = pygame.image.load("Graphics/Background/Background.png").convert()
ocean_rect = ocean.get_rect(topleft = (0, 0))

submarine = pygame.image.load("Graphics/Player/Default.png").convert_alpha()
submarine_rect = submarine.get_rect(center = (100, 250))
submarine_mask = pygame.mask.from_surface(submarine)

obstacle1 = pygame.image.load("Graphics/Items/Obstacle1.png").convert_alpha()
obstacle1_rect = obstacle1.get_rect(center = (900, 100))
obstacle1_mask = pygame.mask.from_surface(obstacle1)

obstacle2 = pygame.image.load("Graphics/Items/Obstacle2.png").convert_alpha()
obstacle2_rect =obstacle2.get_rect(center = (1400, 200))
obstacle2_mask = pygame.mask.from_surface(obstacle2)

obstacle3 = pygame.image.load("Graphics/Items/Obstacle3.png").convert_alpha()
obstacle3_rect = obstacle3.get_rect(center = (1800, 300))
obstaclek3_mask = pygame.mask.from_surface(obstacle3)

coin = pygame.image.load("Graphics/Items/Coin.png").convert_alpha()
coin_rect = coin.get_rect(center = (2000, 300))
coin_mask = pygame.mask.from_surface(coin)

coin_menu = pygame.image.load("Graphics/Menu/Coin.png").convert_alpha()
coin_menu_rect = coin_menu.get_rect(topleft = (685, 345))

background = pygame.image.load("Graphics/Menu/Background.png").convert()
background_rect = background.get_rect(topleft = (0, 0))

default_shop = pygame.image.load("Graphics/Menu/Default.png").convert_alpha()
default_shop_rect = default_shop.get_rect(midleft = (15, 200))

common_shop = pygame.image.load("Graphics/Menu/Common.png").convert_alpha()
common_shop_rect = common_shop.get_rect(midleft = (default_shop_rect.right + 30, 200))
common_prize = normal_font_small.render("10 Coins", True, red)

rare_shop = pygame.image.load("Graphics/Menu/Rare.png").convert_alpha()
rare_shop_rect = common_shop.get_rect(midleft = (common_shop_rect.right + 30, 200))
rare_prize = normal_font_small.render("50 Coins", True, red)

epic_shop = pygame.image.load("Graphics/Menu/Epic.png").convert_alpha()
epic_shop_rect = epic_shop.get_rect(midleft = (rare_shop_rect.right + 30, 200))
epic_prize = normal_font_small.render("100 Coins", True, red)

legendary_shop = pygame.image.load("Graphics/Menu/Legendary.png").convert_alpha()
legendary_shop_rect = legendary_shop.get_rect(midleft = (epic_shop_rect.right + 30, 200))
legendary_prize = normal_font_small.render("500 Coins", True, red)

locked_text = normal_font_small.render("Locked", True, red)

selected = pygame.image.load("Graphics/Menu/Selected.png").convert_alpha()
selected_rect = selected.get_rect(topleft = (default_shop_rect.left + 2, default_shop_rect.top))

selector = pygame.image.load("Graphics/Menu/Selector.png").convert_alpha()

locked = pygame.image.load("Graphics/Menu/Locked.png").convert_alpha()
locked_common_rect = locked.get_rect(topleft = (common_shop_rect.left + 40, common_shop_rect.top + 30))
locked_rare_rect = locked.get_rect(topleft = (rare_shop_rect.left + 40, rare_shop_rect.top + 30))
locked_epic_rect = locked.get_rect(topleft = (epic_shop_rect.left + 40, epic_shop_rect.top + 30))
locked_legendary_rect = locked.get_rect(topleft = (legendary_shop_rect.left + 40, legendary_shop_rect.top + 30))

shop = pygame.image.load("Graphics/Menu/Shop.png").convert_alpha()
shop_rect = shop.get_rect(center = (400, 320))

shop_pressed = pygame.image.load("Graphics/Menu/Shop_Pressed.png").convert_alpha()
shop_pressed_rect = shop_pressed.get_rect(center = (400, 320))

back = pygame.image.load("Graphics/Menu/Back.png").convert_alpha()
back_rect = back.get_rect(topleft = (15, 15))

back_pressed = pygame.image.load("Graphics/Menu/Back_Pressed.png").convert_alpha()
back_pressed_rect = back_pressed.get_rect(topleft = (15, 15))

death_sound = pygame.mixer.Sound("Sounds/Effects/Death.mp3")
coin_sound = pygame.mixer.Sound("Sounds/Effects/Coin.mp3")
button_sound = pygame.mixer.Sound("Sounds/Effects/Button.mp3")

def resetPositions():
    global background_rect, submarine_rect, obstacle1_rect, obstacle2_rect, obstacle3_rect, coin_rect
    background_rect.topleft = (0, 0)
    submarine_rect.center = (100, 250)
    obstacle1_rect.center = (900, 100)
    obstacle2_rect.center = (1400, 200)
    obstacle3_rect.center = (1800, 300)
    coin_rect.center = (2000, 300)

def displayCoins():
    global coins
    coins_text = pixel_font.render(f"x{coins}", True, red)
    coins_text_rect = text.get_rect(topleft = (740, 340))

    if "1" in str(coins):
        coin_menu_rect.x = 695 - len(str(coins)) * 33
        coins_text_rect.x = 750 - len(str(coins)) * 33
    else:
        coin_menu_rect.x = 685 - len(str(coins)) * 33
        coins_text_rect.x = 740 - len(str(coins)) * 33

    screen.blit(coins_text, coins_text_rect)
    screen.blit(coin_menu, coin_menu_rect)

stage = 1
survived_time = 0
death = True
coin_shown = True
coins = int(open("Game_Files/Coins.txt", "r").read())
skin = int(open("Game_Files/Current_Skin.txt", "r").read())
skins_list = ["Default", "Common", "Rare", "Epic", "Legendary"]
skins_available = open("Game_Files/Skins.txt", "r").read()
skins_available_list = []
for x in skins_available:
    skins_available_list.append(x)
default_available = int(skins_available_list[0])
common_available = int(skins_available_list[1])
rare_available = int(skins_available_list[2])
epic_available = int(skins_available_list[3])
legendary_available = int(skins_available_list[4])

while True:    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            open("Game_Files/Current_Skin.txt", "w").write(str(skin))
            open("Game_Files/Highscore.txt").close()
            open("Game_Files/Coins.txt").close()
            open("Game_Files/Skins.txt").close()
            open("Game_Files/Current_Skin.txt").close()
            pygame.quit()
            sys.exit()

    if stage == 1:
        if death == True:
            death = False
            pygame.mixer.music.stop()
            pygame.mixer.music.load(f"Sounds/Music/Lobby.mp3")
            pygame.mixer.music.play(-1)
        
        screen.blit(background, background_rect)
        screen.blit(text, text_rect)
        
        if shop_rect.collidepoint(pygame.mouse.get_pos()):
            screen.blit(shop_pressed, shop_pressed_rect)
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_presses = pygame.mouse.get_pressed()
                if mouse_presses[0]:
                    pygame.mixer.Sound.play(button_sound)
                    background_rect = background.get_rect(topleft = (0, 0))
                    default_shop_rect = default_shop.get_rect(midleft = (15, 200))
                    common_shop_rect = common_shop.get_rect(midleft = (default_shop_rect.right + 30, 200))
                    rare_shop_rect = common_shop.get_rect(midleft = (common_shop_rect.right + 30, 200))
                    epic_shop_rect = epic_shop.get_rect(midleft = (rare_shop_rect.right + 30, 200))
                    legendary_shop_rect = legendary_shop.get_rect(midleft = (epic_shop_rect.right + 30, 200))
                    if skin == 0:
                         selected_rect = selected.get_rect(topleft = (default_shop_rect.left + 2, default_shop_rect.top))
                    elif skin == 1:
                        selected_rect = selected.get_rect(topleft = (common_shop_rect.left + 2, common_shop_rect.top))
                    elif skin == 2:
                        selected_rect = selected.get_rect(topleft = (rare_shop_rect.left + 2, rare_shop_rect.top))
                    elif skin == 3:
                        selected_rect = selected.get_rect(topleft = (epic_shop_rect.left + 2, epic_shop_rect.top))
                    elif skin == 4:
                        selected_rect = selected.get_rect(topleft = (legendary_shop_rect.left + 2, legendary_shop_rect.top))
                    locked_common_rect = locked.get_rect(topleft = (common_shop_rect.left + 40, common_shop_rect.top + 30))
                    locked_rare_rect = locked.get_rect(topleft = (rare_shop_rect.left + 40, rare_shop_rect.top + 30))
                    locked_epic_rect = locked.get_rect(topleft = (epic_shop_rect.left + 40, epic_shop_rect.top + 30))
                    locked_legendary_rect = locked.get_rect(topleft = (legendary_shop_rect.left + 40, legendary_shop_rect.top + 30))
                    stage = 3
        else:
            screen.blit(shop, shop_rect)
        
        current_highscore = open("Game_Files/Highscore.txt", "r").read()
        highscore = normal_font.render(f"Highscore: {current_highscore}", True, white)
        highscore_rect = highscore.get_rect(center = (400, 150))
        
        current_score = normal_font.render(f"Your score: {survived_time}", True, white)
        current_score_rect = current_score.get_rect(center = (400, 220))

        screen.blit(highscore, highscore_rect)
        screen.blit(current_score, current_score_rect)

        displayCoins()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            stage = 2
            tick_nr = 0
            survived_time = 0
            speed = 1
            coin_shown = True
            game_start = True

    if stage == 2:
        if game_start == True:
            game_start = False
            pygame.mixer.music.load(f"Sounds/Music/Game.mp3")
            pygame.mixer.music.play(-1)
            submarine = pygame.image.load(f"Graphics/Player/{skins_list[skin]}.png").convert_alpha()
        
        speed += 0.0003
        movement = 5 * speed

        if tick_nr < 60:
            tick_nr += 1
        else:
            survived_time += 1
            tick_nr = 1

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            submarine_rect.top -= 7
        if keys[pygame.K_DOWN]:
            submarine_rect.bottom += 7

        if ocean_rect.right > 800:
            ocean_rect.left -= movement
        else:
            ocean_rect.topleft = (0, 0)

        if obstacle1_rect.left < -500:
            random_line = randint(1, 400)
            obstacle1_rect.center = (900, random_line)
        if obstacle2_rect.left < -500:
            random_line = randint(1, 400)
            obstacle2_rect.center = (900, random_line)
        if obstacle3_rect.left < -500:
            random_line = randint(1, 400)
            obstacle3_rect.center = (900, random_line)
        if coin_rect.left < -500:
            coin_shown = True
            random_line = randint(1, 400)
            coin_rect.center = (900, random_line)

        obstacle1_rect.left -= movement
        obstacle2_rect.left -= movement
        obstacle3_rect.left -= movement
        coin_rect.left -= movement

        if submarine_rect.top < -50:
            submarine_rect.y += 7
        if submarine_rect.bottom > 450:
            submarine_rect.y -= 7

        submarine_mask = pygame.mask.from_surface(submarine)
        obstacle1_mask = pygame.mask.from_surface(obstacle1)
        obstacle2_mask = pygame.mask.from_surface(obstacle2)
        obstacle3_mask = pygame.mask.from_surface(obstacle3)
        coin_mask = pygame.mask.from_surface(coin)

        screen.blit(ocean, ocean_rect)
        screen.blit(submarine, submarine_rect)
        screen.blit(obstacle1, obstacle1_rect)
        screen.blit(obstacle2, obstacle2_rect)
        screen.blit(obstacle3, obstacle3_rect)

        if coin_shown == True:
            screen.blit(coin, coin_rect)

        displayCoins()

        score_str = str(survived_time)
        score = normal_font.render(score_str, True, black)
        score_rect = score.get_rect(center = (740, 50))

        screen.blit(score, score_rect)

        if submarine_mask.overlap(obstacle1_mask, (obstacle1_rect[0] - submarine_rect.x, obstacle1_rect[1] - submarine_rect.y)) or submarine_mask.overlap(obstacle2_mask, (obstacle2_rect[0] - submarine_rect.x, obstacle2_rect[1] - submarine_rect.y)) or submarine_mask.overlap(obstacle3_mask, (obstacle3_rect[0] - submarine_rect.x, obstacle3_rect[1] - submarine_rect.y)):
            pygame.mixer.Sound.play(death_sound)
            if int(current_highscore) < survived_time:
                open("Game_Files/Highscore.txt", "w").write(str(survived_time))
            open("Game_Files/Coins.txt", "w").write(str(coins))
            coins = int(open("Game_Files/Coins.txt", "r").read())
            resetPositions()
            stage = 1
            death = True

        if coin_mask.overlap(obstacle1_mask, (obstacle1_rect[0] - coin_rect.x, obstacle1_rect[1] - coin_rect.y)) or coin_mask.overlap(obstacle2_mask, (obstacle2_rect[0] - coin_rect.x, obstacle2_rect[1] - coin_rect.y)) or coin_mask.overlap(obstacle3_mask, (obstacle3_rect[0] - coin_rect.x, obstacle3_rect[1] - coin_rect.y)):
            coin_rect.center = (coin_rect.x, 3000)

        if submarine_mask.overlap(coin_mask, (coin_rect[0] - submarine_rect.x, coin_rect[1] - submarine_rect.y)):
            pygame.mixer.Sound.play(coin_sound)
            coin_shown = False
            coin_rect.center = (coin_rect.x, 3000)
            if coins < 999:
                coins += 1

    if stage == 3:
        skins_available = open("Game_Files/Skins.txt", "r").read()
        skins_available_list = []
        for x in skins_available:
            skins_available_list.append(x)
        default_available = int(skins_available_list[0])
        common_available = int(skins_available_list[1])
        rare_available = int(skins_available_list[2])
        epic_available = int(skins_available_list[3])
        legendary_available = int(skins_available_list[4])

        screen.blit(background, background_rect)
        screen.blit(default_shop, default_shop_rect)
        screen.blit(common_shop, common_shop_rect)
        screen.blit(rare_shop, rare_shop_rect)
        screen.blit(epic_shop, epic_shop_rect)
        screen.blit(legendary_shop, legendary_shop_rect)
        screen.blit(selected, selected_rect)
        if common_available == 0:
            screen.blit(locked, locked_common_rect)
        if rare_available == 0:
            screen.blit(locked, locked_rare_rect)
        if epic_available == 0:
            screen.blit(locked, locked_epic_rect)
        if legendary_available == 0:
            screen.blit(locked, locked_legendary_rect)

        displayCoins()

        if back_rect.collidepoint(pygame.mouse.get_pos()):
            screen.blit(back_pressed, back_pressed_rect)
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_presses = pygame.mouse.get_pressed()
                if mouse_presses[0]:
                    pygame.mixer.Sound.play(button_sound)
                    stage = 1
        else:
            screen.blit(back, back_rect)
        
        scroll = "Still"
        if event.type == pygame.MOUSEWHEEL:
            if event.y > 0:
                scroll = "Up"
            elif event.y < 0:
                scroll = "Down"

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT] or scroll == "Down":
            if legendary_shop_rect.right + 30 > 800:
                background_rect.x -= 8
                default_shop_rect.x -= 8
                common_shop_rect.x -= 8
                rare_shop_rect.x -= 8
                epic_shop_rect.x -= 8
                legendary_shop_rect.x -= 8
                selected_rect.x -= 8
                locked_common_rect.x -= 8
                locked_rare_rect.x -= 8
                locked_epic_rect.x -= 8
                locked_legendary_rect.x -= 8
        if keys[pygame.K_LEFT] or scroll == "Up":
            if background_rect.left < 0:
                background_rect.x += 8
                default_shop_rect.x += 8
                common_shop_rect.x += 8
                rare_shop_rect.x += 8
                epic_shop_rect.x += 8
                legendary_shop_rect.x += 8
                selected_rect.x += 8
                locked_common_rect.x += 8
                locked_rare_rect.x += 8
                locked_epic_rect.x += 8
                locked_legendary_rect.x += 8

        if default_shop_rect.collidepoint(pygame.mouse.get_pos()):
            selector_rect = selector.get_rect(topleft = (default_shop_rect.left + 2, default_shop_rect.top))
            screen.blit(selector, selector_rect)
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_presses = pygame.mouse.get_pressed()
                if mouse_presses[0]:
                    if default_available == 1:
                        selected_rect.topleft = (default_shop_rect.left + 2, default_shop_rect.top)
                        skin = 0
        elif common_shop_rect.collidepoint(pygame.mouse.get_pos()):
            selector_rect = selector.get_rect(topleft = (common_shop_rect.left + 2, common_shop_rect.top))
            screen.blit(selector, selector_rect)
            if common_available == 0:
                screen.blit(common_prize, pygame.mouse.get_pos())
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_presses = pygame.mouse.get_pressed()
                    if mouse_presses[0]:
                        if coins >= 10:
                            pygame.mixer.Sound.play(coin_sound)
                            coins -= 10
                            open("Game_Files/Skins.txt", "w").write("11000")
                            open("Game_Files/Coins.txt", "w").write(str(coins))
                            selected_rect.topleft = (common_shop_rect.left + 2, common_shop_rect.top)
                            skin = 1
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_presses = pygame.mouse.get_pressed()
                if mouse_presses[0]:
                    if common_available == 1:
                        selected_rect.topleft = (common_shop_rect.left + 2, common_shop_rect.top)
                        skin = 1
        elif rare_shop_rect.collidepoint(pygame.mouse.get_pos()):
            selector_rect = selector.get_rect(topleft = (rare_shop_rect.left + 2, rare_shop_rect.top))
            screen.blit(selector, selector_rect)
            if rare_available == 0:
                if common_available == 1:
                    screen.blit(rare_prize, pygame.mouse.get_pos())
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_presses = pygame.mouse.get_pressed()
                        if mouse_presses[0]:
                            if coins >= 50:
                                pygame.mixer.Sound.play(coin_sound)
                                coins -= 50
                                open("Game_Files/Skins.txt", "w").write("11100")
                                open("Game_Files/Coins.txt", "w").write(str(coins))
                                selected_rect.topleft = (rare_shop_rect.left + 2, rare_shop_rect.top)
                                skin = 2
                else:
                    screen.blit(locked_text, pygame.mouse.get_pos())
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_presses = pygame.mouse.get_pressed()
                if mouse_presses[0]:
                    if rare_available == 1:
                        selected_rect.topleft = (rare_shop_rect.left + 2, rare_shop_rect.top)
                        skin = 2
        elif epic_shop_rect.collidepoint(pygame.mouse.get_pos()):
            selector_rect = selector.get_rect(topleft = (epic_shop_rect.left + 2, epic_shop_rect.top))
            screen.blit(selector, selector_rect)
            if epic_available == 0:
                if rare_available == 1:
                    screen.blit(epic_prize, pygame.mouse.get_pos())
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_presses = pygame.mouse.get_pressed()
                        if mouse_presses[0]:
                            if coins >= 100:
                                pygame.mixer.Sound.play(coin_sound)
                                coins -= 100
                                open("Game_Files/Skins.txt", "w").write("11110")
                                open("Game_Files/Coins.txt", "w").write(str(coins))
                                selected_rect.topleft = (epic_shop_rect.left + 2, epic_shop_rect.top)
                                skin = 3
                else:
                    screen.blit(locked_text, pygame.mouse.get_pos())
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_presses = pygame.mouse.get_pressed()
                if mouse_presses[0]:
                    if epic_available == 1:
                        selected_rect.topleft = (epic_shop_rect.left + 2, epic_shop_rect.top)
                        skin = 3
        elif legendary_shop_rect.collidepoint(pygame.mouse.get_pos()):
            selector_rect = selector.get_rect(topleft = (legendary_shop_rect.left + 2, legendary_shop_rect.top))
            screen.blit(selector, selector_rect)
            if legendary_available == 0:
                if epic_available == 1:
                    screen.blit(legendary_prize, pygame.mouse.get_pos())
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_presses = pygame.mouse.get_pressed()
                        if mouse_presses[0]:
                            if coins >= 500:
                                pygame.mixer.Sound.play(coin_sound)
                                coins -= 500
                                open("Game_Files/Skins.txt", "w").write("11111")
                                open("Game_Files/Coins.txt", "w").write(str(coins))
                                selected_rect.topleft = (legendary_shop_rect.left + 2, legendary_shop_rect.top)
                                skin = 2
                else:
                    screen.blit(locked_text, pygame.mouse.get_pos())
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_presses = pygame.mouse.get_pressed()
                if mouse_presses[0]:
                    if legendary_available == 1:
                        selected_rect.topleft = (legendary_shop_rect.left + 2, legendary_shop_rect.top)
                        skin = 4

        if death == True:
            death = False
            pygame.mixer.music.stop()
            pygame.mixer.music.load(f"Sounds/Music/Lobby.mp3")
            pygame.mixer.music.play(-1)

    pygame.display.update()
    clock.tick(60)