# src/pgg_game/components/player_info.py

from dataclasses import dataclass
import pygame

@dataclass
class PlayerInfoComponent:
    """
    Хранит информацию о сущности-игроке.
    """
    name: str
    color: pygame.Color
    turn_order: int  # Порядок хода (0 - ходит первым, 1 - вторым и т.д.)
    gold: int = 100  # Начальное количество золота
