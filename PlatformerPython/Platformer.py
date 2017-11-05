import math
import random, colorsys
import sys

import pygame   
import spritesheet

joystick = None

# Your code here

level_b6 = [
    "#############################################################################################################",
    "#T                         T                                                                                #",
    "#x                                                                                                          #",
    "######                     ##                                                                               #",
    "#            ########                                                                                       #",
    "#                      ##                                                                                   #",
    "#    ######                ##                                                                               #",
    "#         T     ###                                                                                         #",
    "###                                                                                                         #",
    "#T                  #######                                                                                 #",
    "#        WWWWWW  WW    T                                                                                    #",
    "######  ############                                                                                        #",
    "#                                                                                                           #",
    "#                       #####                                                                               #",
    "#o         ######                                                                                           #",
    "#############################################################################################################",
    ]


level_b5 = [
    "##############################",
    "#                            #",
    "# x                          #",
    "######                       #",
    "#                            #",
    "#T                            #",
    "######                       #",
    "#                            #",
    "#T                           #",
    "######                       #",
    "#                            #",
    "#T                           #",
    "######                       #",
    "#                            #",
    "#T                           #",
    "######                       #",
    "#                            #",
    "#T                           #",
    "######                       #",
    "#                            #",
    "#                            #",
    "######                       #",
    "#                            #",
    "#                            #",
    "######                       #",
    "#                            #",
    "#T                           #",
    "######                       #",
    "#                            #",
    "#                            #",
    "######                       #",
    "#                            #",
    "#                            #",
    "######             o       T #",
    "##############################",
]


level_b4 = [
    "##############################",
    "##############################",
    "##############################",
    "##############################",
    "##############################",
    "#                            #",
    "#                            #",
    "#                            #",
    "#                            #",
    "#            T    T          #",
    "#            ######          #",
    "#                            #",
    "#                            #",
    "#         ##                 #",
    "#o  ##x                     T#",
    "##############################",
    "##############################",
    "##############################",
]



level_list = []
level_list.append(level_b6)
level_list.append(level_b5)
level_list.append(level_b4)


ss = spritesheet.spritesheet('assets/man_idle.png')
ssr = spritesheet.spritesheet('assets/man_moving.png')
ssl = spritesheet.spritesheet('assets/man_moving.png')

ssd = spritesheet.spritesheet('assets/man_ducked.png')




quake = {
    "intensity": 16,
    "offset": [0,0],
    "speed" : 8,
    "do" : False,
    "timeout" : 0,
    "flicker" : False,
    "flickering" : False
}

spee = {
    "speed": 20,
    "offset" : 0,
    "do": False,
    "timer": 0,
    "beenonce": False,
    "shade": True
}

freeze = False

pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.init()

levelMusic = pygame.mixer.Sound("assets/level_music.wav")
menuMusic = pygame.mixer.Sound("assets/loop.wav")



sounds = {
    "bang" : pygame.mixer.Sound("assets/bang.wav"),
    "jump" : pygame.mixer.Sound("assets/jump.wav"),
    "camera": pygame.mixer.Sound("assets/switch.wav"),
    "transition": pygame.mixer.Sound("assets/transition.wav"),
    "shoot": pygame.mixer.Sound("assets/pistolshot01.wav"),
    "failed_shot": pygame.mixer.Sound("assets/failed_shot.wav"),
    "reload": pygame.mixer.Sound("assets/reload.wav"),
    "break": pygame.mixer.Sound("assets/shoot.wav")

}
pygame.mixer.music.set_volume(0.6)

pygame.joystick.init()
# joystick = pygame.joystick.Joystick(0)
# joystick.init()

mute = False

import math

def rot_center(image, angle):
    """rotate an image while keeping its center and size"""
    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image

def magnitude(v):
    return math.sqrt(v[0]*v[0] + v[1]*v[1])

def add(u, v):
    return [ u[i]+v[i] for i in range(len(u)) ]

def sub(u, v):
    return [ u[i]-v[i] for i in range(len(u)) ]

def dot(u, v):
    return sum(u[i]*v[i] for i in range(len(u)))

def normalize(v):
    vmag = magnitude(v)
    return [ v[i]/vmag  for i in range(len(v)) ]

