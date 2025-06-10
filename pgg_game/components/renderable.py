# src/pgg_game/components/renderable.py

from dataclasses import dataclass
from enum import Enum, auto
import pygame

class ShapeType(Enum):
    """Перечисление для определения формы объекта при рендеринге."""
    RECTANGLE = auto()
    CIRCLE = auto()
    # В будущем можно добавить SPRITE, TEXT и т.д.

@dataclass
class RenderableComponent:
    """
    Содержит всю информацию, необходимую для отрисовки сущности.

    Система рендеринга будет искать сущности с этим компонентом и компонентом
    Transform, чтобы знать, ЧТО, ГДЕ и КАК рисовать.
    """
    color: pygame.Color  # Цвет объекта
    shape: ShapeType     # Форма объекта (прямоугольник, круг и т.д.)
    layer: int           # Слой отрисовки (0=фон, 1=тайлы, 2=юниты, 3=UI)
                         # Чем больше число, тем выше рисуется объект.
