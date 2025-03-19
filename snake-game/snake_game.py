import pygame
import time
import random
import sys

# 初始化pygame
pygame.init()

# 定义颜色
white = (255, 255, 255)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)
grid_color = (30, 30, 30)  # 深灰色网格
yellow = (255, 255, 0)
purple = (128, 0, 128)
light_green = (144, 238, 144)
light_yellow = (255, 255, 224)
light_red = (255, 182, 193)
dark_gray = (40, 40, 40)
menu_bg_color = (25, 25, 40)  # 深蓝色菜单背景

# 设置显示窗口
display_width = 600
display_height = 400
dis = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Snake Game')

# 设置游戏时钟
clock = pygame.time.Clock()

# 蛇的大小和速度 - 增大蛇和食物的尺寸
snake_block = 20

# 难度级别对应的速度
EASY = 8
MEDIUM = 15
HARD = 22

# 字体设置 - 增大字体大小
font_style = pygame.font.SysFont("arial", 30)
score_font = pygame.font.SysFont("arial", 40)
title_font = pygame.font.SysFont("arial", 50, bold=True)
button_font = pygame.font.SysFont("arial", 32)

# 显示分数
def your_score(score):
    value = score_font.render("Score: " + str(score), True, white)
    dis.blit(value, [10, 10])

# 绘制蛇
def our_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(dis, green, [x[0], x[1], snake_block, snake_block])

# 显示消息
def message(msg, color, y_displace=0):
    mesg = font_style.render(msg, True, color)
    # 计算文本的宽度，以便居中显示
    text_width = mesg.get_width()
    dis.blit(mesg, [(display_width - text_width) / 2, display_height / 3 + y_displace])

# 绘制网格
def draw_grid():
    for x in range(0, display_width, snake_block):
        pygame.draw.line(dis, grid_color, (x, 0), (x, display_height))
    for y in range(0, display_height, snake_block):
        pygame.draw.line(dis, grid_color, (0, y), (display_width, y))

