import pygame
import sys
import random
from Colors import Colors
import os
from UI import create_buttons, draw_rounded_button
from Config import screen_width, screen_height, screen, font

pygame.init()


info = pygame.display.Info()
screen_width, screen_height = info.current_w, info.current_h
screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
pygame.display.set_caption("Treasure Hunt")


# âm thanh
pygame.mixer.music.load('Sound/begin.mp3')
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play()

# Hình độ khó
# slider_image = pygame.image.load('Image/Slider.jpg')
# slider_image = pygame.transform.scale(slider_image, (280, 30))
# button_image = pygame.image.load('Image/Dragger.jpg')
# button_image = pygame.transform.scale(button_image, (30, 50))
background_image = pygame.image.load('Image/background.jpg')  # Tải hình nền mới
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))  


# Hàm vẽ nền
def draw_background():
    screen.blit(background_image, (0, 0))  # Vẽ hình nền mới
    for star in stars:
        if star['visible']:
            pygame.draw.circle(screen, Colors.WHITE, (star['x'], star['y']), star['size'])

# tạo các ngôi sao trên nền
def create_stars(num_stars):
    stars = []
    for _ in range(num_stars):
        star = {
            'x': random.randint(0, screen_width),
            'y': random.randint(0, screen_height),
            'size': random.randint(1, 2),
            'visible': True
        }
        stars.append(star)
    return stars



# Vẽ nền với ngôi sao



# # Draw colored text
# def draw_colored_text(surface, text, center):
#     colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 165, 0), (75, 0, 130), (238, 130, 238)]
#     font = pygame.font.Font("Font/diego3d.ttf", 60)
#     angle = 0
#     total_width = sum(font.size(char)[0] * 1.2 for char in text)
#     start_x = (screen_width - total_width) // 2
#     position_y = 20

#     for i, char in enumerate(text):
#         char_color = colors[i % len(colors)]
#         char_surface = font.render(char, True, char_color)
#         char_rect = char_surface.get_rect(topleft=(start_x + angle, position_y))
#         surface.blit(char_surface, char_rect)
#         angle += font.size(char)[0] * 1.2