def custom_game_init():
    global title_font
    global level_font
    global player
    global level_list
    global level_exit
    global enemy_images_bee
    global camera_images
    global background_image
    global enemy_images_wheel
    global particles
    global score_font
    global particle_types
    global bullets
    global bullet_image
    global bullet_glow_image
    global ammo, bullet_fire_cooldown, bullet_fire_max_cooldown, camera_dot_images


    camerasheet = spritesheet.spritesheet('assets/camera.png')
    camera_images = [rot_center(camerasheet.image_at((0, 0, 32, 32)), -45),
                     pygame.transform.flip(rot_center(camerasheet.image_at((0, 0, 32, 32)), -45), True, False)]
    camera_dot_images = [rot_center(camerasheet.image_at((0, 32, 32, 32)), -45),
                     pygame.transform.flip(rot_center(camerasheet.image_at((0, 32, 32, 32)), -45), True, False)]

    ammo = 8
    bullet_fire_cooldown = 0
    bullet_fire_max_cooldown = 20

    player = {
        "lives" : 5,
        "xm": 0,
        "images": [
            pygame.image.load("assets/player_left_0.png"),
            pygame.image.load("assets/player_right_0.png"),
            pygame.image.load("assets/player_up_0.png"),
            pygame.image.load("assets/player_down_0.png")
        ],
        "assets": {
            "idle": [ss.image_at((0, 0, 32, 32)),
                     ss.image_at((0, 32, 32, 32)),
                     ss.image_at((0, 64, 32, 32)),
                     ss.image_at((0, 96, 32, 32)),
                     ss.image_at((0, 128, 32, 32)),
                     ss.image_at((0, 160, 32, 32)),
                     ss.image_at((0, 192, 32, 32)),
                     ss.image_at((0, 224, 32, 32)),

                     ss.image_at((0, 192, 32, 32)),
                     ss.image_at((0, 160, 32, 32)),
                     ss.image_at((0, 128, 32, 32)),
                     ss.image_at((0, 96, 32, 32)),
                     ss.image_at((0, 64, 32, 32)),
                     ss.image_at((0, 32, 32, 32))],
            "left": [ pygame.transform.flip(ssl.image_at((0, 0, 32, 32)), True, False),
                      pygame.transform.flip(ssl.image_at((0, 32, 32, 32)), True, False),
                      pygame.transform.flip(ssl.image_at((0, 64, 32, 32)), True, False),
                      pygame.transform.flip(ssl.image_at((0, 96, 32, 32)), True, False),
                      pygame.transform.flip(ssl.image_at((0, 128, 32, 32)), True, False),
                      pygame.transform.flip(ssl.image_at((0, 160, 32, 32)), True, False),
                      pygame.transform.flip(ssl.image_at((0, 192, 32, 32)), True, False),
                      pygame.transform.flip(ssl.image_at((0, 224, 32, 32)), True, False)],
            "right": [ssr.image_at((0, 0, 32, 32)),
                     ssr.image_at((0, 32, 32, 32)),
                     ssr.image_at((0, 64, 32, 32)),
                     ssr.image_at((0, 96, 32, 32)),
                     ssr.image_at((0, 128, 32, 32)),
                     ssr.image_at((0, 160, 32, 32)),
                     ssr.image_at((0, 192, 32, 32)),
                     ssr.image_at((0, 224, 32, 32))],
            "ducked": [ssd.image_at((0, 0, 32, 32)),
                      ssd.image_at((0, 32, 32, 32)),
                      ssd.image_at((0, 64, 32, 32)),
                      ssd.image_at((0, 96, 32, 32)),
                      ssd.image_at((0, 64, 32, 32)),
                      ssd.image_at((0, 32, 32, 32))]

        },
        "rect": pygame.Rect(0, 0, 32, 27),
        "start_rect": pygame.Rect(0, 0, 32, 27),
        "image_index": 0,
        "yv" : 0,
        "inAir": False,
        "jumps": 0,
        "max_jumps": 2,
        "ducked": False,
        "direction": "right",
        "can": {
            "pound":True,
            "shoot":True
        },
        "dash": [0, 0]
    }

    pygame.display.set_icon(player["assets"]["idle"][0])
    pygame.display.set_caption("They're behind everything")

    exit_ss = spritesheet.spritesheet('assets/exit_32.png')

    level_exit = {
        "images": [exit_ss.image_at((0, 0, 32, 32)),
                   exit_ss.image_at((0, 32, 32, 32)),
                   exit_ss.image_at((0, 64, 32, 32)),
                   exit_ss.image_at((0, 96, 32, 32)),
                   exit_ss.image_at((0, 128, 32, 32)),
                   exit_ss.image_at((0, 160, 32, 32)),
                   exit_ss.image_at((0, 192, 32, 32)),
                   exit_ss.image_at((0, 224, 32, 32)),
                   ],
        "rect": pygame.Rect(0, 0, 32, 32)
    }

    background_image = pygame.image.load("assets/background.png")
    bullet_image = pygame.image.load("assets/bullet.png")

    bullet_glow_image = pygame.image.load("assets/bullet_glow.png")
    colorkey = bullet_glow_image.get_at((0, 0))
    bullet_glow_image.set_colorkey(colorkey)

    particle_types = {
        "wall" : pygame.image.load("assets/particle.png"),
        "slime": pygame.image.load("assets/slime.png"),
        "dark": pygame.image.load("assets/dark.png"),
        "blue": pygame.image.load("assets/blue.png"),
        "red": pygame.image.load("assets/red.png"),

    }


    enemy_images_bee = []
    enemy_images_bee.append(pygame.transform.flip(pygame.image.load("assets/enemy_right_32_0.png"), True, False))
    enemy_images_bee.append(pygame.transform.flip(pygame.image.load("assets/enemy_right_32_1.png"), True, False))
    enemy_images_bee.append(pygame.image.load("assets/enemy_right_32_0.png"))
    enemy_images_bee.append(pygame.image.load("assets/enemy_right_32_1.png"))
    enemy_images_bee.append(pygame.image.load("assets/eyes.png"))
    enemy_images_bee.append(pygame.transform.flip(pygame.image.load("assets/eyes.png"), True, False))



    wheel = spritesheet.spritesheet("assets/wheel.png")
    enemy_images_wheel = []
    enemy_images_wheel.append(wheel.image_at((0, 0, 32, 32)))
    enemy_images_wheel.append(wheel.image_at((0, 32, 32, 32)))
    enemy_images_wheel.append(wheel.image_at((0, 0, 32, 32)))
    enemy_images_wheel.append(wheel.image_at((0, 32, 32, 32)))

    particles = []
    bullets = []

    # camera_image = pygame.image.load("camera_32.png")

    title_font = pygame.font.SysFont("jokerman", 50)
    level_font = pygame.font.SysFont("ariel", 32)
    score_font = pygame.font.SysFont("ariel", 16)


    add_game_state("start", "update_game_start", "draw_game_start")
    add_game_state("running", "update_game_running", "draw_game_running")
    set_game_state("start")




    return

def draw_particles(surface):
    for i in range(len(particles) - 1, -1, -1):
        particle = particles[i]
        image = particle["image"].copy()
        # this works on images with per pixel alpha too
        alpha = particle["life"] * 255
        if alpha > 255:
            alpha = 255
        if alpha < 0:
            alpha = 0
        image.fill((255, 255, 255, alpha), None, pygame.BLEND_RGBA_MULT)
        # particle["image"].set_alpha()

        surface.blit(image, (particle["pos"][0] - mapX, particle["pos"][1] -mapY ))


        if particle["gravity"]:
            rect = pygame.Rect(particle["pos"][0], particle["pos"][1], 4, 4)
            if rect.collidelist(wall_list) == -1:
                particle["pos"][0] += particle["velocity"][0]
                particle["pos"][1] += particle["velocity"][1]
            particle["velocity"][1] += 1

        else:
            particle["pos"][0] += particle["velocity"][0]
            particle["pos"][1] += particle["velocity"][1]

        if particle["life"] > 0:
            particle["life"] -= 1
        else:
            del particles[i]

