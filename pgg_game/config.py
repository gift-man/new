# src/pgg_game/config.py

import pygame

# --- Основные настройки экрана и производительности ---
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60
WINDOW_TITLE = "Procedural Generation Strategy Game"

# --- Настройки игровой сетки и мира ---
TILE_SIZE = 32  # Размер одной клетки в пикселях

# Размеры сетки в тайлах (вычисляются автоматически)
GRID_WIDTH = SCREEN_WIDTH // TILE_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // TILE_SIZE

# --- Цвета ---
# Использование словаря для цветов делает код более читаемым и организованным.
COLORS = {
    'background': pygame.Color("#0d1b2a"),    # Темно-синий фон
    'grid_lines': pygame.Color("#1b263b"),    # Чуть светлее для линий сетки
    'text': pygame.Color("#e0e1dd"),          # Почти белый для текста
    'highlight': pygame.Color("#fca311"),     # Яркий оранжевый для выделения

    # Цвета игроков
    'player_one': pygame.Color("#e63946"),    # Красный
    'player_two': pygame.Color("#a8dadc"),    # Голубой
    'player_three': pygame.Color("#457b9d"),   # Синий
    'player_four': pygame.Color("#f1faee"),     # Белый
    
    # Цвета для провинций
    'province_neutral': pygame.Color("#778da9"), # Серый для нейтральных
}

