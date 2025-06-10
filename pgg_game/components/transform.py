# src/pgg_game/components/transform.py

from dataclasses import dataclass

@dataclass
class TransformComponent:
    """
    Хранит информацию о положении и размере сущности в мире.

    Это один из самых базовых компонентов. Он используется как системами
    логики (для определения соседства), так и системой рендеринга (для отрисовки
    в правильном месте).
    """
    x: int  # Координата X в пикселях
    y: int  # Координата Y в пикселях
    width: int
    height: int