def create_explosion(rect):
    for i in range(0, random.randint(80, 160)):
        pos = rect.move(0, 0)
        pos[0] += random.randint(0, 32)
        pos[1] += random.randint(0, 32)
        add_particle(pos, "wall", [random.randint(-4, 4), random.randint(-4, 4)], random.randint(10, 40), True)

def create_slime_explosion(rect):
    for i in range(0, random.randint(60, 120)):
        pos = rect.move(0, 0)
        pos[0] += random.randint(0, 32)
        pos[1] += random.randint(0, 32)
        add_particle(pos, "red", [random.randint(-8, 8), random.randint(-8, 8)], random.randint(20, 100), True)
def create_blue_explosion(rect):
    for i in range(0, random.randint(60, 120)):
        pos = rect.move(0, 0)
        pos[0] += random.randint(0, 32)
        pos[1] += random.randint(0, 32)
        add_particle(pos, "blue", [random.randint(-8, 8), random.randint(-8, 8)], random.randint(20, 100), True)

def create_red_explosion(rect):
    for i in range(0, random.randint(10, 20)):
        pos = rect.move(0, 0)
        # pos[0] += random.randint(0, 32)
        # pos[1] += random.randint(16, 48)
        add_particle(pos, "red", [random.randint(-12, 12), random.randint(-2, 12)], random.randint(20, 100), True)

def shoot_bullet(pos, dir):
    global bullet_fire_cooldown, bullet_fire_max_cooldown, ammo
    bullet_fire_cooldown = bullet_fire_max_cooldown
    sounds["shoot"].play()
    ammo -= 1
    global bullets, particle_types, bullet_image
    speed = 8
    m = float(magnitude(dir))
    dir[0] = (dir[0] / m) * speed
    dir[1] = (dir[1] / m) * speed

    bullet = {
        "rect": pygame.Rect(pos[0], pos[1], 8, 8),
        "image": bullet_image,
        "velocity": dir
    }
    bullets.append(bullet)

def draw_and_update_bullets(surface):
    global bullets, wall_list, enemy_list, mapX
    rects = []
    for enemy in enemy_list:
        rects.append(enemy['rect'])

    for i in range(len(bullets) - 1, -1, -1):
        bullet = bullets[i]


        surface.blit(bullet["image"], bullet["rect"].move(-mapX, -mapY))
        times = int(abs(bullet["velocity"][0]))
        for a in range(0, int(abs(bullet["velocity"][0])) + int(abs(bullet["velocity"][1]))):
            if a > times:
                bullet_move_rect = bullet["rect"].move(0, bullet["velocity"][1])
            else:
                bullet_move_rect = bullet["rect"].move(bullet["velocity"][0], 0)


            # surface.blit(bullet["image"], bullet["rect"].move(-mapX, 0))
            if bullet_move_rect.collidelist(wall_list) == -1:
                bullet["rect"] = bullet_move_rect
            else:
                create_red_explosion(bullets[i]["rect"])

                del bullets[i]
                break

            e = bullet_move_rect.collidelist(rects)
            if  e != -1:
                create_explosion(bullet["rect"])
                create_red_explosion(bullets[i]["rect"])
                del enemy_list[e]
                del bullets[i]

                add_score(100, bullet["rect"])
                break
            brk = False
            for camera in camera_list:
                if not camera['active']:
                    if bullet['rect'].colliderect(camera['rect']):
                        add_score(500, camera['rect'].move(0, 0))
                        camera['image'] = camera_images[1]
                        camera['active'] = True
                        sounds["break"].play()
                        create_explosion(camera["rect"])
                        win = True
                        for camera in camera_list:
                            if not camera['active']:
                                win = False
                                break
                        if win:
                            quake["timeout"] = 20
                            sounds["bang"].play()
                            create_explosion(level_exit["rect"])
                        del bullets[i]
                        brk = True
            if brk:
                break




def add_score(amount, pos):
    global particles
    global score
    score += amount
    pos[0] += 32

    text = {
        "pos" : pos,
        "image" : score_font.render(str(amount), 1, (255, 255, 255)),
        "life": 20,
        "velocity": (0, -2),
        "gravity": False

    }
    # particles.append(text)

def add_particle(pos, type, velocity=[0,0], life=20, gravity=False):
    global particles
    global grey_particle
    particle = {
        "pos" : pos,
        "image" : particle_types[type],
        "life": life,
        "velocity": velocity,
        "gravity": gravity
    }
    particles.append(particle)

ACCELERATION = -2
JUMP_FORCE = 18
TERMINAL_VELOCITY = 32

