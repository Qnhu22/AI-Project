import pygame
import sys
import random
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
        boat.move(direction, maze_matrix)  # Di chuyển thuyền AI
        print(f"AI moved to {boat.row}, {boat.col}")  # In ra bước di chuyển của AI
        return auto_move_index + 1
    return auto_move_index



# Hàm reset lại game
def reset_game():
    global player_step_counter, AI_step, keys, collected_keys, algorithm_selected, game_over, player_won, ai_active, start_time, num_keys,show_algorithm_panel

    # Reset trạng thái người chơi
    player.reset_position()
   # Biến để kiểm tra xem bảng chọn thuật toán có hiển thị hay không

    player_step_counter = 0

    # Reset trạng thái thuyền
    boat.row, boat.col = maze_size - 1, 0
    boat.path = None
    boat.path_index = 0

    # Random lại keys
    num_keys = random.randint(3, 5)  # Reset số lượng keys ngẫu nhiên
    keys = generate_keys(maze_matrix, num_keys)

    collected_keys = 0  # Reset số keys đã thu thập

    # Tải âm thanh vào khi bắt đầu trò chơi hoặc reset game
    


    # Reset các biến trạng thái trò chơi
    

    AI_step = 0
    algorithm_selected = None
    game_over = False
    player_won = False
    ai_active = False

    # Reset thời gian bắt đầu
    start_time = pygame.time.get_ticks()
win_sound = pygame.mixer.Sound("Sound/chucmung.wav")  # Thay bằng đường dẫn đến tệp âm thanh win
lose_sound = pygame.mixer.Sound("Sound/lose.wav")  # Thay bằng đường dẫn đến tệp âm thanh lose

pygame.init()
player = Player(0, 0)
boat = Boat(maze_size - 1, 0)
maze = Maze(maze_matrix)
num_keys = random.randint(3, 5)
keys = generate_keys(maze_matrix, num_keys)
collected_keys = 0
buttons = create_buttons(screen_width, screen_height)

game_over = False  # Biến kiểm tra trạng thái trò chơi; False nghĩa là trò chơi vẫn đang diễn ra
player_won = False  # Biến kiểm tra xem người chơi đã thắng hay chưa; False nghĩa là người chơi chưa thắng
algorithm_selected = None  # Biến để lưu thuật toán đã chọn; None nghĩa là chưa có thuật toán nào được chọn
start_time = pygame.time.get_ticks()  # Lưu thời gian bắt đầu trò chơi
ai_active = False  # Biến kiểm tra xem AI có đang hoạt động hay không; False nghĩa là AI chưa hoạt động
auto_move_delay = 10  # Độ trễ (ms) giữa các bước tự động
last_move_time = pygame.time.get_ticks()  # Theo dõi thời gian của lần di chuyển cuối cùng

