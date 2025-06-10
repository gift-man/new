# src/pgg_game/systems/input_system.py

import pygame
from typing import TYPE_CHECKING

# --- ИЗМЕНЕНИЕ ЗДЕСЬ ---
# Мы импортируем не только Engine, но и GameState напрямую из модуля.
if TYPE_CHECKING:
    from ..core.engine import Engine, GameState

from ..world.game_world import GameWorld

class InputSystem:
    """
    Система обработки ввода. Преобразует события Pygame в действия в игре.
    """
    def __init__(self):
        self.quit_requested = False

    def update(self, world: GameWorld, engine: 'Engine'):
        """
        Основной метод системы, который вызывается каждый кадр.
        
        :param world: Экземпляр GameWorld для будущих взаимодействий.
        :param engine: Экземпляр Engine для управления состоянием игры.
        """
        for event in pygame.event.get():
            # 1. Обработка закрытия окна
            if event.type == pygame.QUIT:
                self.quit_requested = True
            
            # 2. Обработка нажатий клавиш
            if event.type == pygame.KEYDOWN:
                # Закрытие игры по нажатию на Escape работает всегда
                if event.key == pygame.K_ESCAPE:
                    self.quit_requested = True
                
                # --- И ИЗМЕНЕНИЕ ЗДЕСЬ ---
                # Теперь мы сравниваем engine.state напрямую с импортированным GameState.
                
                # Если мы в меню, нажатие Enter начинает игру
                if engine.state == GameState.MENU and event.key == pygame.K_RETURN:
                    engine.change_state(GameState.GAME)

                # Если мы в игре, можно добавить другие действия
                # Например, завершение хода по нажатию на пробел
                if engine.state == GameState.GAME and event.key == pygame.K_SPACE:
                    engine.turn_system.end_turn(world)

            # 3. Обработка кликов мыши (пока только выводим информацию)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if engine.state == GameState.GAME:
                    if event.button == 1: # Левая кнопка
                        mouse_x, mouse_y = event.pos
                        print(f"Клик в игровом режиме в координатах: ({mouse_x}, {mouse_y})")
                        # Здесь в Фазе 2 будет логика выбора провинций
