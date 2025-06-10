# src/pgg_game/systems/ui_system.py

import pygame
from ..world.game_world import GameWorld
from .turn_system import TurnSystem
from ..components.player_info import PlayerInfoComponent
from ..components.province_info import ProvinceInfoComponent
from ..components.selected import SelectedComponent
from ..config import COLORS, SCREEN_WIDTH, SCREEN_HEIGHT

class UISystem:
    """
    Система управления пользовательским интерфейсом (UI).
    Разделена на методы для отрисовки разных игровых состояний.
    """
    def __init__(self, screen: pygame.Surface, turn_system: TurnSystem):
        self.screen = screen
        self.turn_system = turn_system
        
        # Загружаем шрифты один раз при инициализации для производительности
        try:
            self.font_title = pygame.font.SysFont("Arial", 48, bold=True)
            self.font_main = pygame.font.SysFont("Arial", 28)
            self.font_small = pygame.font.SysFont("Arial", 20)
        except pygame.error:
            # Запасные шрифты, если системные не найдены
            self.font_title = pygame.font.Font(None, 54)
            self.font_main = pygame.font.Font(None, 32)
            self.font_small = pygame.font.Font(None, 24)

    def _render_text(self, text: str, position: tuple, font: pygame.font.Font, color=COLORS['text'], center=False):
        """
        Вспомогательная функция для отрисовки текста.
        Добавлен флаг 'center' для удобного центрирования текста.
        """
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        if center:
            text_rect.center = position
        else:
            text_rect.topleft = position
        self.screen.blit(text_surface, text_rect)

    def update_menu(self):
        """
        Отрисовывает интерфейс главного меню.
        Вызывается из Engine, когда state == GameState.MENU.
        """
        title_pos = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3)
        self._render_text("Procedural Strategy", title_pos, self.font_title, COLORS['highlight'], center=True)
        
        start_pos = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self._render_text("Нажмите ENTER, чтобы начать игру", start_pos, self.font_main, center=True)
        
        exit_pos = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)
        self._render_text("Нажмите ESCAPE для выхода", exit_pos, self.font_small, center=True)

    def update_game_hud(self, world: GameWorld):
        """
        Отрисовывает игровой HUD (Heads-Up Display).
        Вызывается из Engine, когда state == GameState.GAME.
        """
        # Рисуем информационную панель о текущем ходе и игроке
        self._draw_turn_info(world)
        
        # Рисуем информацию о выбранной провинции, если таковая есть
        self._draw_selected_province_info(world)

    def _draw_turn_info(self, world: GameWorld):
        """Отрисовывает информацию о текущем игроке и ходе вверху экрана."""
        current_player_id = self.turn_system.get_current_player_id()
        if current_player_id is None:
            # Эта надпись теперь будет видна только в первые моменты, пока TurnSystem не найдет игроков
            self._render_text("Инициализация игроков...", (10, 10), self.font_main)
            return

        player_info = world.get_component(current_player_id, PlayerInfoComponent)
        if not player_info:
            return

        turn_text = f"Ход: {self.turn_system.turn_number}"
        player_text = f"Игрок: {player_info.name}"
        gold_text = f"Золото: {player_info.gold}"
        
        # Рисуем текст с небольшим отступом, используя цвет игрока
        self._render_text(turn_text, (10, 10), self.font_main, player_info.color)
        self._render_text(player_text, (180, 10), self.font_main, player_info.color)
        self._render_text(gold_text, (450, 10), self.font_main, player_info.color)

    def _draw_selected_province_info(self, world: GameWorld):
        """Ищет выбранную провинцию и, если находит, рисует информацию о ней."""
        selected_entities = world.get_entities_with_components(SelectedComponent, ProvinceInfoComponent)
        
        if not selected_entities:
            return # Ничего не выбрано, выходим

        # Берем первую (и по логике единственную) выбранную сущность
        selected_id = list(selected_entities)[0]
        province_info = world.get_component(selected_id, ProvinceInfoComponent)
        
        # --- Отрисовка инфо-панели внизу экрана ---
        panel_height = 80
        info_panel_rect = pygame.Rect(0, SCREEN_HEIGHT - panel_height, SCREEN_WIDTH, panel_height)
        pygame.draw.rect(self.screen, COLORS['background'], info_panel_rect)
        pygame.draw.line(self.screen, COLORS['highlight'], (0, SCREEN_HEIGHT - panel_height), (SCREEN_WIDTH, SCREEN_HEIGHT - panel_height), 2)
        
        # Название провинции
        self._render_text(f"Провинция: {province_info.name}", (20, SCREEN_HEIGHT - 65), self.font_main)
        
        # Владелец
        owner_text = "Владелец: Нейтральная"
        owner_color = COLORS['text']
        if province_info.owner_id is not None:
            owner_info = world.get_component(province_info.owner_id, PlayerInfoComponent)
            if owner_info:
                owner_text = f"Владелец: {owner_info.name}"
                owner_color = owner_info.color
        self._render_text(owner_text, (20, SCREEN_HEIGHT - 35), self.font_small, owner_color)