show_algorithm_panel = False


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if not game_over:
                direction = None
                if event.key == pygame.K_LEFT:
                    direction = (0, -1)  # Left
                elif event.key == pygame.K_RIGHT:
                    direction = (0, 1)   # Right
                elif event.key == pygame.K_UP:
                    direction = (-1, 0)  # Up
                elif event.key == pygame.K_DOWN:
                    direction = (1, 0)   # Down
                
                if direction: 
                    player.move(direction, maze_matrix)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if show_algorithm_panel:
                if buttons["bfs"].collidepoint(event.pos):
                    algorithm_selected = "BFS"
                    show_algorithm_panel = False
                elif buttons["a_star"].collidepoint(event.pos):
                    algorithm_selected = "A*"
                    show_algorithm_panel = False
                elif buttons["simulated_annealing"].collidepoint(event.pos):
                    algorithm_selected = "Simulated Annealing"
                    show_algorithm_panel = False
                elif buttons["stochastic_hc"].collidepoint(event.pos):
                    algorithm_selected = "Stochastic Hill Climbing"
                    show_algorithm_panel = False
                elif buttons["ucs"].collidepoint(event.pos):
                    algorithm_selected = "UCS"
                    show_algorithm_panel = False
                elif buttons["beam_search"].collidepoint(event.pos):
                    algorithm_selected = "Beam Search"
                    show_algorithm_panel = False

            if buttons["reset"].collidepoint(event.pos):
                print("Reset button clicked")
                reset_game()
            elif buttons["home"].collidepoint(event.pos):
                print("Home button clicked")
                pygame.mixer.music.stop()
                exec(open("Home.py", encoding="utf-8").read())
            elif buttons["bfs"].collidepoint(event.pos):
                print("BFS button clicked")
                algorithm_selected = "BFS"
            elif buttons["a_star"].collidepoint(event.pos):
                print("A* button clicked")
                algorithm_selected = "A*"
            elif buttons["algorithm_menu"].collidepoint(event.pos):
                show_algorithm_panel = not show_algorithm_panel  # Toggle hiển thị bảng chọn

            elif buttons["simulated_annealing"].collidepoint(event.pos):
                print("Simulated Annealing button clicked")
                algorithm_selected = "Simulated Annealing"
            elif buttons["exit"].collidepoint(event.pos):
                print("Exit button clicked")
                pygame.quit()
                sys.exit()
            elif buttons["stochastic_hc"].collidepoint(event.pos):
                print("Stochastic Hill Climbing button clicked")
                algorithm_selected = "Stochastic Hill Climbing"
            elif buttons["ucs"].collidepoint(event.pos):
                print("UCS button clicked")
                algorithm_selected = "UCS"
            elif buttons["beam_search"].collidepoint(event.pos):
                print("Beam Search Climbing button clicked")
                algorithm_selected = "Beam Search"

    current_time = pygame.time.get_ticks() # Get the current time
    elapsed_time = (current_time - start_time) // 1000 # Time elapsed since the game started

    if elapsed_time >= 5 and algorithm_selected and not game_over:
        ai_active = True
        boat.update_path(maze_matrix, (player.row, player.col), algorithm_selected)
        boat.move(maze_matrix)

        # Check if the boat catches the player
        if (boat.row, boat.col) == (player.row, player.col):
            game_over = True
            player_won = False
            game_completed = True


    if check_collect(player.row, player.col, keys):
        collected_keys += 1

    if player.is_at_goal():
            # Game over logic\ưp
            
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

    draw_rounded_button(buttons["reset"], "Reset", Colors.DARK_BLUE, 36 )
    draw_rounded_button(buttons["algorithm_menu"], "Algorithm", Colors.DARK_BLUE, 36)
    draw_rounded_button(buttons["home"], "Home",Colors.DARK_BLUE, 36)
    #draw_rounded_button(buttons["bfs"], "BFS", Colors.DARK_BLUE, 36)
    #draw_rounded_button(buttons["simulated_annealing"], "SA", Colors.DARK_BLUE, 36)
    draw_rounded_button(buttons["exit"], "Exit", Colors.DARK_BLUE, 36)
    #draw_rounded_button(buttons["a_star"], "A*", Colors.DARK_BLUE, 36)
    #draw_rounded_button(buttons["greedy"], "Greedy", Colors.DARK_BLUE, 36)
    #draw_rounded_button(buttons["stochastic_hc"], "Stochastic HC", Colors.DARK_BLUE, 36)
    #draw_rounded_button(buttons["ucs"], "UCS", Colors.DARK_BLUE, 36)
    #draw_rounded_button(buttons["beam_search"], "Beam Search", Colors.DARK_BLUE, 36)

    keys_textbox_rect = pygame.Rect(screen_width - 400, 60, 300, 50)
    pygame.draw.rect(screen, Colors.WHITE, keys_textbox_rect, 3)  # Draw border
    pygame.draw.rect(screen, Colors.PINK, keys_textbox_rect.inflate(-3*2, -3*2))  # Draw background

    keys_text = font.render(f"Keys: {collected_keys}/{num_keys}", True, Colors.WHITE)
    keys_text_rect = keys_text.get_rect(center=keys_textbox_rect.center)  #  the text
    screen.blit(keys_text, keys_text_rect)

    if game_over:
    

        #print(f"AI (Boat) Total Steps: {boat.step_count}")
        #print(f"Boat AI started at {boat.start_position} and ended at {boat.end_position}.")

        if player_won:
            screen.blit(win_image, (screen_width // 2 - win_image.get_width() // 2,
                                    screen_height // 2 - win_image.get_height() // 2))
            win_sound.play() 
        else:
            screen.blit(lose_image, (screen_width // 2 - lose_image.get_width() // 2,
                                    screen_height // 2 - lose_image.get_height() // 2))
            lose_sound.play() 
        
    if show_algorithm_panel:
        panel_rect = pygame.Rect(50, 100, 250, 400)
        pygame.draw.rect(screen, Colors.PURPLE_2, (screen_width // 4, screen_height // 4, screen_width // 2, screen_height // 2), 0, 15)  # Viền ngoài trắng
        pygame.draw.rect(screen, Colors.PURPLE_2, (screen_width // 4 - 5, screen_height // 4 - 5, screen_width // 2 + 10, screen_height // 2 + 10), 5, 15)  
        algo_buttons = ["bfs", "a_star", "simulated_annealing", "stochastic_hc", "ucs", "beam_search"]

        # Cài đặt các thông số cho các nút
        panel_x = screen_width // 4
        panel_y = screen_height // 4
        panel_width = screen_width // 2
        panel_height = screen_height // 2

        # Tính vị trí x để căn giữa nút trong bảng + đẩy qua phải một chút (ví dụ 20px)
        button_width = 230
        button_margin = 10
        button_height = 40
        

        offset_right = 20  # Đẩy sang phải
        offset_down = 30   # Đẩy xuống dưới

        total_buttons_height = len(algo_buttons) * (button_height + button_margin)
        y_offset = ((panel_height - total_buttons_height) // 2) + offset_down

        for i, key in enumerate(algo_buttons):
            btn_rect = pygame.Rect(
                panel_x + (panel_width - button_width) // 2 + offset_right,  # Căn giữa trong bảng + sang phải
                panel_y + y_offset + i * (button_height + button_margin),    # Căn giữa theo chiều dọc + xuống dưới
                button_width,
                button_height
            )

            draw_rounded_button(btn_rect, key.replace("_", " ").upper(), Colors.PINK, 28)
            buttons[key] = btn_rect

    # Thêm nút đóng
        close_button_rect = pygame.Rect(screen_width // 2 + screen_width // 4 - 40, screen_height // 4 - 40, 40, 40)
        pygame.draw.rect(screen, Colors.RED, close_button_rect, border_radius=10)
        close_text = pygame.font.Font("Font/Jomplang-6Y3Jo.ttf", 28).render("X", True, Colors.WHITE)
        close_text_rect = close_text.get_rect(center=close_button_rect.center)
        screen.blit(close_text, close_text_rect)

    
    pygame.display.flip()
