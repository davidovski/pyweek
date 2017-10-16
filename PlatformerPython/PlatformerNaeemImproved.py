import pygame
import sys
import random

# Your code here
maxX = 0

ASSET_FOLDER = "assets/"

level_1 = [
    "######################################################################",
    "#                                                                    #",
    "#                                                                    #",
    "#                        ####                                      x #",
    "#         E T          ##                          ################# #",
    "#        #####      ###                                              #",
    "# T             ###     E                                            #",
    "#######                ######                  ##################    #",
    "#              o                                                     #",
    "#          #########                                                 #",
    "#                                  ######################            #",
    "#     E  T                                                           #",
    "#    ##########       #######                                        #",
    "#                                                                    #",
    "#                  E                                                 #",
    "######################################################################",
]

level_2 = [
    "#############################################################################################################",
    "#                                                                                                           #",
    "#x   E                     T                                                                                #",
    "######             E       ##                                                                               #",
    "#            ########                                                                                       #",
    "#                      ##  T                                                                                #",
    "#    ######                ##                                                                               #",
    "#T              ###                                                                                         #",
    "###                     E                                                                                   #",
    "#                   #######                                                                                 #",
    "#       E                                                                                                   #",
    "#       ############                                                                                        #",
    "######                                                                                                      #",
    "#                       #####                                                                               #",
    "#o         ######           E                                                                               #",
    "#############################################################################################################",
]

def custom_game_init():
    global title_font
    global level_font
    global player
    global level_list
    global level_exit
    global enemy_images
    global treasure_image
    global background_image
    global mapX, guns

    player = {
        "images": [
            pygame.image.load(ASSET_FOLDER + "KaleLeft.png"),
            pygame.image.load(ASSET_FOLDER + "KaleLeft.png"),
            pygame.image.load(ASSET_FOLDER + "KaleLeft.png"),
            pygame.image.load(ASSET_FOLDER + "KaleLeft.png"),
            pygame.image.load(ASSET_FOLDER + "KaleRight.png"),
            pygame.image.load(ASSET_FOLDER + "KaleRight.png"),
            pygame.image.load(ASSET_FOLDER + "KaleRight.png"),
            pygame.image.load(ASSET_FOLDER + "KaleRight.png")
        ],
        "rect": pygame.Rect(0, 0, 32, 32),
        "start_rect": pygame.Rect(0, 0, 32, 32),
        "direction": [0,0]
    }

    level_exit = {
        "image": pygame.image.load(ASSET_FOLDER + "exit_32.png"),
        "rect": pygame.Rect(0, 0, 32, 32)
    }

    background_image = pygame.image.load(ASSET_FOLDER + "background.png")

    enemy_images = []
    enemy_images.append(pygame.image.load(ASSET_FOLDER + "enemy_left_32_0.png"))
    enemy_images.append(pygame.image.load(ASSET_FOLDER + "enemy_left_32_1.png"))
    enemy_images.append(pygame.image.load(ASSET_FOLDER + "enemy_right_32_0.png"))
    enemy_images.append(pygame.image.load(ASSET_FOLDER + "enemy_right_32_1.png"))

    treasure_image = pygame.image.load(ASSET_FOLDER + "treasure_32.png")

    guns = {
        "image": pygame.image.load(ASSET_FOLDER + "small_pistol.png"),
        "rect": pygame.Rect(0, 0, 32, 32)
    }
    guns['rect'] = guns['rect'].move(999,146)
    title_font = pygame.font.SysFont("jokerman", 50)
    level_font = pygame.font.SysFont("ariel", 32)

    add_game_state("start", "update_game_start", "draw_game_start")
    add_game_state("running", "update_game_running", "draw_game_running")
    set_game_state("start")

    level_list = []
    level_list.append(level_1)
    level_list.append(level_2)

    mapX = 0
    
    return