def update_game_running():
    global keys
    global last_keys

    global player
    global enemy_list
    global camera_list
    global score
    global mute
    global level_exit
    global freeze
    global camera_images
    global key_taps, key_times, bullet_fire_cooldown, ammo
    bullet_fire_cooldown -= 1
    if bullet_fire_cooldown == int(bullet_fire_max_cooldown / 2):
        sounds["reload"].play()

    if keys[pygame.K_m] and not last_keys[pygame.K_m]:
        mute = not mute
        if mute:
            pygame.mixer.music.set_volume(0)
        else:
            pygame.mixer.music.set_volume(0.5)

    if not freeze:
        if keys[pygame.K_LSHIFT]:
            move_step = 12

        else:
            move_step = 6
            player["max_jumps"] = 2

        enemy_move_step = 4

        player["inAir"] = check_and_move_player(3, 0, -player["yv"]) or  player["yv"] == 0


        if player["yv"] > -TERMINAL_VELOCITY:
            player["yv"] += ACCELERATION
        if not player["inAir"]:
            player["yv"] = 0


        # Read the keyboard input and move the marker

        if keys[pygame.K_s]:
            player["ducked"] = True
            if player["can"]["pound"]:
                if not last_keys[pygame.K_s] and player["inAir"]:
                    quake["timeout"] = 10
                    sounds["bang"].play()

        else:
            player["ducked"] = False

        if MOUSEDOWN and not LAST_MOUSEDOWN:
            if ammo > 0:
                if bullet_fire_cooldown < 0:
                    mp = mouse_pos
                    mp[0] += mapX
                    mp[1] += mapY
                    v = [mp[0] - player["rect"][0], mp[1] - player["rect"][1]]

                    # v = normalize(v)

                    shoot_bullet((player['rect'][0] + 16, player['rect'][1] + 3), v)
            else:
                sounds["failed_shot"].play()

        if keys[pygame.K_r] and not last_keys[pygame.K_r] and ammo == 0:
            ammo = 8
            sounds["reload"].play()


        if not player["ducked"]:
            if keys[pygame.K_d]:
                if key_taps[pygame.K_d] >= 1:
                    player["dash"][0] = 16



                check_and_move_player(1, move_step + player["dash"][0], 0)
                player["direction"] = "right"
            elif keys[pygame.K_a]:
                if key_taps[pygame.K_a] >= 1:
                    player["dash"][0] = -16

                check_and_move_player(0, -move_step + player["dash"][0], 0)
                player["direction"] = "left"



            if not check_and_move_player(3, 0, -player["yv"]):
                player["jumps"] = 0

            if player["jumps"] < player["max_jumps"] and keys[pygame.K_w] and not last_keys[pygame.K_w]:
                player["yv"] = JUMP_FORCE

                player["jumps"] += 1

                for i in range(0, random.randint(40, 80)):
                    pos = player["rect"].move(0,0)
                    pos[0] += 16 + random.randint(-4, 4)
                    pos[1] += 32
                    add_particle(pos, "wall", [int(random.randint(-32, 32) / 8), int(random.randint(-32, 32) / 8)], random.randint(40, 80), True)

                sounds["jump"].play()

        else:
            if player["inAir"]:
                if player["can"]["pound"]:
                    for i in range(0, 10):
                        check_and_move_player(3, 0, 5)
                        player["yv"] = -20







        check_and_move_enemies(enemy_move_step)

        # Check if we have reached the exit or hit enemy
        if player['rect'].colliderect(level_exit['rect']):
            win = True
            for camera in camera_list:
                if not camera['active']:
                    win = False
                    break
            if win:
                ammo = 8
                score += 1000
                spee["do"] = True
                freeze = True
                sounds["transition"].play()

        # for enemy in enemy_list:
        #     if player['rect'].colliderect(enemy['rect']):
        #         set_game_state("start")



    return
mapX = 0


mapScrollX = {
    "direction": 0,
    "current_speed": 0,
    "speed": 8,
    "acceleration": 1,
    #the percentage of the screen to start scrolling at
    "percent_of_screen": 40,
}

mapY = 0


mapScrollY = {
    "direction": 0,
    "current_speed": 0,
    "speed": 16,
    "acceleration": 8,
    #the percentage of the screen to start scrolling at
    "percent_of_screen": 30,
}


