# src/pgg_game/systems/turn_system.py

from typing import List
from ..world.game_world import GameWorld, Entity
from ..components.player_info import PlayerInfoComponent

class TurnSystem:
    """
    Система управления ходами. Отвечает за определение текущего игрока
    и переход хода к следующему.
    """
    def __init__(self):
        # Список ID сущностей-игроков, отсортированный по порядку хода.
        self.players: List[Entity] = []
        self.current_turn_index: int = 0
        self.turn_number: int = 1
        # Флаг, чтобы инициализация прошла только один раз.
        self.is_initialized: bool = False

    def _initialize(self, world: GameWorld):
        """
        Находит всех игроков в мире и сортирует их по порядку хода.
        Выполняется один раз при первом вызове update.
        """
        # Находим всех сущностей, у которых есть компонент PlayerInfoComponent.
        player_entities = world.get_entities_with_components(PlayerInfoComponent)
        
        # Сортируем ID игроков на основе значения 'turn_order' в их компонентах.
        self.players = sorted(
            player_entities,
            key=lambda e: world.get_component(e, PlayerInfoComponent).turn_order
        )
        
        if self.players:
            print(f"TurnSystem: Найдено игроков - {len(self.players)}. Порядок ходов установлен.")
        else:
            print("TurnSystem: Внимание! В мире не найдено ни одного игрока.")
        
        self.is_initialized = True

    def update(self, world: GameWorld):
        """
        Метод update в этой системе используется для первоначальной инициализации.
        В дальнейшем логика этой системы будет вызываться по событиям (например, end_turn).
        """
        if not self.is_initialized:
            self._initialize(world)
    
    def end_turn(self, world: GameWorld):
        """
        Завершает текущий ход и передает его следующему игроку.
        Этот метод будет вызываться извне (например, из InputSystem по нажатию кнопки).
        """
        if not self.players:
            return  # Нечего делать, если нет игроков

        # Переключаемся на следующего игрока в списке, используя остаток от деления
        # для автоматического "зацикливания" на первого игрока после последнего.
        self.current_turn_index = (self.current_turn_index + 1) % len(self.players)
        
        # Если мы вернулись к первому игроку (индекс 0), значит, начался новый глобальный ход.
        if self.current_turn_index == 0:
            self.turn_number += 1
            print(f"--- Начало хода номер {self.turn_number} ---")
            
        current_player_id = self.get_current_player_id()
        player_info = world.get_component(current_player_id, PlayerInfoComponent)
        print(f"Ход переходит к игроку: {player_info.name}")

    def get_current_player_id(self) -> Entity | None:
        """Возвращает ID игрока, чей сейчас ход."""
        if not self.players:
            return None
        return self.players[self.current_turn_index]

