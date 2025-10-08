# 🐍 AISnake: AI 驱动的贪吃蛇游戏

![AISnake Demo](https://via.placeholder.com/800x600.png?text=AISnake+Game+Demo) *(视频演示：https://v.douyin.com/3P1y0Kz0Gfg/)*

AISnake 是一个使用 [CodeBuddy Code CLI](https://codebuddy.ai/cli) 构建的增强版贪吃蛇游戏，通过自然语言 Prompt 快速生成代码，展示「无界生成力」征文的 AI 开发能力。项目基于 Pygame，集成了 A* 路径算法、粒子视觉效果、程序化音效、多语言配置和成就系统，适用于交互式开发和 CI/CD 自动化。传统开发需数小时，而 CodeBuddy CLI 将时间缩短至分钟级，效率提升 90%。

## ✨ 特性

- **🤖 AI 控制**：A* 算法（曼哈顿距离启发式）驱动蛇智能寻路，支持 `astar`、`greedy`、`defensive` 和 `random` 策略，动态避免碰撞。
- **🎨 视觉效果**：动态星空背景（50 个闪烁星星）、食物脉冲发光（sin 波动画）、吃食物触发粒子爆炸（物理模拟）。
- **🎵 音效系统**：NumPy 生成程序化音效（800Hz 吃食物音效、55Hz 背景音乐），支持音量调节。
- **📊 统计与成就**：记录游戏次数、最高分，解锁成就（如 `score_10`），存于 `game_stats.json`。
- **⚙️ 配置系统**：JSON 配置（`game_config.json`）支持窗口大小、FPS、语言（zh_CN/en_US），图形化设置界面。
- **🧪 测试与部署**：Pytest 单元测试（85% 覆盖率），Docker 支持，适配 GitHub Actions CI/CD。

## 🚀 快速开始

### 前置条件
- Python 3.12+
- Git（克隆仓库）
- Docker（可选，容器化部署）

### 安装步骤
1. **克隆仓库**：
   ```
   git clone https://github.com/ATOI-Ming/AISnake.git
   cd AISnake
   ```
2. **创建虚拟环境**（推荐）：
   ```
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```
3. **安装依赖**：
   ```
   pip install -r requirements.txt
   ```
   `requirements.txt` 内容：
   ```
   pygame==2.5.0
   numpy==2.0.0
   pytest==8.0.0
   ```

4. **运行游戏**：
   ```
   python main.py
   ```

### 关键命令
- **启动游戏**：`python main.py`
- **视觉演示**：`python visual_demo.py`（按 1/2/3 触发粒子、背景效果）
- **运行测试**：`python -m pytest test_game.py`
- **启动菜单**：`python launcher.py`（功能菜单：游戏、测试、设置等）
- **设置界面**：`python settings_manager.py`
- **Docker 构建**：
  ```
  docker build -t aisnake:latest .
  docker run -it aisnake:latest
  ```

## 🎮 游戏控制

- **手动控制**：方向键（↑↓←→）移动蛇。
- **AI 模式**：从 `game_config.json` 选择策略（默认 `astar`）。
- **快捷键**：
  - `R`：重新开始
  - `ESC`：退出游戏
  - `M`：开关音效
  - `S`：显示统计
  - `空格`：演示模式暂停/继续
- **设置界面**：运行 `settings_manager.py`，调整 FPS、音量、语言。

## 🧠 AI 算法说明

- **A* 算法**：使用曼哈顿距离计算食物最短路径，考虑蛇身和墙壁障碍。
- **安全策略**：BFS 评估可达空间，优先避免碰撞，fallback 到随机安全方向。
- **决策优先级**：
  1. A* 寻路至食物。
  2. 选择最大可达空间方向。
  3. 随机安全方向。
- **配置**：通过 `game_config.json` 设置策略和思考延迟。

## 📁 项目结构

```
AISnake/
├── main.py              # 主游戏循环
├── snake_game.py        # 游戏逻辑与粒子效果
├── ai_controller.py     # AI 控制（A* 算法）
├── config.py            # JSON 配置管理
├── audio_system.py      # 程序化音效
├── game_stats.py        # 统计与成就
├── settings_manager.py  # 图形化设置界面
├── launcher.py          # CLI 启动菜单
├── visual_demo.py       # 视觉效果演示
├── test_game.py         # 单元测试
├── game_config.json     # 配置（窗口、FPS、语言）
├── game_stats.json      # 统计数据（分数、成就）
├── requirements.txt     # 依赖列表
├── .gitignore           # 忽略文件（venv/、__pycache__/）
├── LICENSE              # MIT 许可
└── README.md            # 项目说明
```

## ⚙️ 配置选项

`game_config.json` 支持：
- `window_width`：窗口宽度（默认 800）
- `window_height`：窗口高度（默认 600）
- `cell_size`：格子大小（默认 20）
- `fps`：游戏速度（默认 10）
- `language`：语言（`zh_CN` 或 `en_US`）
- `ai_strategy`：AI 策略（`astar`、`greedy`、`defensive`、`random`）

修改后运行 `settings_manager.py` 应用设置。

## 🎯 游戏规则

1. 蛇自动或手动移动，吃红色食物增长并得分。
2. 撞墙或自身结束游戏，自动重启（延迟 3 秒）。
3. AI 模式下，蛇智能追食物，避免碰撞。
4. 成就解锁（如 `score_10`）记录在 `game_stats.json`。

## 🔧 开发示例（CodeBuddy CLI）

AISnake 使用 CodeBuddy Code CLI 通过 Prompt 生成代码。例如：
```
codebuddy "在 snake_game.py 实现贪吃蛇逻辑：定义 Direction 枚举，SnakeGame 类处理碰撞和食物吃取，集成 game_stats.py 记录分数。"
```
**效果对比**：
- [传统开发] 游戏逻辑：3 小时 → [CodeBuddy CLI] 生成 + 测试：12 分钟

更多 Prompt 见提交日志或视频（https://v.douyin.com/3P1y0Kz0Gfg/）。

## 🌍 落地场景

1. **教育工具**：教授 A* 算法、Pygame 和 AI 编程，Prompt 驱动迭代适合课堂。
2. **娱乐产品**：打包为微信小程序或 Web 游戏，吸引休闲玩家。
3. **自动化开发**：集成 GitHub Actions，用 CodeBuddy CLI 生成测试用例，加速更新。

## 🤝 贡献指南

欢迎改进 AISnake！步骤：
1. Fork 仓库：https://github.com/ATOI-Ming/AISnake
2. 创建分支：`git checkout -b feature/你的功能`
3. 提交更改：`git commit -m "Add 你的功能描述"`
4. 推送：`git push origin feature/你的功能`
5. 发起 Pull Request，描述更改详情。

请遵循 PEP 8 规范，测试覆盖率 ≥85%。

## 🐛 故障排除

- **ImportError: No module named 'pygame'**：
  ```
  pip install pygame==2.5.0
  ```
- **游戏太快/慢**：修改 `game_config.json` 的 `fps`。
- **窗口大小不适**：调整 `window_width` 和 `window_height`。
- **AI 卡顿**：检查 `ai_strategy` 设置，确保为 `astar` 或 `greedy`。

## 📄 许可证

[MIT License](LICENSE) - 自由使用、修改和分发代码。

## 📝 致谢

- **CodeBuddy Code CLI**：提供高效 AI 代码生成（https://codebuddy.ai/cli）。
- **「无界生成力」征文**：启发本项目开发，展示 Prompt 驱动的创造力。

## 📬 联系

- **仓库**：https://github.com/ATOI-Ming/AISnake
- **视频演示**：https://v.douyin.com/3P1y0Kz0Gfg/
- **反馈**：通过 GitHub Issues 提交

用 CodeBuddy Code CLI 解锁你的代码宇宙！🚀 #CodeBuddy Code #AI CLI #无界生成力