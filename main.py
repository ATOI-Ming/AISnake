#!/usr/bin/env python3
"""
AI控制的贪吃蛇游戏
作者: AI Assistant
"""

import pygame
import sys
import time
from snake_game import SnakeGame
from ai_controller import AIController
from config import game_config, get_text
from game_stats import game_stats
from audio_system import audio_system

def main():
    """主函数"""
    print("🐍 AI贪吃蛇游戏 - 完整增强版启动中...")
    print("=" * 70)
    print("🎮 游戏控制:")
    print("- 🤖 AI将自动控制贪吃蛇")
    print("- ⌨️  按 R 键重新开始游戏")
    print("- 🚪 按 ESC 或关闭窗口退出")
    print("- 🔊 按 M 键切换音效开关")
    print("- 📊 按 S 键显示详细统计")
    print("")
    print("✨ 视觉效果:")
    print("- 🌟 动态背景星空")
    print("- 🎆 粒子爆炸效果")
    print("- 🌈 渐变色蛇身")
    print("- 💫 食物脉冲发光")
    print("- 👁️  蛇头眼睛动画")
    print("- 🔥 移动轨迹效果")
    print("")
    print("🎵 音效系统:")
    print("- 🍎 吃食物音效")
    print("- 💥 游戏结束音效")
    print("- 🏆 成就解锁音效")
    print("- 🎼 环境背景音乐")
    print("")
    print("📈 统计功能:")
    print("- 📊 实时游戏统计")
    print("- 🏆 成就系统")
    print("- 📝 历史记录")
    print("- ⏱️  游戏时间追踪")
    print("=" * 70)
    
    # 从配置文件获取游戏设置
    WINDOW_WIDTH = game_config.get("window.width", 800)
    WINDOW_HEIGHT = game_config.get("window.height", 600)
    CELL_SIZE = game_config.get("window.cell_size", 20)
    FPS = game_config.get("performance.fps", 10)

    try:
        # 初始化音效系统
        if game_config.get("audio.enable_sound", True):
            audio_system.play_background_music()

        # 创建游戏实例
        game = SnakeGame()  # 使用配置文件中的默认值
        ai_controller = AIController(game)

        print(f"游戏窗口大小: {WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        print(f"网格大小: {game.grid_width}x{game.grid_height}")
        print(f"游戏速度: {FPS} FPS")
        print("游戏开始!")

        # 显示统计信息
        stats = game_stats.get_all_time_stats()
        if stats["total_games"] > 0:
            print(f"历史统计: 总游戏{stats['total_games']}次, 最高分{stats['highest_score']}, 平均分{stats['average_score']:.1f}")
        
        # 游戏主循环
        running = True
        auto_restart_delay = game_config.get("performance.auto_restart_delay", 3.0)
        game_over_time = None

        while running:
            # 处理事件
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key == pygame.K_r and game.game_over:
                        game.reset_game()
                        game_over_time = None
                        print(f"游戏重新开始! 上次得分: {game.score}")
                    elif event.key == pygame.K_m:  # 切换音效
                        audio_system.toggle_sound()
                        print(f"音效: {'开启' if audio_system.enabled else '关闭'}")
                    elif event.key == pygame.K_s:  # 显示统计
                        stats = game_stats.get_all_time_stats()
                        session_stats = game_stats.get_session_stats()
                        print(f"\n=== 游戏统计 ===")
                        print(f"本次会话: {session_stats['games_played']}局, 最佳{session_stats['best_score']}分")
                        print(f"历史记录: {stats['total_games']}局, 最高{stats['highest_score']}分, 平均{stats['average_score']:.1f}分")
                        print(f"总游戏时间: {stats['total_play_time']/60:.1f}分钟")
                        print("================\n")
            
            if not game.game_over:
                # AI控制
                best_direction = ai_controller.get_best_direction()
                game.move(best_direction)
                
                # 检查游戏是否结束
                if game.game_over:
                    game_over_time = time.time()
                    print(f"游戏结束! 最终得分: {game.score}")
                    print(f"蛇的长度: {len(game.snake)}")
                    print(f"移动次数: {game.move_count}")

                    # 检查成就
                    achievements = game_stats.check_achievements(game.score, len(game.snake))
                    for achievement in achievements:
                        print(f"🏆 {achievement}")
                        audio_system.play_achievement_sound()

                    print(f"{auto_restart_delay}秒后自动重新开始...")
            else:
                # 自动重启逻辑
                if game_over_time and time.time() - game_over_time > auto_restart_delay:
                    old_score = game.score
                    game.reset_game()
                    game_over_time = None
                    print(f"自动重新开始! 上次得分: {old_score}")
            
            # 绘制游戏
            game.draw()
            
            # 控制帧率
            game.clock.tick(FPS)
        
        print("游戏退出")
        
    except Exception as e:
        print(f"游戏运行出错: {e}")
        import traceback
        traceback.print_exc()
    finally:
        pygame.quit()
        sys.exit()

def test_ai():
    """测试AI控制器"""
    print("🧪 测试AI控制器...")
    
    game = SnakeGame(400, 400, 20)
    ai_controller = AIController(game)
    
    # 测试几步移动
    for i in range(10):
        if game.game_over:
            break
            
        direction = ai_controller.get_best_direction()
        print(f"步骤 {i+1}: 蛇头位置 {game.get_head_position()}, "
              f"食物位置 {game.food}, 选择方向 {direction.name}")
        
        game.move(direction)
    
    print(f"测试完成，得分: {game.score}")
    pygame.quit()

if __name__ == "__main__":
    # 可以通过命令行参数选择测试模式
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        test_ai()
    else:
        main()
