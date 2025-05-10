import pygame
import sys
import random
import os
from Config import screen, screen_width, screen_height, maze_matrix, cell_width, cell_height, goal_image, goal_rect, background_image, lose_image, maze_size, win_image, key_image, font
from Player import Player
from Maze import Maze
from UI import draw_rounded_button
from Colors import Colors
from Boat import Boat
from Key import generate_keys, check_collect
from UI import create_buttons

pygame.init()

def ai_move(auto_move_path, auto_move_index, maze_matrix, boat):
    if auto_move_path is not None and auto_move_index < len(auto_move_path):
        direction = auto_move_path[auto_move_index]
        boat.move(direction, maze_matrix)
        print(f"AI moves to {boat.row}, {boat.col}")
        return auto_move_index + 1
    return auto_move_index

def draw_info_box():
    info_box_rect = pygame.Rect(screen_width - 450, 120, 380, 200)
    pygame.draw.rect(screen, (0, 0, 0), info_box_rect, 3)
    pygame.draw.rect(screen, Colors.PINK, info_box_rect.inflate(-3*2, -3*2))

    title_font = pygame.font.Font("Font/Jomplang-6Y3Jo.ttf", 30)
    title_text = title_font.render("Monster Info", True, (0, 0, 0))
    title_rect = title_text.get_rect(topleft=(screen_width - 440, 130))
    screen.blit(title_text, title_rect)

    coords_font = pygame.font.Font("Font/Jomplang-6Y3Jo.ttf", 36)
    coordinates_text = coords_font.render(f"Coordinates: ({boat.row}, {boat.col})", True, (0, 0, 0))
    screen.blit(coordinates_text, (screen_width - 430, 170))

    steps_text = coords_font.render(f"Steps: {boat.step_count}", True, (0, 0, 0))
    screen.blit(steps_text, (screen_width - 430, 210))

    time_text = coords_font.render(f"Time: {monster_elapsed_time} s", True, (0, 0, 0))
    screen.blit(time_text, (screen_width - 430, 250))

