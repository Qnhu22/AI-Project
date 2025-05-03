import pygame
from Config import screen_width, screen_height, screen, font
from Colors import Colors


def draw_rounded_button(button_rect, text, color, font_size, border_color_outer=Colors.PURPLE_2, border_color_inner=Colors.LIGHT_YELLOW, border_thickness=3, radius=0, offset_x=-40):
    # Điều chỉnh vị trí của nút bằng cách dịch sang trái `offset_x` pixel
    adjusted_rect = button_rect.move(offset_x, 0)
    pygame.draw.rect(screen, border_color_outer, adjusted_rect, border_thickness + 2, border_radius=radius)  
    pygame.draw.rect(screen, border_color_inner, adjusted_rect.inflate(-border_thickness * 2, -border_thickness * 2), border_thickness, border_radius=radius)   
    pygame.draw.rect(screen, color, adjusted_rect.inflate(-border_thickness * 4, -border_thickness * 4), border_radius=radius)
    font = pygame.font.Font("Font/Jomplang-6Y3Jo.ttf", font_size)
    label = font.render(text, True, Colors.WHITE)
    screen.blit(label, label.get_rect(center=adjusted_rect.center))
    



# Thiết lập các nút
def create_buttons(screen_width, screen_height):
    y_offset = 60  # Khoảng cách giữa các nút thuật toán
    bottom_y_offset = 60  # Khoảng cách giữa các nút phía dưới
    button_width = 200
    button_height = 60

    # Các nút thuật toán sẽ căn vào góc phải
    button_x = screen_width - 220  # Căn phải cho các nút thuật toán, cách bên trái 220px

    # Các nút thuật toán (sắp xếp theo chiều dọc từ trên xuống dưới)
    algorithm_buttons_y = 70  # Bắt đầu sắp xếp nút thuật toán từ y = 70

    buttons = {
        # Các nút thuật toán (sắp xếp bên phải màn hình)
        "stochastic_hc": pygame.Rect(button_x, algorithm_buttons_y + + y_offset * 2, button_width, button_height),
        "a_star": pygame.Rect(button_x, algorithm_buttons_y + y_offset * 3, button_width, button_height),
        "bfs": pygame.Rect(button_x, algorithm_buttons_y + y_offset * 4, button_width, button_height),
        "simulated_annealing": pygame.Rect(button_x, algorithm_buttons_y + y_offset * 5, button_width, button_height),
        "ucs": pygame.Rect(button_x, algorithm_buttons_y + y_offset * 6, button_width, button_height),
        "beam_search": pygame.Rect(button_x, algorithm_buttons_y + y_offset * 7, button_width, button_height),
        
        # Các nút phía dưới (sắp xếp bên trái hơn các thuật toán)
        "reset": pygame.Rect(screen_width - 300, screen_height - bottom_y_offset * 6, 200, 60),
        "algorithm_menu": pygame.Rect(screen_width - 300, screen_height - bottom_y_offset * 7, 200, 60),
        "exit": pygame.Rect(screen_width - 300, screen_height - bottom_y_offset * 8, 200, 60),
        
        # Các nút khác (Home, Game, Start, Stop)
        "home": pygame.Rect(screen_width - 300, screen_height - bottom_y_offset * 9, 200, 60),
        "game": pygame.Rect(screen_width - 220, screen_height - bottom_y_offset * 5, 200, 60),
        "start": pygame.Rect(screen_width - 220, screen_height - bottom_y_offset * 6, 200, 60),
        "stop": pygame.Rect(screen_width - 220, screen_height - bottom_y_offset * 7, 200, 60),

    }

    return buttons
