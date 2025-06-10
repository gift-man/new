# src/pgg_game/core/engine.py

import pygame
from enum import Enum, auto

from ..world.game_world import GameWorld
from ..config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, WINDOW_TITLE, GRID_WIDTH, GRID_HEIGHT, TILE_SIZE, COLORS
from ..systems.input_system import InputSystem
from ..systems.render_system import RenderSystem
from ..systems.turn_system import TurnSystem
from ..systems.ui_system import UISystem
from ..systems.map_generator_system import MapGenerationSystem

class GameState(Enum):
    MENU = auto()
    GAME = auto()

class Engine:
    def __init__(self, world: GameWorld):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(WINDOW_TITLE)
        self.clock = pygame.time.Clock()
        self.is_running = False
        self.world = world
        self.state = GameState.MENU

        # Инициализация систем
        self.turn_system = TurnSystem()
        self.input_system = InputSystem()
        self.ui_system = UISystem(self.screen, self.turn_system)
        self.render_system = RenderSystem(self.screen)
        self.map_generator_system = MapGenerationSystem(GRID_WIDTH, GRID_HEIGHT, TILE_SIZE)

    def run(self):
        """
        Запускает главный игровой цикл с единой, правильной логикой рендеринга.
        """
        self.is_running = True
        print(f"Engine запущен. Текущее состояние: {self.state.name}. Нажмите ENTER для старта.")

        while self.is_running:
            # 1. Регулируем FPS
            self.clock.tick(FPS)
            
            # 2. Обработка ввода (работает всегда)
            self.input_system.update(self.world, self)
            
            # 3. Обновление логики в зависимости от состояния
            if self.state == GameState.GAME:
                self.map_generator_system.update(self.world)
                self.turn_system.update(self.world)

            # 4. --- ЕДИНЫЙ КОНВЕЙЕР ОТРИСОВКИ ---
            # Он работает всегда, но рисует разные вещи в зависимости от состояния.
            
            # 4.1. Очищаем экран фоновым цветом
            self.screen.fill(COLORS['background'])
            
            # 4.2. Рисуем игровые объекты или UI
            if self.state == GameState.MENU:
                self.ui_system.update_menu()
            elif self.state == GameState.GAME:
                # Сначала рисуем игровые сущности (карту, юнитов)
                self.render_system.update(self.world)
                # Затем поверх них рисуем игровой интерфейс (HUD)
                self.ui_system.update_game_hud(self.world)

            # 4.3. Обновляем дисплей, чтобы показать все нарисованное
            pygame.display.flip()

            # 5. Проверяем флаг выхода
            if self.input_system.quit_requested:
                self.is_running = False
        
        self._cleanup()
        
    def change_state(self, new_state: GameState):
        if self.state == new_state: return
        print(f"Смена состояния с {self.state.name} на {new_state.name}")
        self.state = new_state

    def _cleanup(self):
        print("Engine: Завершение работы...")
        pygame.quit()
