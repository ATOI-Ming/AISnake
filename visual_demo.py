#!/usr/bin/env python3
"""
AI贪吃蛇视觉效果演示
展示各种视觉效果的独立演示
"""

import pygame
import sys
import time
import math
import random
from snake_game import SnakeGame
from ai_controller import AIController

def demo_particles():
    """演示粒子效果"""
    print("🎆 粒子效果演示")
    game = SnakeGame(600, 400, 20)
    
    # 手动创建一些粒子效果
    for i in range(5):
        x = random.randint(5, game.grid_width - 5)
        y = random.randint(5, game.grid_height - 5)
        game.create_food_particles((x, y))
        time.sleep(0.5)
        
        # 绘制几帧来显示粒子
        for _ in range(30):
            game.draw()
            game.clock.tick(60)
            
            # 处理退出事件
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
    
    pygame.quit()

def demo_snake_growth():
    """演示蛇的成长过程"""
    print("🐍 蛇成长演示")
    game = SnakeGame(800, 600, 25)
    ai = AIController(game)
    
    # 让AI玩一会儿来展示成长
    start_time = time.time()
    while time.time() - start_time < 30:  # 运行30秒
        if game.game_over:
            game.reset_game()
        
        direction = ai.get_best_direction()
        game.move(direction)
        game.draw()
        game.clock.tick(15)  # 稍微快一点
        
        # 处理事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    return
    
    pygame.quit()

def demo_visual_effects():
    """演示所有视觉效果"""
    print("✨ 完整视觉效果演示")
    game = SnakeGame(1000, 700, 20)
    ai = AIController(game)
    
    print("演示说明:")
    print("- 观察背景星空动画")
    print("- 注意蛇头的发光效果和眼睛")
    print("- 看蛇身的渐变色彩")
    print("- 食物的脉冲发光效果")
    print("- 吃食物时的粒子爆炸")
    print("- 游戏结束时的爆炸效果")
    print("- 按ESC退出演示")
    
    demo_time = 0
    while demo_time < 60:  # 运行1分钟
        dt = game.clock.tick(12) / 1000.0
        demo_time += dt
        
        if not game.game_over:
            direction = ai.get_best_direction()
            game.move(direction)
        else:
            # 游戏结束后等待3秒重新开始
            time.sleep(3)
            game.reset_game()
        
        game.draw()
        
        # 处理事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    return
    
    pygame.quit()

def interactive_demo():
    """交互式演示"""
    print("🎮 交互式视觉效果演示")
    print("控制说明:")
    print("- 1: 创建食物粒子效果")
    print("- 2: 创建爆炸效果")
    print("- 3: 重置游戏")
    print("- SPACE: 暂停/继续")
    print("- ESC: 退出")
    
    game = SnakeGame(800, 600, 20)
    ai = AIController(game)
    paused = False
    
    while True:
        dt = game.clock.tick(10) / 1000.0
        
        # 处理事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    return
                elif event.key == pygame.K_1:
                    # 创建食物粒子效果
                    pos = (random.randint(2, game.grid_width-2), 
                          random.randint(2, game.grid_height-2))
                    game.create_food_particles(pos)
                elif event.key == pygame.K_2:
                    # 创建爆炸效果
                    pos = (random.randint(2, game.grid_width-2), 
                          random.randint(2, game.grid_height-2))
                    game.create_explosion_particles(pos)
                elif event.key == pygame.K_3:
                    game.reset_game()
                elif event.key == pygame.K_SPACE:
                    paused = not paused
        
        # 游戏逻辑
        if not paused and not game.game_over:
            direction = ai.get_best_direction()
            game.move(direction)
        elif game.game_over:
            # 自动重启
            time.sleep(2)
            game.reset_game()
        
        # 绘制
        game.draw()
        
        # 显示控制提示
        if paused:
            pause_text = game.font.render("暂停中 - 按SPACE继续", True, game.YELLOW)
            pause_rect = pause_text.get_rect(center=(game.width//2, 50))
            game.screen.blit(pause_text, pause_rect)
            pygame.display.flip()

def main():
    """主演示菜单"""
    print("🎨 AI贪吃蛇视觉效果演示系统")
    print("=" * 50)
    print("选择演示模式:")
    print("1. 粒子效果演示")
    print("2. 蛇成长演示")
    print("3. 完整视觉效果演示")
    print("4. 交互式演示")
    print("5. 退出")
    print("=" * 50)
    
    while True:
        try:
            choice = input("请输入选择 (1-5): ").strip()
            
            if choice == '1':
                demo_particles()
                break
            elif choice == '2':
                demo_snake_growth()
                break
            elif choice == '3':
                demo_visual_effects()
                break
            elif choice == '4':
                interactive_demo()
                break
            elif choice == '5':
                print("退出演示系统")
                break
            else:
                print("无效选择，请输入1-5")
        except KeyboardInterrupt:
            print("\n退出演示系统")
            break
        except Exception as e:
            print(f"演示出错: {e}")
            break

if __name__ == "__main__":
    main()