def draw_game_running():
    global game_surface
    global map_surface
    global level_exit
    global enemy_list
    global level_index
    global score_font

    global score
    global keys
    global clock, mapX, mapY, ammo


    levelWidth = len(level_list[level_index][0]) * 32

    levelHeight = len(level_list[level_index]) * 32
    halfScreen = screen.get_width() / 2

    map_area = pygame.Rect(0, 0, 0, 0)
    map_area.unionall_ip(wall_list)
    game_surface.blit(background_image, (0, 0))
    map_surface.set_colorkey( (0,0,0), pygame.RLEACCEL )

    for camera in camera_list:
        pygame.draw.rect(game_surface, (30, 30, 30), (camera['rect'][0] + 12 - mapX, camera['rect'][1] - 8 - mapY, 12, 24))
        if not camera['active']:
            if camera['rect'][0] > player['rect'][0]:
                game_surface.blit(camera_images[1], camera['rect'].move(-mapX, -mapY))
            else:
                game_surface.blit(camera_images[0], camera['rect'].move(-mapX, -mapY))

    game_surface.blit(map_surface, (-mapX, -mapY))


        # if camera['active']:
        #     game_surface.blit(camera_images[0], camera['rect'])
        # elif not ['active']:
        #     game_surface.blit(camera_images[1], camera['rect'])
    draw_particles(game_surface)
    # pygame.display.set_icon(player["assets"]["right"][int(alpha / 2) % len(player["assets"]["right"])])
    for enemy in enemy_list:
        enemy_frame = enemy['rect'].centerx//8 % 2
        if enemy['direction'][0] > 0:
            enemy_frame_start = 2
        else:
            enemy_frame_start = 0
        game_surface.blit(enemy['images'][enemy_frame_start + enemy_frame], enemy['rect'].move(-mapX, -mapY))
    if keys[pygame.K_a]:

        game_surface.blit(player["assets"]["left"][int(alpha / 2) % len(player["assets"]["left"])], (player['rect'][0] - mapX, player["rect"][1] + 1 - mapY))
    elif keys[pygame.K_d]:
        game_surface.blit(player["assets"]["right"][int(alpha / 2) % len(player["assets"]["right"])], (player['rect'][0] - mapX, player["rect"][1] + 1 - mapY))

    else:
        if player["ducked"]:
            game_surface.blit(player["assets"]["ducked"][int(alpha / 2) % len(player["assets"]["ducked"])], (player['rect'][0]- mapX, player["rect"][1] + 1 - mapY))
        else:
            game_surface.blit(player["assets"]["idle"][int(alpha / 2) % len(player["assets"]["idle"])], (player['rect'][0]- mapX, player["rect"][1] + 1 - mapY))
    win = True
    for camera in camera_list:
        if not camera['active']:
            win = False
            break
    if win:
        game_surface.blit(level_exit['images'][int(alpha / 4) % len(player["images"])], level_exit['rect'].move(-mapX, -mapY))
        # for i in range(0, random.randint(8, 400)):
        #     pos = level_exit['rect'].move(0,0)
        #     pos[0] += random.randint(4, 26)
        #     pos[1] += random.randint(0, 30)
        #     add_particle(pos, "blue", [0, -32], 20, False)
        if alpha % 4 == 0:
            create_blue_explosion(level_exit['rect'])


    draw_and_update_bullets(game_surface)

    if quake["do"] or quake["timeout"] > 0:
        for wall in wall_list:
            if alpha % 10 == 0:
                pos = [wall[0],wall[1]]
                pos[0] += random.randint(0,32)
                pos[1] += random.randint(30,34)
                add_particle(pos, "wall", [random.randint(-4, 4), 4], random.randint(10, 30), True)

    level_name = str(level_index - 6)
    level_name = level_name.replace("-", "B")

    level_text = level_font.render(level_name, 1, (255, 255, 255))

    bullet_text = level_font.render(str(ammo), 1, (255, 255, 255))
    hud_surface.blit(bullet_text, (4, 4))

    score_string = str(score)
    for i in range(0, 10 - len(score_string)):
        score_string = "0" + score_string
    rendered_text = level_font.render("Lives: " + str(player["lives"]) + "  Score: " + score_string, 1, (255, 255, 255))

    position = rendered_text.get_rect()
    position.midbottom = game_surface.get_rect().midbottom

    fps = score_font.render("fps: " + str(int(clock.get_fps())) + " p=" + str(len(particles))+ " e=" + str(len(enemy_list)), 1, (255, 255, 255))
    hud_surface.blit(fps, (4, 490))
    # hud_surface.blit(rendered_text, position)


    if mapScrollX["current_speed"] > mapScrollX["direction"]:
        mapScrollX["current_speed"] -= mapScrollX["acceleration"]
    elif mapScrollX["current_speed"] < mapScrollX["direction"]:
        mapScrollX["current_speed"] += mapScrollX["acceleration"]
    mapX += mapScrollX["current_speed"]

    if mapScrollY["current_speed"] > mapScrollY["direction"]:
        mapScrollY["current_speed"] -= mapScrollY["acceleration"]
    elif mapScrollY["current_speed"] < mapScrollY["direction"]:
        mapScrollY["current_speed"] += mapScrollY["acceleration"]
    mapY += mapScrollY["current_speed"]

    if player['rect'].x - mapX > (1 - mapScrollX["percent_of_screen"] / 100) * screen.get_width():
        mapScrollX["direction"] = mapScrollX["speed"]
    elif player['rect'].x - mapX < (mapScrollX["percent_of_screen"] / 100) * screen.get_width():
        mapScrollX["direction"] = -mapScrollX["speed"]
    else:
        mapScrollX["direction"] = 0

    if mapX < 0:
        mapX = 0
    elif mapX > levelWidth - screen.get_width():
        mapX = levelWidth - screen.get_width()

    if player['rect'].y - mapY > (1 - mapScrollY["percent_of_screen"] / 100) * screen.get_height():
        mapScrollY["direction"] = mapScrollY["speed"]
    elif player['rect'].y - mapY < (mapScrollY["percent_of_screen"] / 100) * screen.get_height():
        mapScrollY["direction"] = -mapScrollY["speed"]
    else:
        mapScrollY["direction"] = 0

    if mapY < 0:
        mapY = 0
    elif mapY > levelHeight - screen.get_height():
        mapY = levelHeight - screen.get_height()


    return

def update_game_start():
    global keys, levelMusic
    if keys[pygame.K_SPACE]:
        custom_game_reset()
        player["lives"] = 5
        set_game_state("running")
        pygame.mixer.stop()
        levelMusic.play(-1)

    return

def draw_game_start():
    global title_font
    global game_surface
    global score

    rendered_text = title_font.render("Press Space to Start", 1, (255, 255, 255))
    shadow_text = title_font.render("Press Space to Start", 1, (0, 0, 0))

    position = rendered_text.get_rect()
    position.center = game_surface.get_rect().center
    game_surface.blit(shadow_text, position.move((5, 5)))
    game_surface.blit(rendered_text, position)

    score_text = title_font.render("Last Score: " + str(score), 1, (255, 255, 255))
    score_position = score_text.get_rect()
    score_position.midtop = position.midbottom
    game_surface.blit(score_text, score_position)
    return

def create_map(level_data, block_size):
    """
    Populates wall, enemy, player & exit data
    with rectangles of block_size.
    using the symbols in the level data
    """
    global player
    global wall_list
    global level_exit
    global enemy_list
    global camera_list

    wall_list = []
    enemy_list = []
    camera_list = []

    # Reset the wall & enemy lists
    wall_list[:] = []
    enemy_list[:] = []
    camera_list[:] = []

    # Fill the walls array with rectangles for each '#'
    x = y = 0
    for row in level_data:
        for col in row:
            if col == " ":
                x += block_size
                continue

            elif col == "#":
                wall_list.append(pygame.Rect(x, y, block_size, block_size))

            # Set the player position if we find an 'o'
            elif col == "o":
                player["rect"] = pygame.Rect(x, y, block_size, block_size)
                player["start_rect"] = pygame.Rect(x, y, block_size, block_size)

            # Set the exit position if we find an 'x'
            elif col == "x":
                level_exit["rect"] = pygame.Rect(x, y, block_size, block_size)

            # Set the enemy position if we find an 'E'
            elif col == "B":
                add_enemy(x, y, 6, "bee")
            elif col == "W":
                add_enemy(x, y, 4, "wheel")

            # Set the camera position if we find an 'T'
            elif col == "T":
                add_camera(x, y, 10)

            x += block_size
        y += block_size
        x = 0

    return wall_list

