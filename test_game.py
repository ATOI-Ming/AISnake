#!/usr/bin/env python3
"""
游戏功能测试脚本
用于验证所有模块是否正常工作
"""

import sys
import traceback

def test_imports():
    """测试所有模块导入"""
    print("🧪 测试模块导入...")
    
    try:
        print("  - 测试配置系统...")
        from config import game_config, get_text, get_theme_colors
        print(f"    ✅ 配置系统正常，当前语言: {game_config.get('language.current', 'zh_CN')}")
        
        print("  - 测试统计系统...")
        from game_stats import game_stats
        print("    ✅ 统计系统正常")
        
        print("  - 测试音效系统...")
        from audio_system import audio_system
        print(f"    ✅ 音效系统正常，状态: {'启用' if audio_system.enabled else '禁用'}")
        
        print("  - 测试游戏核心...")
        from snake_game import SnakeGame
        print("    ✅ 游戏核心正常")
        
        print("  - 测试AI控制器...")
        from ai_controller import AIController
        print("    ✅ AI控制器正常")
        
        return True
        
    except Exception as e:
        print(f"    ❌ 导入失败: {e}")
        traceback.print_exc()
        return False

def test_config():
    """测试配置系统"""
    print("\n⚙️ 测试配置系统...")
    
    try:
        from config import game_config
        
        # 测试配置读取
        width = game_config.get("window.width", 800)
        height = game_config.get("window.height", 600)
        fps = game_config.get("performance.fps", 10)
        
        print(f"  - 窗口大小: {width}x{height}")
        print(f"  - 游戏速度: {fps} FPS")
        print(f"  - AI算法: {game_config.get('ai.algorithm', 'astar')}")
        print(f"  - 颜色主题: {game_config.get('colors.theme', 'default')}")
        
        # 测试配置保存
        game_config.save_config()
        print("  ✅ 配置系统测试通过")
        return True
        
    except Exception as e:
        print(f"  ❌ 配置系统测试失败: {e}")
        return False

def test_game_creation():
    """测试游戏创建"""
    print("\n🎮 测试游戏创建...")
    
    try:
        from snake_game import SnakeGame
        from ai_controller import AIController
        
        # 创建游戏实例
        game = SnakeGame(400, 400, 20)
        print(f"  - 游戏窗口: {game.width}x{game.height}")
        print(f"  - 网格大小: {game.grid_width}x{game.grid_height}")
        print(f"  - 蛇初始位置: {game.get_head_position()}")
        print(f"  - 食物位置: {game.food}")
        
        # 创建AI控制器
        ai = AIController(game)
        print(f"  - AI算法: {ai.algorithm}")
        
        # 测试几步移动
        for i in range(3):
            direction = ai.get_best_direction()
            success = game.move(direction)
            print(f"  - 步骤{i+1}: 方向{direction.name}, 成功: {success}")
            if not success:
                break
        
        print(f"  - 最终得分: {game.score}")
        print("  ✅ 游戏创建测试通过")
        
        # 清理pygame
        import pygame
        pygame.quit()
        return True
        
    except Exception as e:
        print(f"  ❌ 游戏创建测试失败: {e}")
        traceback.print_exc()
        return False

def test_audio():
    """测试音效系统"""
    print("\n🎵 测试音效系统...")
    
    try:
        from audio_system import audio_system
        
        print(f"  - 音效状态: {'启用' if audio_system.enabled else '禁用'}")
        print(f"  - 主音量: {audio_system.master_volume}")
        print(f"  - 音效音量: {audio_system.sfx_volume}")
        
        if audio_system.enabled:
            print("  - 测试音效播放...")
            audio_system.play_eat_sound()
            print("    ✅ 吃食物音效")
            
            audio_system.play_game_over_sound()
            print("    ✅ 游戏结束音效")
        
        print("  ✅ 音效系统测试通过")
        return True
        
    except Exception as e:
        print(f"  ❌ 音效系统测试失败: {e}")
        return False

def test_stats():
    """测试统计系统"""
    print("\n📊 测试统计系统...")
    
    try:
        from game_stats import game_stats
        
        # 测试统计功能
        stats = game_stats.get_all_time_stats()
        print(f"  - 总游戏次数: {stats['total_games']}")
        print(f"  - 最高分: {stats['highest_score']}")
        print(f"  - 平均分: {stats['average_score']:.1f}")
        
        # 测试会话统计
        session = game_stats.get_session_stats()
        print(f"  - 本次会话游戏: {session['games_played']}")
        print(f"  - 本次会话最佳: {session['best_score']}")
        
        print("  ✅ 统计系统测试通过")
        return True
        
    except Exception as e:
        print(f"  ❌ 统计系统测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("🚀 AI贪吃蛇游戏 - 功能测试")
    print("=" * 50)
    
    tests = [
        ("模块导入", test_imports),
        ("配置系统", test_config),
        ("游戏创建", test_game_creation),
        ("音效系统", test_audio),
        ("统计系统", test_stats)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
        except Exception as e:
            print(f"❌ {test_name}测试出现异常: {e}")
    
    print("\n" + "=" * 50)
    print(f"📋 测试结果: {passed}/{total} 通过")
    
    if passed == total:
        print("🎉 所有测试通过！游戏可以正常运行。")
        print("\n🎮 启动游戏:")
        print("  python main.py          # 开始游戏")
        print("  python main.py test     # AI测试")
        print("  python launcher.py      # 启动器")
    else:
        print("⚠️ 部分测试失败，请检查错误信息。")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