def update_game_running():
    global keys
    global player
    global enemy_list
    global treasure_list
    global score
    global jump_step

    move_step = 6
    gravity = 8
    enemy_move_step = 4
    #deadzone_right = mapX - 

    # Read the keyboard input and move the marker
    if keys[pygame.K_LEFT]:
        if check_and_move_player(-move_step, 0):
            player['direction'][0] = -move_step

    if keys[pygame.K_RIGHT]:
        if check_and_move_player(move_step, 0):
            player['direction'][0] = move_step

    # Move down by gravity
    # if no collision, we must be 'in the air'
    in_air = check_and_move_player(0, gravity)

    # Allow jumping if not already in the air
    if keys[pygame.K_SPACE] and not in_air:
        jump_step = 30

    # do the jump step move and if it results in a collision
    # reduce the jump_step immediately to zero
    if not check_and_move_player(0, -jump_step):
        jump_step = 0

    # reduce the jump step back down to zero over time
    if jump_step != 0:
        jump_step -= 2

    check_and_move_enemies(enemy_move_step)

    # Check if we have reached the exit or hit enemy
    if player['rect'].colliderect(level_exit['rect']):
        score += len(enemy_list)
        load_next_level()
    

    for enemy in enemy_list:
        if player['rect'].colliderect(enemy['rect']):
            set_game_state("start")

    for treasure in treasure_list:
        if treasure['active'] and player['rect'].colliderect(treasure['rect']):
            score = score + treasure['value']
            treasure['active'] = False

    return

def draw_game_running():
    global screen
    global map_surface
    global level_exit
    global enemy_list
    global level_index
    global score
    global mapX, guns

#    mapX = mapX + 1
    levelWidth = len(level_list[level_index][0]) * 32
    halfScreen = screen.get_width() / 2
    
    player_frame = player['rect'].centerx//16 % 4
    if player['direction'][0] > 0:
        player_frame_start = 4
    else:
        player_frame_start = 0
    

    wall_middle_sprite = pygame.image.load(ASSET_FOLDER + "wall_32.png")
    wall_left_sprite = pygame.image.load(ASSET_FOLDER + "wall_left_32.png")
    wall_right_sprite = pygame.image.load(ASSET_FOLDER + "wall_right_32.png")

    map_area = pygame.Rect(0, 0, 0, 0)
    map_area.unionall_ip(wall_list)

    screen.blit(background_image, (0,0))
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

        screen.blit(wall_sprite, wall.move(-mapX, 0))
#    screen.blit(map_surface, (0, 0))
    screen.blit(player['images'][player_frame_start + player_frame], player['rect'].move(-mapX, 0))
    screen.blit(level_exit['image'], level_exit['rect'].move(-mapX, 0))

    for treasure in treasure_list:
        if treasure['active']:
            screen.blit(treasure['image'], treasure['rect'].move(-mapX, 0))

    for enemy in enemy_list:
        enemy_frame = enemy['rect'].centerx//8 % 2
        if enemy['direction'][0] > 0:
            enemy_frame_start = 2
        else:
            enemy_frame_start = 0
        screen.blit(enemy['images'][enemy_frame_start + enemy_frame], enemy['rect'].move(-mapX, 0))

    rendered_text = level_font.render("Level: " + str(level_index + 1) + "  Score: " + str(score), 1, (255, 255, 255))
    position = rendered_text.get_rect()
    position.midbottom = screen.get_rect().midbottom
    screen.blit(rendered_text, position)

    screen.blit(guns['image'], guns['rect'])

    if player['rect'].x - mapX > 0.8 * screen.get_width():
        mapX += 8
    elif player['rect'].x - mapX < 0.2 * screen.get_width():
        mapX -= 8

    if mapX < 0:
        mapX = 0
    elif mapX > levelWidth - screen.get_width():
        mapX = levelWidth - screen.get_width()
        
    return

def update_game_start():
    global keys
    if keys[pygame.K_SPACE]:
        custom_game_reset()
        set_game_state("running")
    return