def create_map_surface(wall_list):
    """
    Creates a map surface image using
    the passed list of rectangles which
    represent the location of walls.
    """
    global background_image, mapX

    # Find the size of the image
    # required by merging all the rectangles
    # in the list
    wall_middle_sprite = pygame.image.load("assets/wall_32.png")
    wall_left_sprite = pygame.image.load("assets/wall_left_32.png")
    wall_right_sprite = pygame.image.load("assets/wall_right_32.png")
    map_area = pygame.Rect(0, 0, 0, 0)
    map_area.unionall_ip(wall_list)

    # create the image
    map_surface = pygame.Surface((map_area.width, map_area.height))

    # map_surface.blit(background_image, (-mapX, 0))

    rgb = colorsys.hsv_to_rgb((alpha % 100) / 100, 1.0, 1.0)
    game_surface.fill((0,0,0))
    # blit the walls in
    for wall in wall_list:
        right_rect = wall.move(32, 0)
        left_rect = wall.move(-32, 0)

        if wall.right == map_area.right or wall.left == map_area.left:
            wall_sprite = wall_middle_sprite
        elif right_rect.collidelist(wall_list) == -1:
            wall_sprite = wall_right_sprite
        elif left_rect.collidelist(wall_list) == -1:
            wall_sprite = wall_left_sprite
        else:
            wall_sprite = wall_middle_sprite
        if right_rect.collidelist(wall_list) == -1 and left_rect.collidelist(wall_list) == -1:
            wall_sprite = wall_middle_sprite



        map_surface.blit(wall_sprite, wall)

    # return the image surface
    return map_surface

def add_camera(x, y, value):
    """
    Create a new enemy data dictionary
    Add it to the enemy list
    """
    global camera_list
    global camera_images

    camera = {
        "image": camera_images[0],
        "rect": pygame.Rect(x, y, 32, 32),
        "active": False,
        "value": value,
        "alpha": random.randint(20, 100)
    }
    camera_list.append(camera)

def add_enemy(x, y, move_step, type):
    """
    Create a new enemy data dictionary
    Add it to the enemy list
    """
    global enemy_list
    global enemy_images_bee
    global enemy_images_wheel



    if (type == "wheel"):
        enemy = {
            "images": enemy_images_wheel,
            "rect": pygame.Rect(x, y, 32, 32),
            "start_rect": pygame.Rect(x, y, 32, 32),
            "direction": [move_step, 0],
            "type": "wheel",
            "light": False
        }
        enemy_list.append(enemy)
        return
    enemy = {
        "images": enemy_images_bee,
        "rect": pygame.Rect(x, y, 32, 20),
        "start_rect": pygame.Rect(x, y, 32, 20),
        "direction": [move_step, 0],
        "type": "bee",
        "light": False
    }
    enemy_list.append(enemy)

def load_next_level():
    """
    Parses the level list (with wrap around)
    to create new map objects & map image surface
    """
    global wall_list
    global particles
    global bullets
    global wall_list

    global map_surface
    global level_index
    global level_list

    particles[:] = []
    bullets[:] = []

    level_index += 1
    if level_index == len(level_list):
        level_index = 0

    wall_list = create_map(level_list[level_index], 32)
    map_surface = create_map_surface(wall_list)
    return

def restart_level():
    """
    Parses the level list (with wrap around)
    to create new map objects & map image surface
    """
    global wall_list
    global particles
    global bullets
    global wall_list

    global map_surface
    global level_index
    global level_list
    global menuMusic, ammo

    # player["lives"] -= 1
    ammo = 8
    bullet_fire_cooldown = bullet_fire_max_cooldown
    if player["lives"] < 1:
        set_game_state("start")
        pygame.mixer.music.stop()
        menuMusic.play(-1)

    bullets[:] = []

    quake["timeout"] = 20
    wall_list = create_map(level_list[level_index], 32)
    map_surface = create_map_surface(wall_list)
    return

def custom_game_reset():
    """
    Initialise the game state
    """
    global enemy_list
    global player
    global score
    global level_index

    score = 0
    level_index = -1
    load_next_level()

    for enemy in enemy_list:
        enemy['rect'] = enemy['start_rect']

    player['rect'] = player['start_rect']

    return

def check_and_move_player(image_index, move_x, move_y):
    """
    Checks a requested move
    and only updates the player data if
    the move does not collide
    """
    global player
    global wall_list

    # Copy the player rectangle and move it in the direction
    # requested

    player_move_rect = player['rect']
    player_move_rect = player_move_rect.move(move_x, move_y)

    # If it *doesn't* collide with a wall, update the player
    # rectangle and player direction
    if player_move_rect.collidelist(wall_list) == -1:

        player['rect'] = player_move_rect
        player["image_index"] = image_index
        return True

    return False

