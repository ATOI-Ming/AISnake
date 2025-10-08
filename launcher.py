#!/usr/bin/env python3
"""
AI贪吃蛇游戏启动器
提供多种启动选项和功能
"""

import sys
import os
import subprocess
from config import game_config, get_text
from game_stats import game_stats

def print_banner():
    """打印游戏横幅"""
    print("=" * 80)
    print("🐍 AI贪吃蛇游戏 - 完整增强版")
    print("   Enhanced AI Snake Game with Visual Effects")
    print("=" * 80)
    print()

def print_menu():
    """打印主菜单"""
    print("📋 请选择功能:")
    print("1. 🎮 开始游戏 (Start Game)")
    print("2. 🧪 测试AI控制器 (Test AI Controller)")
    print("3. 🎨 视觉效果演示 (Visual Effects Demo)")
    print("4. ⚙️  游戏设置 (Game Settings)")
    print("5. 📊 查看统计 (View Statistics)")
    print("6. 🏆 查看成就 (View Achievements)")
    print("7. 🔧 重置数据 (Reset Data)")
    print("8. ℹ️  关于游戏 (About)")
    print("9. 🚪 退出 (Exit)")
    print()

def show_statistics():
    """显示游戏统计"""
    print("\n📊 游戏统计信息")
    print("=" * 50)
    
    stats = game_stats.get_all_time_stats()
    session_stats = game_stats.get_session_stats()
    
    print(f"🎮 总游戏次数: {stats['total_games']}")
    print(f"🏆 最高分数: {stats['highest_score']}")
    print(f"📈 平均分数: {stats['average_score']:.1f}")
    print(f"🍎 总食物数: {stats['total_food_eaten']}")
    print(f"⏱️  总游戏时间: {stats['total_play_time']/60:.1f} 分钟")
    
    print(f"\n📅 本次会话:")
    print(f"   游戏次数: {session_stats['games_played']}")
    print(f"   最佳分数: {session_stats['best_score']}")
    print(f"   平均分数: {session_stats['average_score']:.1f}")
    
    # 显示最近的分数
    recent_scores = game_stats.get_recent_scores(5)
    if recent_scores:
        print(f"\n🕒 最近5次游戏:")
        for i, record in enumerate(recent_scores, 1):
            print(f"   {i}. 分数: {record['score']}, 长度: {record['length']}, 时间: {record['duration']:.1f}s")
    
    # 显示最高分记录
    best_scores = game_stats.get_best_scores(3)
    if best_scores:
        print(f"\n🥇 最高分记录:")
        for i, record in enumerate(best_scores, 1):
            print(f"   {i}. 分数: {record['score']}, 长度: {record['length']}, 时间: {record['duration']:.1f}s")
    
    print("=" * 50)

def show_achievements():
    """显示成就"""
    print("\n🏆 成就系统")
    print("=" * 50)
    
    stats = game_stats.get_all_time_stats()
    achievements = stats.get('achievements', [])
    
    if achievements:
        print("已解锁的成就:")
        for achievement in achievements:
            if achievement.startswith('score_'):
                score = achievement.split('_')[1]
                print(f"🎯 得分达人 - 单局得分{score}分")
            elif achievement.startswith('length_'):
                length = achievement.split('_')[1]
                print(f"🐍 长蛇传说 - 蛇长度达到{length}")
            elif achievement.startswith('games_'):
                games = achievement.split('_')[1]
                print(f"🎮 游戏达人 - 游戏{games}次")
        
        print(f"\n总计解锁: {len(achievements)} 个成就")
    else:
        print("暂无解锁的成就，继续努力吧！")
    
    print("\n可解锁的成就:")
    print("🎯 得分系列: 10, 25, 50, 100, 200, 500分")
    print("🐍 长度系列: 10, 20, 50, 100格")
    print("🎮 游戏系列: 10, 50, 100, 500, 1000次")
    print("=" * 50)