def draw_game_start():
    global title_font
    global screen
    global score

    rendered_text = title_font.render("Press Space to Start", 1, (255, 255, 255))
    shadow_text = title_font.render("Press Space to Start", 1, (0, 0, 0))

    position = rendered_text.get_rect()
    position.center = screen.get_rect().center
    screen.blit(shadow_text, position.move((5, 5)))
    screen.blit(rendered_text, position)

    score_text = title_font.render("Last Score: " + str(score), 1, (255, 255, 255))
    score_position = score_text.get_rect()
    score_position.midtop = position.midbottom
    screen.blit(score_text, score_position)
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
    global treasure_list

    wall_list = []
    enemy_list = []
    treasure_list = []

    # Reset the wall & enemy lists
    wall_list[:] = []
    enemy_list[:] = []
    treasure_list[:] = []

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
            elif col == "E":
                add_enemy(x, y, 4)

            # Set the treasure position if we find an 'T'
            elif col == "T":
                add_treasure(x, y, 10)

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
    global background_image

    # Find the size of the image
    # required by merging all the rectangles
    # in the list
    wall_middle_sprite = pygame.image.load(ASSET_FOLDER + "wall_32.png")
    wall_left_sprite = pygame.image.load(ASSET_FOLDER + "wall_left_32.png")
    wall_right_sprite = pygame.image.load(ASSET_FOLDER + "wall_right_32.png")
    map_area = pygame.Rect(0, 0, 0, 0)
    map_area.unionall_ip(wall_list)

    # create the image
    map_surface = pygame.Surface((map_area.width, map_area.height))
    map_surface.blit(background_image, (0,0))

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


        map_surface.blit(wall_sprite, wall)

    # return the image surface
    return map_surface

def add_treasure(x, y, value):
    """
    Create a new enemy data dictionary
    Add it to the enemy list
    """
    global treasure_list
    global treasure_image

    treasure = {
        "image": treasure_image,
        "rect": pygame.Rect(x, y, 32, 32),
        "active": True,
        "value": value
    }
    treasure_list.append(treasure)

def add_enemy(x, y, move_step):
    """
    Create a new enemy data dictionary
    Add it to the enemy list
    """
    global enemy_list
    global enemy_images

    enemy = {
        "images": enemy_images,
        "rect": pygame.Rect(x, y, 32, 32),
        "start_rect": pygame.Rect(x, y, 32, 32),
        "direction": [move_step, 0]
    }
    enemy_list.append(enemy)

def load_next_level():
    """
    Parses the level list (with wrap around)
    to create new map objects & map image surface
    """
    global wall_list
    global map_surface
    global level_index
    global level_list

    level_index += 1
    if level_index == len(level_list):
        level_index = 0

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
    global jump_step

    score = 0
    level_index = -1
    load_next_level()

    jump_step = 0
    for enemy in enemy_list:
        enemy['rect'] = enemy['start_rect']

    player['rect'] = player['start_rect']

    return

def check_and_move_player(move_x, move_y):
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

    rect_index = player_move_rect.collidelist(wall_list)
    if rect_index == -1:
        player['rect'] = player_move_rect
        return True
    else:
        collision_rect = wall_list[rect_index]
        if(move_x > 0):
            player['rect'].right = collision_rect.left
        if(move_x < 0):
            player['rect'].left = collision_rect.right
        if(move_y > 0):
            player['rect'].bottom = collision_rect.top
        if(move_y < 0):
            player['rect'].top = collision_rect.bottom

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

    for enemy in enemy_list:
        enemy_vector = enemy['direction']

        # update the enemy move rectangle according to direction vector & speed
        enemy_move_rect = enemy['rect'].move(enemy_vector[0], enemy_vector[1])

        # If the enemy has hit a wall, generate a new direction
        if enemy_move_rect.collidelist(wall_list) != -1:
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
    global screen
    global clock
    global keys, last_keys
    global game_state_dict
    global current_game_state

    # Initialise pygame
    pygame.init()

    # Screen
    screen = pygame.display.set_mode((960, 510), pygame.DOUBLEBUF)

    keys = pygame.key.get_pressed()
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
        game_input()
        game_update()
        game_draw()
    return


def game_input():
    """
    Fill the keys list with the
    currently pressed keys
    and check for quit
    """
    global keys
    global last_keys

    last_keys = keys
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
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


def game_draw():
    """
    Draw to the screen
    by calling the current game state's
    draw function
    """
    global screen
    global clock
    global game_state_dict
    global current_game_state

    # Clear the screen
    screen.fill([127, 127, 127])

    if current_game_state:
        globals()[current_game_state["draw_function"]]()

    # Update the display to the screen
    pygame.display.flip()

    # Delay until time for next frame
    clock.tick(50)
    return


# Python cleverness to allow this file to
# be used as a module or executed directly
if __name__ == "__main__":
    game_init()