def draw_monster_path(boat):
    if not show_path or not game_over or not boat.get_monster_path():
        return

    monster_path = boat.get_monster_path()
    for i in range(len(monster_path) - 1):
        start_pos = (monster_path[i][1] * cell_width + cell_width // 2, monster_path[i][0] * cell_height + cell_height // 2)
        end_pos = (monster_path[i + 1][1] * cell_width + cell_width // 2, monster_path[i + 1][0] * cell_height + cell_height // 2)
        pygame.draw.line(screen, Colors.PINK, start_pos, end_pos, 5)
        dx = end_pos[0] - start_pos[0]
        dy = end_pos[1] - start_pos[1]
        length = (dx**2 + dy**2)**0.5
        if length > 0:
            dx = dx / length
            dy = dy / length
        mid_pos = (start_pos[0] + dx * length * 0.5, start_pos[1] + dy * length * 0.5)
        arrow_size = 10
        arrow_points = [
            (mid_pos[0] - dx * arrow_size + dy * arrow_size / 2, mid_pos[1] - dy * arrow_size - dx * arrow_size / 2),
            (mid_pos[0], mid_pos[1]),
            (mid_pos[0] - dx * arrow_size - dy * arrow_size / 2, mid_pos[1] - dy * arrow_size + dx * arrow_size / 2)
        ]
        pygame.draw.polygon(screen, Colors.PINK, arrow_points)
        pygame.draw.circle(screen, Colors.PINK, start_pos, 8)

def reset_game():
    global player_step_counter, keys, collected_keys, algorithm_selected, game_over, player_won, ai_active, start_time, num_keys, show_algorithm_panel, monster_start_time, monster_elapsed_time, show_path, path_printed, is_reset_allowed, trained_path

    player.reset_position()
    player_step_counter = 0

    boat.row, boat.col = maze_size - 1, 0
    boat.path = None
    boat.path_index = 0
    boat.step_count = 0  # Reset step_count của boat về 0
    boat.monster_path = [(boat.row, boat.col)]

    num_keys = random.randint(3, 5)
    keys = generate_keys(maze_matrix, num_keys)
    collected_keys = 0

    algorithm_selected = None
    game_over = False
    player_won = False
    ai_active = False
    trained_path = None

    if os.path.exists("q_table.pkl"):
        os.remove("q_table.pkl")
        print("Deleted Q-table file")

    start_time = pygame.time.get_ticks()
    monster_start_time = None
    monster_elapsed_time = 0

    show_path = False
    path_printed = False

    show_algorithm_panel = False
    print("Game reset")
    is_reset_allowed = False

win_sound = pygame.mixer.Sound("Sound/chucmung.wav")
lose_sound = pygame.mixer.Sound("Sound/lose.wav")

pygame.init()
player = Player(0, 0)
boat = Boat(maze_size - 1, 0)
maze = Maze(maze_matrix)
num_keys = random.randint(3, 5)
keys = generate_keys(maze_matrix, num_keys)
collected_keys = 0
buttons = create_buttons(screen_width, screen_height)

win_display_start_time = None
sound_played = False
game_over = False
player_won = False
algorithm_selected = None
start_time = pygame.time.get_ticks()
ai_active = False
auto_move_delay = 10
last_move_time = pygame.time.get_ticks()
last_debug_time = pygame.time.get_ticks()
show_algorithm_panel = False
monster_start_time = None
monster_elapsed_time = 0
show_path = False
path_printed = False
is_reset_allowed = True
last_ai_move_time = pygame.time.get_ticks()
trained_path = None

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if not game_over:
                direction = None
                if event.key == pygame.K_LEFT:
                    direction = (0, -1)
                elif event.key == pygame.K_RIGHT:
                    direction = (0, 1)
                elif event.key == pygame.K_UP:
                    direction = (-1, 0)
                elif event.key == pygame.K_DOWN:
                    direction = (1, 0)
                if direction:
                    player.move(direction, maze_matrix)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if show_algorithm_panel:
                if buttons["bfs"].collidepoint(event.pos):
                    algorithm_selected = "BFS"
                    show_algorithm_panel = False
                    print("Selected BFS")
                    trained_path = None
                elif buttons["a_star"].collidepoint(event.pos):
                    algorithm_selected = "A*"
                    show_algorithm_panel = False
                    print("Selected A*")
                    trained_path = None
                elif buttons["simulated_annealing"].collidepoint(event.pos):
                    algorithm_selected = "Simulated Annealing"
                    show_algorithm_panel = False
                    print("Selected Simulated Annealing")
                    trained_path = None
                elif buttons["stochastic_hc"].collidepoint(event.pos):
                    algorithm_selected = "Stochastic Hill Climbing"
                    show_algorithm_panel = False
                    print("Selected Stochastic Hill Climbing")
                    trained_path = None
                elif buttons["ucs"].collidepoint(event.pos):
                    algorithm_selected = "UCS"
                    show_algorithm_panel = False
                    print("Selected UCS")
                    trained_path = None
                elif buttons["beam_search"].collidepoint(event.pos):
                    algorithm_selected = "Beam Search"
                    show_algorithm_panel = False
                    print("Selected Beam Search")
                    trained_path = None
                elif buttons["q_learning"].collidepoint(event.pos):
                    algorithm_selected = "Q-Learning"
                    show_algorithm_panel = False
                    print("Selected Q-Learning")
                    if boat.path is None or (player.row, player.col) != boat.last_target:
                        boat.update_path(maze_matrix, (player.row, player.col), algorithm_selected)
                        trained_path = boat.path
                    boat.last_target = (player.row, player.col)
            elif not show_algorithm_panel:
                if buttons["reset"].collidepoint(event.pos):
                    is_reset_allowed = True
                    print("Reset button pressed")
                    reset_game()
                elif buttons["home"].collidepoint(event.pos):
                    print("Home button pressed")
                    pygame.mixer.music.stop()
                    exec(open("Home.py", encoding="utf-8").read())
                elif buttons["algorithm_menu"].collidepoint(event.pos):
                    show_algorithm_panel = not show_algorithm_panel
                    print("Algorithm menu toggled")
                elif buttons["exit"].collidepoint(event.pos):
                    print("Exit button pressed")
                    pygame.quit()
                    sys.exit()
                elif buttons["show_path"].collidepoint(event.pos):
                    print("Show Path button pressed")
                    if game_over:
                        show_path = not show_path

    current_time = pygame.time.get_ticks()
    elapsed_time = (current_time - start_time) // 1000

    if current_time - last_debug_time >= 1000:
        print(f"Elapsed time: {elapsed_time}, Selected algorithm: {algorithm_selected}, Game over: {game_over}, AI active: {ai_active}")
        last_debug_time = current_time

    if elapsed_time >= 5 and algorithm_selected and not game_over and not ai_active:
        monster_start_time = pygame.time.get_ticks()
        ai_active = True
        print("AI activated after 5 seconds")

    if ai_active and not game_over:
        if current_time - last_ai_move_time >= 150:
            try:
                # Chỉ gọi update_path nếu cần (tránh lặp lại không cần thiết)
                if algorithm_selected == "Q-Learning":
                    if trained_path is None or boat.path_index >= len(trained_path):
                        if (player.row, player.col) != boat.last_target:
                            boat.update_path(maze_matrix, (player.row, player.col), algorithm_selected)
                            trained_path = boat.path
                            boat.last_target = (player.row, player.col)
                else:
                    # Các thuật toán khác không cần trained_path
                    if boat.path is None or boat.path_index >= len(boat.path) or (player.row, player.col) != boat.last_target:
                        boat.update_path(maze_matrix, (player.row, player.col), algorithm_selected)
                        boat.last_target = (player.row, player.col)
                boat.move(maze_matrix)
            except Exception as e:
                print(f"Error in AI movement: {e}")
            last_ai_move_time = current_time

        if (boat.row, boat.col) == (player.row, player.col):
            game_over = True
            player_won = False

    if ai_active and not game_over and monster_start_time is not None:
        monster_elapsed_time = (pygame.time.get_ticks() - monster_start_time) // 1000

    if check_collect(player.row, player.col, keys):
        collected_keys += 1

    if player.is_at_goal():
        if collected_keys == num_keys:
            game_over = True
            player_won = True
        else:
            game_over = True
            player_won = False

    screen.blit(background_image, (0, 0))
    goal_x = (maze_size - 1) * cell_width + (cell_width - goal_rect.width) // 2
    goal_y = (maze_size - 1) * cell_height + (cell_height - goal_rect.height) // 2
    screen.blit(goal_image, (goal_x, goal_y))
    maze.draw(screen)
    player.draw(screen)
    boat.draw(screen)
    for key in keys:
        key.draw(screen)

    keys_textbox_rect = pygame.Rect(screen_width - 400, 60, 300, 50)
    pygame.draw.rect(screen, Colors.WHITE, keys_textbox_rect, 3)
    pygame.draw.rect(screen, Colors.PINK, keys_textbox_rect.inflate(-3*2, -3*2))
    keys_text = font.render(f"Keys: {collected_keys}/{num_keys}", True, Colors.WHITE)
    keys_text_rect = keys_text.get_rect(center=keys_textbox_rect.center)
    screen.blit(keys_text, keys_text_rect)

    draw_info_box()
    draw_rounded_button(buttons["show_path"], "Show Path", Colors.DARK_BLUE, 36)
    draw_rounded_button(buttons["reset"], "Reset", Colors.DARK_BLUE, 36)
    draw_rounded_button(buttons["algorithm_menu"], "Algorithm", Colors.DARK_BLUE, 36)
    draw_rounded_button(buttons["home"], "Home", Colors.DARK_BLUE, 36)
    draw_rounded_button(buttons["exit"], "Exit", Colors.DARK_BLUE, 36)

    draw_monster_path(boat)

    if game_over and not path_printed:
        print("Monster path:", boat.get_monster_path())
        path_printed = True

    if game_over:
        if win_display_start_time is None:
            win_display_start_time = pygame.time.get_ticks()

        # Phát âm thanh 1 lần
        if not sound_played:
            if player_won:
                win_sound.play()
            else:
                lose_sound.play()
            sound_played = True

        elapsed_since_win = pygame.time.get_ticks() - win_display_start_time
        if elapsed_since_win <= 5000:  # Hiển thị hình trong 5 giây
            if player_won:
                screen.blit(win_image, (
                    screen_width // 2 - win_image.get_width() // 2,
                    screen_height // 2 - win_image.get_height() // 2
                ))
            else:
                screen.blit(lose_image, (
                    screen_width // 2 - lose_image.get_width() // 2,
                    screen_height // 2 - lose_image.get_height() // 2
                ))


    if show_algorithm_panel:
        panel_rect = pygame.Rect(50, 100, 250, 400)
        pygame.draw.rect(screen, Colors.PURPLE_2, (screen_width // 4, screen_height // 4, screen_width // 2, screen_height // 2), 0, 15)
        pygame.draw.rect(screen, Colors.PURPLE_2, (screen_width // 4 - 5, screen_height // 4 - 5, screen_width // 2 + 10, screen_height // 2 + 10), 5, 15)
        algo_buttons = ["bfs", "a_star", "simulated_annealing", "stochastic_hc", "ucs", "beam_search", "q_learning"]

        panel_x = screen_width // 4
        panel_y = screen_height // 4
        panel_width = screen_width // 2
        panel_height = screen_height // 2

        button_width = 230
        button_margin = 10
        button_height = 40
        offset_right = 20
        offset_down = 30

        total_buttons_height = len(algo_buttons) * (button_height + button_margin)
        y_offset = ((panel_height - total_buttons_height) // 2) + offset_down

        for i, key in enumerate(algo_buttons):
            btn_rect = pygame.Rect(
                panel_x + (panel_width - button_width) // 2 + offset_right,
                panel_y + y_offset + i * (button_height + button_margin),
                button_width,
                button_height
            )
            draw_rounded_button(btn_rect, key.replace("_", " ").upper(), Colors.PINK, 28)
            buttons[key] = btn_rect

        close_button_rect = pygame.Rect(screen_width // 2 + screen_width // 4 - 40, screen_height // 4 - 40, 40, 40)
        pygame.draw.rect(screen, Colors.RED, close_button_rect, border_radius=10)
        close_text = pygame.font.Font("Font/Jomplang-6Y3Jo.ttf", 28).render("X", True, Colors.WHITE)
        close_text_rect = close_text.get_rect(center=close_button_rect.center)
        screen.blit(close_text, close_text_rect)

    pygame.display.flip()