def show_about():
    """显示关于信息"""
    print("\nℹ️  关于AI贪吃蛇游戏")
    print("=" * 50)
    print("🎮 游戏名称: AI贪吃蛇 - 完整增强版")
    print("🤖 AI算法: A*寻路, 贪心策略, 防御策略, 随机策略")
    print("🎨 视觉效果: 粒子系统, 发光效果, 动态背景, 轨迹追踪")
    print("🎵 音效系统: 程序化音效生成, 背景音乐")
    print("📊 统计系统: 游戏记录, 成就系统, 历史追踪")
    print("⚙️  配置系统: 可自定义设置, 多主题支持")
    print("🌍 多语言: 中文, English")
    print()
    print("🛠️  技术栈:")
    print("   - Python 3.12+")
    print("   - Pygame 2.5+")
    print("   - NumPy (音效生成)")
    print("   - JSON (配置和数据存储)")
    print()
    print("📝 开发者: AI Assistant")
    print("📅 版本: 2.0 Enhanced Edition")
    print("=" * 50)

def reset_data():
    """重置游戏数据"""
    print("\n🔧 重置游戏数据")
    print("=" * 50)
    print("⚠️  警告: 此操作将删除所有游戏数据，包括:")
    print("   - 游戏统计记录")
    print("   - 成就进度")
    print("   - 历史分数")
    print("   - 游戏设置")
    print()
    
    confirm = input("确认重置所有数据? (输入 'YES' 确认): ").strip()
    if confirm == 'YES':
        try:
            # 重置统计数据
            game_stats.reset_stats()
            
            # 重置配置
            game_config.reset_to_default()
            
            print("✅ 数据重置完成!")
        except Exception as e:
            print(f"❌ 重置失败: {e}")
    else:
        print("❌ 重置已取消")
    
    print("=" * 50)

def run_game():
    """运行主游戏"""
    try:
        subprocess.run([sys.executable, "main.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ 游戏启动失败: {e}")
    except FileNotFoundError:
        print("❌ 找不到main.py文件")

def run_test():
    """运行AI测试"""
    try:
        subprocess.run([sys.executable, "main.py", "test"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ 测试启动失败: {e}")
    except FileNotFoundError:
        print("❌ 找不到main.py文件")

def run_demo():
    """运行视觉演示"""
    try:
        subprocess.run([sys.executable, "visual_demo.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ 演示启动失败: {e}")
    except FileNotFoundError:
        print("❌ 找不到visual_demo.py文件")

def run_settings():
    """运行设置管理器"""
    try:
        subprocess.run([sys.executable, "settings_manager.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ 设置启动失败: {e}")
    except FileNotFoundError:
        print("❌ 找不到settings_manager.py文件")

def main():
    """主函数"""
    print_banner()
    
    # 显示当前配置信息
    print(f"🎮 当前配置:")
    print(f"   窗口大小: {game_config.get('window.width')}x{game_config.get('window.height')}")
    print(f"   游戏速度: {game_config.get('performance.fps')} FPS")
    print(f"   AI算法: {game_config.get('ai.algorithm')}")
    print(f"   颜色主题: {game_config.get('colors.theme')}")
    print(f"   语言: {game_config.get('language.current')}")
    print()
    
    while True:
        print_menu()
        
        try:
            choice = input("请输入选择 (1-9): ").strip()
            
            if choice == '1':
                print("🎮 启动游戏...")
                run_game()
            elif choice == '2':
                print("🧪 启动AI测试...")
                run_test()
            elif choice == '3':
                print("🎨 启动视觉演示...")
                run_demo()
            elif choice == '4':
                print("⚙️ 启动设置管理器...")
                run_settings()
            elif choice == '5':
                show_statistics()
            elif choice == '6':
                show_achievements()
            elif choice == '7':
                reset_data()
            elif choice == '8':
                show_about()
            elif choice == '9':
                print("👋 感谢游玩! Goodbye!")
                break
            else:
                print("❌ 无效选择，请输入1-9")
            
            if choice in ['1', '2', '3', '4']:
                print()  # 添加空行分隔
                
        except KeyboardInterrupt:
            print("\n👋 感谢游玩! Goodbye!")
            break
        except Exception as e:
            print(f"❌ 发生错误: {e}")

if __name__ == "__main__":
    main()
