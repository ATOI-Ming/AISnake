#!/usr/bin/env python3
"""
音效系统
提供游戏音效和背景音乐功能
"""

import pygame
import random
import numpy as np
from typing import Dict, Optional
from config import game_config

class AudioSystem:
    """音效系统管理类"""
    
    def __init__(self):
        self.enabled = game_config.get("audio.enable_sound", True)
        self.master_volume = game_config.get("audio.master_volume", 0.7)
        self.sfx_volume = game_config.get("audio.sfx_volume", 0.8)
        self.music_volume = game_config.get("audio.music_volume", 0.5)
        
        self.sounds = {}
        self.music_playing = False
        
        if self.enabled:
            try:
                pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
                self.generate_sounds()
            except pygame.error as e:
                print(f"音频初始化失败: {e}")
                self.enabled = False
    
    def generate_sounds(self):
        """生成程序化音效"""
        if not self.enabled:
            return
        
        try:
            # 生成吃食物音效
            self.sounds['eat'] = self.generate_eat_sound()
            
            # 生成游戏结束音效
            self.sounds['game_over'] = self.generate_game_over_sound()
            
            # 生成移动音效（可选）
            self.sounds['move'] = self.generate_move_sound()
            
            # 生成成就音效
            self.sounds['achievement'] = self.generate_achievement_sound()
            
            print("音效生成完成")
        except Exception as e:
            print(f"音效生成失败: {e}")
            self.enabled = False
    
    def generate_eat_sound(self) -> pygame.mixer.Sound:
        """生成吃食物的音效"""
        duration = 0.2
        sample_rate = 22050
        frames = int(duration * sample_rate)
        
        # 生成一个愉快的音调
        frequency = 800
        wave = np.sin(2 * np.pi * frequency * np.linspace(0, duration, frames))
        
        # 添加谐波
        wave += 0.3 * np.sin(2 * np.pi * frequency * 2 * np.linspace(0, duration, frames))
        wave += 0.1 * np.sin(2 * np.pi * frequency * 3 * np.linspace(0, duration, frames))
        
        # 添加包络
        envelope = np.exp(-np.linspace(0, 5, frames))
        wave *= envelope
        
        # 转换为pygame音频格式
        wave = (wave * 32767).astype(np.int16)
        stereo_wave = np.array([wave, wave]).T
        stereo_wave = np.ascontiguousarray(stereo_wave)

        return pygame.sndarray.make_sound(stereo_wave)
    
    def generate_game_over_sound(self) -> pygame.mixer.Sound:
        """生成游戏结束音效"""
        duration = 1.0
        sample_rate = 22050
        frames = int(duration * sample_rate)
        
        # 生成下降音调
        start_freq = 400
        end_freq = 200
        frequencies = np.linspace(start_freq, end_freq, frames)
        
        wave = np.sin(2 * np.pi * frequencies * np.linspace(0, duration, frames))
        
        # 添加噪音效果
        noise = np.random.normal(0, 0.1, frames)
        wave += noise
        
        # 添加包络
        envelope = np.exp(-np.linspace(0, 2, frames))
        wave *= envelope
        
        # 转换为pygame音频格式
        wave = (wave * 32767 * 0.5).astype(np.int16)
        stereo_wave = np.array([wave, wave]).T
        stereo_wave = np.ascontiguousarray(stereo_wave)

        return pygame.sndarray.make_sound(stereo_wave)
    
    def generate_move_sound(self) -> pygame.mixer.Sound:
        """生成移动音效（轻微的滴答声）"""
        duration = 0.05
        sample_rate = 22050
        frames = int(duration * sample_rate)
        
        # 生成短促的点击声
        frequency = 1000
        wave = np.sin(2 * np.pi * frequency * np.linspace(0, duration, frames))
        
        # 快速衰减
        envelope = np.exp(-np.linspace(0, 20, frames))
        wave *= envelope
        
        # 转换为pygame音频格式
        wave = (wave * 32767 * 0.3).astype(np.int16)
        stereo_wave = np.array([wave, wave]).T
        stereo_wave = np.ascontiguousarray(stereo_wave)

        return pygame.sndarray.make_sound(stereo_wave)
    
    def generate_achievement_sound(self) -> pygame.mixer.Sound:
        """生成成就音效"""
        duration = 0.8
        sample_rate = 22050
        frames = int(duration * sample_rate)
        
        # 生成上升音调序列
        notes = [523, 659, 784, 1047]  # C, E, G, C (高八度)
        wave = np.zeros(frames)
        
        note_duration = frames // len(notes)
        for i, freq in enumerate(notes):
            start = i * note_duration
            end = min((i + 1) * note_duration, frames)
            note_frames = end - start
            
            note_wave = np.sin(2 * np.pi * freq * np.linspace(0, note_duration/sample_rate, note_frames))
            envelope = np.exp(-np.linspace(0, 3, note_frames))
            wave[start:end] = note_wave * envelope
        
        # 转换为pygame音频格式
        wave = (wave * 32767 * 0.6).astype(np.int16)
        stereo_wave = np.array([wave, wave]).T
        stereo_wave = np.ascontiguousarray(stereo_wave)

        return pygame.sndarray.make_sound(stereo_wave)
    
    def play_sound(self, sound_name: str, volume: float = 1.0):
        """播放音效"""
        if not self.enabled or sound_name not in self.sounds:
            return
        
        try:
            sound = self.sounds[sound_name]
            sound.set_volume(volume * self.sfx_volume * self.master_volume)
            sound.play()
        except Exception as e:
            print(f"播放音效失败 {sound_name}: {e}")
    
    def play_eat_sound(self):
        """播放吃食物音效"""
        self.play_sound('eat', random.uniform(0.8, 1.0))
    
    def play_game_over_sound(self):
        """播放游戏结束音效"""
        self.play_sound('game_over', 0.8)
    
    def play_move_sound(self):
        """播放移动音效"""
        if random.random() < 0.1:  # 只有10%的概率播放，避免太吵
            self.play_sound('move', 0.3)
    
    def play_achievement_sound(self):
        """播放成就音效"""
        self.play_sound('achievement', 0.9)
    
    def generate_background_music(self):
        """生成简单的背景音乐"""
        if not self.enabled:
            return
        
        try:
            # 生成简单的环境音乐
            duration = 10.0  # 10秒循环
            sample_rate = 22050
            frames = int(duration * sample_rate)
            
            # 基础低频音调
            base_freq = 55  # A1
            wave = 0.3 * np.sin(2 * np.pi * base_freq * np.linspace(0, duration, frames))
            
            # 添加和声
            harmonics = [110, 165, 220]  # A2, E3, A3
            for freq in harmonics:
                harmonic_wave = 0.2 * np.sin(2 * np.pi * freq * np.linspace(0, duration, frames))
                # 添加缓慢的调制
                modulation = 0.1 * np.sin(2 * np.pi * 0.1 * np.linspace(0, duration, frames))
                harmonic_wave *= (1 + modulation)
                wave += harmonic_wave
            
            # 添加轻微的噪音纹理
            noise = 0.05 * np.random.normal(0, 1, frames)
            wave += noise
            
            # 应用低通滤波器（简单的移动平均）
            window_size = 100
            wave = np.convolve(wave, np.ones(window_size)/window_size, mode='same')
            
            # 转换为pygame音频格式
            wave = (wave * 32767 * 0.4).astype(np.int16)
            stereo_wave = np.array([wave, wave]).T
            stereo_wave = np.ascontiguousarray(stereo_wave)

            self.background_music = pygame.sndarray.make_sound(stereo_wave)
            
        except Exception as e:
            print(f"背景音乐生成失败: {e}")
    
    def play_background_music(self):
        """播放背景音乐"""
        if not self.enabled or not hasattr(self, 'background_music'):
            self.generate_background_music()
        
        if hasattr(self, 'background_music') and not self.music_playing:
            try:
                self.background_music.set_volume(self.music_volume * self.master_volume)
                self.background_music.play(-1)  # 无限循环
                self.music_playing = True
            except Exception as e:
                print(f"播放背景音乐失败: {e}")
    
    def stop_background_music(self):
        """停止背景音乐"""
        if self.music_playing:
            pygame.mixer.stop()
            self.music_playing = False
    
    def set_master_volume(self, volume: float):
        """设置主音量"""
        self.master_volume = max(0.0, min(1.0, volume))
        game_config.set("audio.master_volume", self.master_volume)
    
    def set_sfx_volume(self, volume: float):
        """设置音效音量"""
        self.sfx_volume = max(0.0, min(1.0, volume))
        game_config.set("audio.sfx_volume", self.sfx_volume)
    
    def set_music_volume(self, volume: float):
        """设置音乐音量"""
        self.music_volume = max(0.0, min(1.0, volume))
        game_config.set("audio.music_volume", self.music_volume)
        if hasattr(self, 'background_music'):
            self.background_music.set_volume(self.music_volume * self.master_volume)
    
    def toggle_sound(self):
        """切换音效开关"""
        self.enabled = not self.enabled
        game_config.set("audio.enable_sound", self.enabled)
        if not self.enabled:
            self.stop_background_music()

# 全局音效系统实例
audio_system = AudioSystem()