# 绘制按钮
def draw_button(text, x, y, width, height, inactive_color, active_color, text_color, selected=False, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    
    # 检查鼠标是否在按钮上或按钮是否被选中
    if (x < mouse[0] < x + width and y < mouse[1] < y + height) or selected:
        pygame.draw.rect(dis, active_color, (x, y, width, height))
        if click[0] == 1 and action != None:
            return action
    else:
        pygame.draw.rect(dis, inactive_color, (x, y, width, height))
    
    # 绘制按钮文字
    text_surf = button_font.render(text, True, text_color)
    text_rect = text_surf.get_rect()
    text_rect.center = ((x + (width / 2)), (y + (height / 2)))
    dis.blit(text_surf, text_rect)
    
    return None

# 游戏结束界面
def game_over_screen(score):
    over_active = True
    
    while over_active:
        dis.fill(menu_bg_color)
        
        # 显示游戏结束和分数
        title = title_font.render("GAME OVER", True, red)
        score_text = score_font.render(f"Final Score: {score}", True, white)
        dis.blit(title, [(display_width - title.get_width()) / 2, 80])
        dis.blit(score_text, [(display_width - score_text.get_width()) / 2, 150])
        
        # 绘制按钮
        button_width = 200
        button_height = 60
        button_x = display_width / 2 - button_width / 2
        
        play_again = draw_button("PLAY AGAIN", button_x, 220, button_width, button_height, 
                               light_green, green, white, False, "play_again")
        quit_game = draw_button("QUIT", button_x, 300, button_width, button_height, 
                              light_red, red, white, False, "quit")
        
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            # 处理键盘输入
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_c or event.key == pygame.K_RETURN:
                    return "play_again"
        
        # 处理按钮点击
        if play_again == "play_again":
            return "play_again"
        if quit_game == "quit":
            pygame.quit()
            sys.exit()
        
        clock.tick(15)

# 显示难度选择菜单
def difficulty_menu():
    menu_active = True
    selected_index = 1  # 默认选中中等难度 (0=Easy, 1=Medium, 2=Hard)
    difficulties = [EASY, MEDIUM, HARD]
    
    # 按钮尺寸和位置
    button_width = 200
    button_height = 60
    button_x = display_width / 2 - button_width / 2
    easy_y = 150
    medium_y = 230
    hard_y = 310
    button_positions = [easy_y, medium_y, hard_y]
    
    # 按钮颜色
    button_colors = [
        (light_green, green, white),  # Easy: 浅绿/绿
        (light_yellow, yellow, black),  # Medium: 浅黄/黄
        (light_red, red, white)  # Hard: 浅红/红
    ]
    
    while menu_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            # 处理键盘输入
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and selected_index > 0:
                    selected_index -= 1
                elif event.key == pygame.K_DOWN and selected_index < 2:
                    selected_index += 1
                elif event.key == pygame.K_RETURN:
                    return difficulties[selected_index]
                elif event.key == pygame.K_1:
                    selected_index = 0
                elif event.key == pygame.K_2:
                    selected_index = 1
                elif event.key == pygame.K_3:
                    selected_index = 2
        
        # 绘制背景
        dis.fill(menu_bg_color)
        
        # 绘制标题
        title = title_font.render("SNAKE GAME", True, white)
        subtitle = font_style.render("Select Difficulty", True, white)
        dis.blit(title, [(display_width - title.get_width()) / 2, 30])
        dis.blit(subtitle, [(display_width - subtitle.get_width()) / 2, 90])
        
        # 绘制难度选择按钮
        easy_action = draw_button("EASY", button_x, easy_y, button_width, button_height, 
                                button_colors[0][0], button_colors[0][1], button_colors[0][2], 
                                selected_index == 0, EASY)
        medium_action = draw_button("MEDIUM", button_x, medium_y, button_width, button_height, 
                                  button_colors[1][0], button_colors[1][1], button_colors[1][2], 
                                  selected_index == 1, MEDIUM)
        hard_action = draw_button("HARD", button_x, hard_y, button_width, button_height, 
                                button_colors[2][0], button_colors[2][1], button_colors[2][2], 
                                selected_index == 2, HARD)
        
        # 处理按钮点击
        if easy_action is not None:
            return easy_action
        if medium_action is not None:
            return medium_action
        if hard_action is not None:
            return hard_action
        
        pygame.display.update()
        clock.tick(15)

# 主游戏函数
def gameLoop(snake_speed):
    game_over = False
    game_close = False

    # 初始化蛇的位置 - 确保位置是网格的整数倍
    x1 = round(display_width / 2 / snake_block) * snake_block
    y1 = round(display_height / 2 / snake_block) * snake_block

    # 初始化蛇的移动方向
    x1_change = 0
    y1_change = 0

    # 初始化蛇的身体
    snake_List = []
    Length_of_snake = 1

    # 随机生成食物位置 - 确保位置是网格的整数倍
    foodx = round(random.randrange(0, display_width - snake_block) / snake_block) * snake_block
    foody = round(random.randrange(0, display_height - snake_block) / snake_block) * snake_block

    while not game_over:

        # 游戏结束时的处理
        if game_close:
            action = game_over_screen(Length_of_snake - 1)
            if action == "play_again":
                # 重新选择难度
                selected_speed = difficulty_menu()
                gameLoop(selected_speed)
            else:
                game_over = True

        # 处理键盘事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = snake_block
                    x1_change = 0

        # 检查是否撞墙
        if x1 >= display_width or x1 < 0 or y1 >= display_height or y1 < 0:
            game_close = True

        # 更新蛇的位置
        x1 += x1_change
        y1 += y1_change
        
        # 绘制黑色背景
        dis.fill(black)
        
        # 绘制网格
        draw_grid()
        
        # 绘制食物
        pygame.draw.rect(dis, red, [foodx, foody, snake_block, snake_block])
        
        # 更新蛇的身体
        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_List.append(snake_Head)
        
        # 如果蛇的长度超过了应有的长度，删除多余的部分
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        # 检查是否撞到自己
        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True

        # 绘制蛇和分数
        our_snake(snake_block, snake_List)
        your_score(Length_of_snake - 1)

        pygame.display.update()

        # 检查是否吃到食物
        if x1 == foodx and y1 == foody:
            # 随机生成新的食物位置 - 确保位置是网格的整数倍
            foodx = round(random.randrange(0, display_width - snake_block) / snake_block) * snake_block
            foody = round(random.randrange(0, display_height - snake_block) / snake_block) * snake_block
            Length_of_snake += 1

        # 控制游戏速度
        clock.tick(snake_speed)

    # 退出游戏
    pygame.quit()
    quit()

# 启动游戏
def main():
    # 显示难度选择菜单并获取选择的难度
    selected_speed = difficulty_menu()
    gameLoop(selected_speed)

# 启动游戏
if __name__ == "__main__":
    main()