def check_and_move_enemies(move_step):
    """
    Moves each enemy & change direction
    randomly if there is an obstacle'.
    Only updates the enemies data if
    the move does not collide
    """
    global wall_list
    global enemy_list
    global alpha
    global score

    for i in range(len(enemy_list) - 1, -1, -1):
        enemy = enemy_list[i]
        enemy_vector = enemy['direction']

        # update the enemy move rectangle according to direction vector & speed


        # If the enemy has hit a wall, generate a new direction
        if enemy["type"] == "bee":
            enemy_move_rect = enemy['rect'].move(enemy_vector[0], enemy_vector[1])
            if enemy_move_rect.collidelist(wall_list) != -1 or random.randint(0, 60) == alpha % 60:
                random_direction = random.randint(0, 3)
                if random_direction == 0:
                    enemy['direction'] = [0, move_step]  # down
                elif random_direction == 1:
                    enemy['direction'] = [0, -move_step]  # up
                elif random_direction == 2:
                    enemy['direction'] = [move_step, 0]  # right
                elif random_direction == 3:
                    enemy['direction'] = [-move_step, 0]  # left
            else:
                enemy['rect'] = enemy_move_rect
        elif enemy["type"] == "wheel":
            enemy_move_rect_right = enemy['rect'].move(16, 48)
            enemy_move_rect_left = enemy['rect'].move(-16, 48)
            if enemy_move_rect_right.collidelist(wall_list) == -1 or enemy_move_rect_left.collidelist(wall_list) == -1:
                rect_bl = enemy['rect'].move(-16, 48)
                rect_br = enemy['rect'].move(16, 48)

                if rect_bl.collidelist(wall_list) != -1:
                    enemy['direction'] = [-abs(enemy_vector[0]), 0]
                elif rect_br.collidelist(wall_list) != -1:
                    enemy['direction'] = [abs(enemy_vector[0]), 0]

            enemy_move_rect = enemy['rect'].move(enemy_vector[0], 0)
            if enemy_move_rect.collidelist(wall_list) != -1:
                enemy['direction'] = [-enemy_vector[0], 0]
            else:
                enemy['rect'] = enemy_move_rect
        if enemy["rect"].colliderect(player["rect"]):
            if player["ducked"] and player["yv"] < -10:

                del enemy_list[i]
                add_score(100, enemy["rect"])
                create_explosion(enemy["rect"])
                return
            else:
                create_slime_explosion(player["rect"])
                restart_level()

                quake["timeout"] = 10
                sounds["bang"].play()
                return

    return


####################################################
#   Game 'Engine'
#   -----------
#
#   Reusable code for lots of basic games
#
#   YOU DON'T NEED TO CHANGE ANYTHING AFTER HERE
#
####################################################


def game_init():
    """
    Perform global initialisation
    """
    global game_surface
    global clock
    global joystick
    global keys, last_keys
    global game_state_dict
    global current_game_state, hud_surface
    global screen, key_times, key_taps

    # Initialise pygame
    pygame.init()

    # game_surface
    game_surface = pygame.Surface((960, 510))
    hud_surface = pygame.Surface((960, 510))
    screen = pygame.display.set_mode((960, 510))
    #screen = pygame.display.set_mode((2560, 1600), pygame.FULLSCREEN |pygame.HWSURFACE | pygame.DOUBLEBUF)
    keys = []
    key_times = []
    key_taps = []
    i = 0
    for key in pygame.key.get_pressed():
        keys.append(key)
        i += 1



    if not joystick is None:
        keys[pygame.K_a] = keys[pygame.K_a] or joystick.get_axis(0) > 0
        keys[pygame.K_d] = keys[pygame.K_d] or joystick.get_axis(0) < 0
        keys[pygame.K_w] = keys[pygame.K_w] or joystick.get_axis(1) < 0
        keys[pygame.K_s] = keys[pygame.K_s] or joystick.get_axis(1) > 0

    last_keys = keys


    # Clock is used to regulate game speed
    clock = pygame.time.Clock()

    game_state_dict = {}
    current_game_state = {}

    if "custom_game_init" in globals():
        custom_game_init()

    return game_run()


def game_run():
    """
    The main gameloop cycle
    """

    if "custom_game_reset" in globals():
        custom_game_reset()

    while True:
        pygame.mouse.set_cursor(*pygame.cursors.broken_x)
        game_input()
        game_update()
        game_draw()
    return

mouse_pos = [0, 0]
LAST_MOUSEDOWN = False
MOUSEDOWN = False
def game_input():
    """
    Fill the keys list with the
    currently pressed keys
    and check for quit
    """
    global keys, keys_times, key_taps
    global last_keys
    global mouse_pos
    global MOUSEDOWN, LAST_MOUSEDOWN

    last_keys = keys
    keys = pygame.key.get_pressed()

    key_index = 0
    for key in keys:
        if len(key_times) > key_index:
            if keys[key_index]:
                key_times[key_index] = key_times[key_index] + 1
            else:
                key_times[key_index] = -1
        else:
            key_times.append(-1)
        key_index += 1

    key_index = 0
    for key in keys:
        if len(key_taps) > key_index:
            if not keys[key_index] and last_keys[key_index]:
                if (key_times[key_index] < 10):
                    key_taps[key_index] = key_taps[key_index] + 1
                else:
                    key_taps[key_index] = 0
            if key_times[key_index] < 10 and key_times[key_index] > -1:
                key_taps[key_index] = 0

        else:
            key_taps.append(-1)
        key_index += 1


    if keys[pygame.K_ESCAPE]:
        pygame.quit()
        sys.exit()

    LAST_MOUSEDOWN = MOUSEDOWN

    # print(str(MOUSEDOWN))
    mouse_pos[0] = pygame.mouse.get_pos()[0]
    mouse_pos[1] = pygame.mouse.get_pos()[1]
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONUP:
            MOUSEDOWN = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            MOUSEDOWN = True
    return


def add_game_state(name, update_function_name, draw_function_name):
    """
    Create a new gamestate data entry dictionary
    Add it to the gamestate dictionary using the
    gamestate name as key
    """
    global game_state_dict

    if update_function_name in globals() and draw_function_name in globals():
        game_state = {
            "update_function": update_function_name,
            "draw_function": draw_function_name
        }
        game_state_dict[name] = game_state
        return True
    else:
        print("game state functions do not exist.")
        return False


def set_game_state(state_name):
    """
    Sets the global current_game_state by name
    Return True if successful
    """
    global game_state_dict
    global current_game_state

    if state_name in game_state_dict:
        current_game_state = game_state_dict[state_name]
        return True
    else:
        print("The state name requested could not be found.")
        return False


