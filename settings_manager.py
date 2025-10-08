#!/usr/bin/env python3
"""
设置管理器
提供游戏设置的图形界面管理
"""

import pygame
import sys
from typing import Dict, Any, List, Tuple
from config import game_config, get_text, COLOR_THEMES
from audio_system import audio_system

class SettingsManager:
    """设置管理器类"""
    
    def __init__(self, width: int = 600, height: int = 500):
        self.width = width
        self.height = height
        self.running = False
        
        # 颜色定义
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.GRAY = (128, 128, 128)
        self.LIGHT_GRAY = (200, 200, 200)
        self.BLUE = (0, 100, 200)
        self.GREEN = (0, 150, 0)
        self.RED = (200, 0, 0)
        
        # 设置项
        self.settings = [
            {
                "name": "游戏速度",
                "key": "performance.fps",
                "type": "slider",
                "min": 5,
                "max": 30,
                "step": 1
            },
            {
                "name": "窗口宽度",
                "key": "window.width",
                "type": "slider",
                "min": 600,
                "max": 1200,
                "step": 50
            },
            {
                "name": "窗口高度",
                "key": "window.height",
                "type": "slider",
                "min": 400,
                "max": 800,
                "step": 50
            },
            {
                "name": "格子大小",
                "key": "window.cell_size",
                "type": "slider",
                "min": 15,
                "max": 30,
                "step": 5
            },
            {
                "name": "粒子效果",
                "key": "visual.enable_particles",
                "type": "toggle"
            },
            {
                "name": "轨迹效果",
                "key": "visual.enable_trail",
                "type": "toggle"
            },
            {
                "name": "发光效果",
                "key": "visual.enable_glow",
                "type": "toggle"
            },
            {
                "name": "背景星空",
                "key": "visual.enable_stars",
                "type": "toggle"
            },
            {
                "name": "网格显示",
                "key": "visual.enable_grid",
                "type": "toggle"
            },
            {
                "name": "音效开关",
                "key": "audio.enable_sound",
                "type": "toggle"
            },
            {
                "name": "主音量",
                "key": "audio.master_volume",
                "type": "slider",
                "min": 0.0,
                "max": 1.0,
                "step": 0.1
            },
            {
                "name": "颜色主题",
                "key": "colors.theme",
                "type": "dropdown",
                "options": list(COLOR_THEMES.keys())
            },
            {
                "name": "语言",
                "key": "language.current",
                "type": "dropdown",
                "options": ["zh_CN", "en_US"]
            }
        ]
        
        self.selected_item = 0
        self.scroll_offset = 0
        
    def init_pygame(self):
        """初始化pygame"""
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("游戏设置")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 24)
        self.title_font = pygame.font.Font(None, 36)
    
    def draw_slider(self, setting: Dict, rect: pygame.Rect, value: Any):
        """绘制滑块"""
        # 滑块轨道
        track_rect = pygame.Rect(rect.x + 150, rect.y + 10, 200, 10)
        pygame.draw.rect(self.screen, self.GRAY, track_rect)
        
        # 计算滑块位置
        min_val = setting["min"]
        max_val = setting["max"]
        ratio = (value - min_val) / (max_val - min_val)
        slider_x = track_rect.x + int(ratio * track_rect.width)
        
        # 绘制滑块
        slider_rect = pygame.Rect(slider_x - 5, track_rect.y - 5, 10, 20)
        pygame.draw.rect(self.screen, self.BLUE, slider_rect)
        
        # 显示数值
        value_text = self.font.render(str(value), True, self.BLACK)
        self.screen.blit(value_text, (track_rect.right + 10, rect.y + 5))
    
    def draw_toggle(self, setting: Dict, rect: pygame.Rect, value: bool):
        """绘制开关"""
        toggle_rect = pygame.Rect(rect.x + 150, rect.y + 5, 50, 20)
        color = self.GREEN if value else self.RED
        pygame.draw.rect(self.screen, color, toggle_rect)
        
        # 开关文本
        text = "ON" if value else "OFF"
        toggle_text = self.font.render(text, True, self.WHITE)
        text_rect = toggle_text.get_rect(center=toggle_rect.center)
        self.screen.blit(toggle_text, text_rect)
    
    def draw_dropdown(self, setting: Dict, rect: pygame.Rect, value: str):
        """绘制下拉框"""
        dropdown_rect = pygame.Rect(rect.x + 150, rect.y + 5, 150, 20)
        pygame.draw.rect(self.screen, self.WHITE, dropdown_rect)
        pygame.draw.rect(self.screen, self.BLACK, dropdown_rect, 2)
        
        # 当前值
        value_text = self.font.render(str(value), True, self.BLACK)
        self.screen.blit(value_text, (dropdown_rect.x + 5, dropdown_rect.y + 2))
    
    def draw(self):
        """绘制设置界面"""
        self.screen.fill(self.WHITE)
        
        # 标题
        title_text = self.title_font.render("游戏设置", True, self.BLACK)
        title_rect = title_text.get_rect(center=(self.width // 2, 30))
        self.screen.blit(title_text, title_rect)
        
        # 设置项
        y_start = 80
        item_height = 40
        visible_items = (self.height - y_start - 50) // item_height
        
        for i, setting in enumerate(self.settings[self.scroll_offset:self.scroll_offset + visible_items]):
            actual_index = i + self.scroll_offset
            y = y_start + i * item_height
            rect = pygame.Rect(20, y, self.width - 40, item_height - 5)
            
            # 高亮选中项
            if actual_index == self.selected_item:
                pygame.draw.rect(self.screen, self.LIGHT_GRAY, rect)
            
            # 设置名称
            name_text = self.font.render(setting["name"], True, self.BLACK)
            self.screen.blit(name_text, (rect.x + 10, rect.y + 10))
            
            # 获取当前值
            current_value = game_config.get(setting["key"])
            
            # 根据类型绘制控件
            if setting["type"] == "slider":
                self.draw_slider(setting, rect, current_value)
            elif setting["type"] == "toggle":
                self.draw_toggle(setting, rect, current_value)
            elif setting["type"] == "dropdown":
                self.draw_dropdown(setting, rect, current_value)
        
        # 底部按钮
        button_y = self.height - 40
        
        # 保存按钮
        save_rect = pygame.Rect(self.width // 2 - 100, button_y, 80, 30)
        pygame.draw.rect(self.screen, self.GREEN, save_rect)
        save_text = self.font.render("保存", True, self.WHITE)
        save_text_rect = save_text.get_rect(center=save_rect.center)
        self.screen.blit(save_text, save_text_rect)
        
        # 取消按钮
        cancel_rect = pygame.Rect(self.width // 2 + 20, button_y, 80, 30)
        pygame.draw.rect(self.screen, self.RED, cancel_rect)
        cancel_text = self.font.render("取消", True, self.WHITE)
        cancel_text_rect = cancel_text.get_rect(center=cancel_rect.center)
        self.screen.blit(cancel_text, cancel_text_rect)
        
        # 重置按钮
        reset_rect = pygame.Rect(20, button_y, 80, 30)
        pygame.draw.rect(self.screen, self.GRAY, reset_rect)
        reset_text = self.font.render("重置", True, self.WHITE)
        reset_text_rect = reset_text.get_rect(center=reset_rect.center)
        self.screen.blit(reset_text, reset_text_rect)
        
        pygame.display.flip()
    
    def handle_input(self, setting: Dict, direction: int):
        """处理输入"""
        current_value = game_config.get(setting["key"])
        
        if setting["type"] == "slider":
            step = setting["step"]
            new_value = current_value + (step * direction)
            new_value = max(setting["min"], min(setting["max"], new_value))
            game_config.set(setting["key"], new_value)
            
            # 实时应用音量设置
            if "volume" in setting["key"]:
                if setting["key"] == "audio.master_volume":
                    audio_system.set_master_volume(new_value)
                elif setting["key"] == "audio.sfx_volume":
                    audio_system.set_sfx_volume(new_value)
                elif setting["key"] == "audio.music_volume":
                    audio_system.set_music_volume(new_value)
        
        elif setting["type"] == "toggle":
            new_value = not current_value
            game_config.set(setting["key"], new_value)
            
            # 实时应用音效设置
            if setting["key"] == "audio.enable_sound":
                audio_system.enabled = new_value
        
        elif setting["type"] == "dropdown":
            options = setting["options"]
            current_index = options.index(current_value) if current_value in options else 0
            new_index = (current_index + direction) % len(options)
            game_config.set(setting["key"], options[new_index])
    
    def run(self):
        """运行设置界面"""
        self.init_pygame()
        self.running = True
        
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                    
                    elif event.key == pygame.K_UP:
                        self.selected_item = max(0, self.selected_item - 1)
                        if self.selected_item < self.scroll_offset:
                            self.scroll_offset = self.selected_item
                    
                    elif event.key == pygame.K_DOWN:
                        self.selected_item = min(len(self.settings) - 1, self.selected_item + 1)
                        visible_items = (self.height - 80 - 50) // 40
                        if self.selected_item >= self.scroll_offset + visible_items:
                            self.scroll_offset = self.selected_item - visible_items + 1
                    
                    elif event.key == pygame.K_LEFT:
                        self.handle_input(self.settings[self.selected_item], -1)
                    
                    elif event.key == pygame.K_RIGHT:
                        self.handle_input(self.settings[self.selected_item], 1)
                    
                    elif event.key == pygame.K_RETURN:
                        if self.settings[self.selected_item]["type"] == "toggle":
                            self.handle_input(self.settings[self.selected_item], 1)
                    
                    elif event.key == pygame.K_r:  # 重置设置
                        game_config.reset_to_default()
                        print("设置已重置为默认值")
            
            self.draw()
            self.clock.tick(60)
        
        pygame.quit()

def main():
    """运行设置管理器"""
    settings = SettingsManager()
    settings.run()

if __name__ == "__main__":
    main()