def draw_instruction_box():
    pygame.draw.rect(screen, Colors.WHITE, (screen_width // 4, screen_height // 4, screen_width // 2, screen_height // 2), 0, 15)
    
    # Thêm viền ngoài đẹp
    pygame.draw.rect(screen, Colors.PURPLE_2, (screen_width // 4 - 5, screen_height // 4 - 5, screen_width // 2 + 10, screen_height // 2 + 10), 5, 15)
    
    # Tiêu đề
    title_font = pygame.font.Font("Font/Jomplang-6Y3Jo.ttf", 40)
    title_text = title_font.render("Instruction", True, Colors.DARK_BLUE)
    title_rect = title_text.get_rect(center=(screen_width // 2, screen_height // 4 + 30))
    screen.blit(title_text, title_rect)
    
    # Nội dung Instruction
    content_font = pygame.font.Font("Font/Jomplang-6Y3Jo.ttf", 28)
    instruction_text = """Happy happy happy
    """
    
    content_lines = instruction_text.split('\n')
    y_offset = screen_height // 4 + 80  # Vị trí ban đầu
    for line in content_lines:
        content_text = content_font.render(line, True, Colors.DARK_BLUE)
        content_rect = content_text.get_rect(center=(screen_width // 2, y_offset))
        screen.blit(content_text, content_rect)
        y_offset += 40  # Tăng độ cao cho mỗi dòng
    
    # Thêm nút "X" để đóng bảng
    close_button_rect = pygame.Rect(screen_width // 2 + screen_width // 4 - 40, screen_height // 4 - 40, 40, 40)
    pygame.draw.rect(screen, Colors.RED, close_button_rect, border_radius=10)
    close_text = pygame.font.Font("Font/Jomplang-6Y3Jo.ttf", 28).render("X", True, Colors.WHITE)
    close_text_rect = close_text.get_rect(center=close_button_rect.center)
    screen.blit(close_text, close_text_rect)

# Draw rounded button
def draw_rounded_button(surface, text, x, y, width, height, color, font_size):
    pygame.draw.rect(surface, color, (x, y, width, height), border_radius=15)
    font = pygame.font.Font("Font/Jomplang-6Y3Jo.ttf", font_size)
    label = font.render(text, True, Colors.WHITE)
    text_rect = label.get_rect(center=(x + width // 2, y + height // 2))
    surface.blit(label, text_rect)


start_button_rect = pygame.Rect(screen_width // 2 - 100, 650, 200, 60)


# Draw difficulty buttons with adjusted spacing
def draw_difficulty_buttons(screen, selected_difficulty):
    font = pygame.font.Font("Font/Jomplang-6Y3Jo.ttf", 36)  # Sử dụng font giống nút Start
    start_button_color = Colors.DARK_BLUE
    buttons = [
        {"label": "Easy", "value": 10, "rect": pygame.Rect(start_button_rect.x - 200+70, 550, 130, 50)},
        {"label": "Normal", "value": 20, "rect": pygame.Rect(start_button_rect.x - 60+90, 550, 160, 50)},
        {"label": "Hard", "value": 30, "rect": pygame.Rect(start_button_rect.x + 120+110, 550, 130, 50)},
    ]
    level_label_font = pygame.font.Font("Font/Jomplang-6Y3Jo.ttf", 36)  # Cập nhật font cho nhãn
    level_label_text = level_label_font.render("GAME LEVEL ", True, Colors.WHITE)
    level_label_rect = level_label_text.get_rect(center=(screen_width // 2 , 500))
    screen.blit(level_label_text, level_label_rect)
    for button in buttons:
        color = start_button_color if button["value"] == selected_difficulty else (180, 180, 180)
        pygame.draw.rect(screen, color, button["rect"], border_radius=10)
        text = font.render(button["label"], True, Colors.WHITE)  # Màu chữ trắng giống nút Start
        text_rect = text.get_rect(center=button["rect"].center)
        screen.blit(text, text_rect)
    return buttons





# Set custom font
custom_font = pygame.font.Font("Font/UTM-Birds-Paradise.ttf", 20)
#difficulty_value = 10  # Giá trị ban đầu của thanh trượt là 10


# Main variables
#stars = create_stars(10000)  # Generate 1000 stars
difficulty_value = 10  # Initial difficulty level

# Main game loop

stars = create_stars(500)
# slider_length = 300
show_instruction = False  



# Vòng lặp chính
current_page = 0 
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            mouse_pos = pygame.mouse.get_pos()
        
            # Kiểm tra xem có click vào nút độ khó nào không
            for button in difficulty_buttons:
                if button["rect"].collidepoint(mouse_pos):
                    difficulty_value = button["value"]                    
                # Nếu bạn muốn vẽ lại MAZE ngay sau khi chọn độ khó
                # bạn có thể gọi lại hàm vẽ maze ở đây nếu cần
            if screen_width // 2 - 100 <= mouse_x <= screen_width // 2 + 100 and 650 <= mouse_y <= 710:
                pygame.mixer.music.stop()        
                     
                with open('difficulty.txt', 'w') as f:
                    f.write("")
                    f.write(str(difficulty_value))
                
                import subprocess

                subprocess.Popen(['python', 'Game.py'])
                #os.execv(sys.executable, ['python'] + [os.path.join(os.getcwd(), 'Game.py')])
                #exec(open("Game.py", encoding="utf-8").read())
            # Kiểm tra nếu click vào nút "Exit"
            elif screen_width - 220 <= mouse_x <= screen_width - 20 and screen_height - 80 <= mouse_y <= screen_height - 20:
                pygame.quit()
                sys.exit()
            elif 0 <= mouse_x <= 200 and screen_height - 80 <= mouse_y <= screen_height - 20:
                show_instruction = True  # Hiển thị bảng Instruction khi nhấn vào nút INSTRUCTION

            
            # Kiểm tra nếu click vào nút "X" để đóng bảng Instruction
            if show_instruction and screen_width // 2 + screen_width // 4 - 40 <= mouse_x <= screen_width // 2 + screen_width // 4 and screen_height // 4 - 40 <= mouse_y <= screen_height // 4:
                show_instruction = False  # Ẩn bảng Instruction khi nhấn vào X
            
               


    draw_background()  # Draw background with stars

    difficulty_buttons = draw_difficulty_buttons(screen, difficulty_value)

    # Tải hình ảnh logo
    logo_image = pygame.image.load('Image/logo.png')
    logo_image = pygame.transform.scale(logo_image, (600, 394))  # Thay đổi kích thước logo theo ý muốn
    logo_x = (screen_width - logo_image.get_width()) // 2 # Dời logo xuống dưới một chút
    logo_y = 40  # Điều chỉnh giá trị này để dời logo xuống (số càng lớn càng xuống dưới)
    screen.blit(logo_image, (logo_x, logo_y))
    
    draw_rounded_button(screen, "START", screen_width // 2 - 100, 650, 200, 60, Colors.DARK_BLUE, 36)
    draw_rounded_button(screen, "EXIT", screen_width - 220, screen_height - 80, 200, 60, Colors.DARK_BLUE, 36)
    draw_rounded_button(screen, "INSTRUCTION", 0, screen_height - 80, 200, 60, Colors.DARK_BLUE, 36)

# Nếu cần hiển thị bảng Instruction
    if show_instruction:
        draw_instruction_box() 

    for star in stars:
        if random.random() < 0.01:
            star['visible'] = not star['visible']


    for star in stars:
        if random.random() < 0.01:
            star['visible'] = not star['visible']

    pygame.display.flip()