def game_update():
    """
    Update the game data
    by calling the current game state's
    update function
    """
    global game_state_dict
    global current_game_state

    if current_game_state:
        globals()[current_game_state["update_function"]]()

    return

alpha = 0

vignette1 = pygame.image.load("assets/vignette1.png")
colorkey = vignette1.get_at((128, 128))
vignette1.set_colorkey(colorkey)

vignette2 = pygame.image.load("assets/vignette2.png")
colorkey = vignette2.get_at((128, 128))
vignette2.set_colorkey(colorkey)

vignette3 = pygame.image.load("assets/vignette3.png")
colorkey = vignette3.get_at((128, 128))
vignette3.set_colorkey(colorkey)

vignette_amin = [vignette1, vignette2, vignette3, vignette2]

def game_draw():

    """
    Draw to the game_surface
    by calling the current game state's
    draw function
    """
    global game_surface
    global clock
    global game_state_dict
    global current_game_state
    global alpha
    global screen
    global quake
    global freeze
    global level_index, hud_surface

    alpha+=1
    # Clear the game_surface
    game_surface.fill((103, 103, 103))
    hud_surface.fill((0, 0, 0))
    # spee["shade"] = True


    if quake["do"]:
        quake["offset"][0] = math.sin(alpha * quake["speed"]) * quake["intensity"]
        quake["offset"][1] = math.cos(alpha * quake["speed"]) * quake["intensity"]
    else:
        if quake["timeout"] > 0:
            quake["offset"][0] = math.sin(alpha * quake["speed"]) * quake["timeout"]
            quake["offset"][1] = math.cos(alpha * quake["speed"]) * quake["timeout"]
            quake["timeout"] -= 1
        else:
            quake["offset"][0] = 0
            quake["offset"][1] = 0

    if current_game_state:
        globals()[current_game_state["draw_function"]]()

    # Update the display to the game_surface
    for i in range(0, 10) :
        if spee["do"]:
            spee["timer"] += 1
            spee["offset"] += spee["speed"]
            if spee["offset"] > 520:
                spee["offset"] = -520
                spee["beenonce"] = True
                load_next_level()
            elif spee["beenonce"] and spee["offset"] >= 0:
                spee["do"] = False
                freeze = False


        else:
            spee["timer"] = 0
            spee["offset"] = 0

            spee["beenonce"] = False



    screen.fill((0, 0, 0))
    if quake["flicker"]:
        if quake["do"] or quake["timeout"] > 0:
            quake["flickering"] = True
            print("!!!")
        else:
            quake["flickering"] = False
            print("...")
        if quake["flickering"]:
            if int(alpha)% 5 == 0:
                spee["shade"] = False
            else:
                spee["shade"] = True
        else:
            spee["shade"] = True

    if spee["shade"] and current_game_state != game_state_dict["start"]:

        vignette_number = int(alpha / 5 % len(vignette_amin))

        rect = pygame.Rect(player["rect"][0] - (48 + 64) - mapX, player["rect"][1] - (48 + 64) - mapY, 256, 256)
        # rect = rect.clamp(pygame.Rect(0, 0, game_surface.get_width(), game_surface.get_height()))

        # rect.inflate_ip(0, 0)

        doOnOpposite = [False, False]

        if rect.x < 0:
            m = rect.width + rect.x
            rect[2] = m
            rect[0] = 0
            doOnOpposite[0] = True
        rect.normalize()
        if rect.y < 0:
            m = rect.height + rect.y
            rect[3] = m
            rect[1] = 0
            doOnOpposite[1] = True
        rect.normalize()
        if rect.x + rect.width > game_surface.get_width():
            rect[2] = game_surface.get_width() - rect.x
        rect.normalize()
        if rect.y + rect.height > game_surface.get_height():
            rect[3] = game_surface.get_height() - rect.y
        rect.normalize()



        try:
            part = game_surface.subsurface(rect)
            screen.blit(part, (quake["offset"][0] + (rect[0]), quake["offset"][1] + (rect[1]) + spee["offset"]))
        except:
            print("Off screen...")
        # screen.blit(pygame.transform.scale(game_surface, (2560, 1360)), (quake["offset"][0], quake["offset"][1]))



        blit_loc = [quake["offset"][0] + (rect[0]), quake["offset"][1] + (rect[1]) + spee["offset"]]
        if doOnOpposite[0]:
            blit_loc[0] = quake["offset"][0] + (rect[0]) + (rect.width - 256)
        if doOnOpposite[1]:
            blit_loc[1] = quake["offset"][1] + (rect[1]) + (rect.height - 256) + spee["offset"]

        screen.blit(vignette_amin[vignette_number], blit_loc)


        for bullet in bullets:
            screen.blit(bullet_glow_image, bullet["rect"].move(-mapX, -mapY))



    else:
        screen.blit(game_surface, (0 + int(quake["offset"][0]), 0 + int(quake["offset"][1] + spee["offset"])))
    # game_surface.scroll(int(quake["offset"][0]), int(quake["offset"][1] + spee["offset"]))
    # screen.blit(game_surface, (0, 0))
    if current_game_state != game_state_dict["start"]:
        for camera in camera_list:
            camera['alpha'] += 1
            if not camera['active']:
                if int(camera['alpha'] / 20) % 2 == 0:
                    if camera['rect'][0] > player['rect'][0]:
                        screen.blit(camera_dot_images[1], camera['rect'].move(-mapX, -mapY))
                    else:
                        screen.blit(camera_dot_images[0], camera['rect'].move(-mapX, -mapY))

    colorkey = (0, 0, 0)
    hud_surface.set_colorkey(colorkey)
    screen.blit(hud_surface, (0 - int(quake["offset"][0]), 0 - int(quake["offset"][1])))
    pygame.display.flip()

    # Delay until time for next frame
    clock.tick(30)
    return

menuMusic.play(-1)
# Python cleverness to allow this file to
# be used as a module or executed directly
if __name__ == "__main__":
    game_init()
