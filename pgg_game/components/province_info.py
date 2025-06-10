# src/pgg_game/components/province_info.py

from dataclasses import dataclass, field
from typing import Dict, Set, Optional

@dataclass
class ProvinceInfoComponent:
    """
    Хранит всю игровую информацию о провинции.

    Этот компонент делает сущность не просто "квадратом на карте", а ключевым
    игровым объектом со своими ресурсами, владельцем и соседями.
    """
    name: str  # Уникальное имя провинции, например, "P-1-5"

    # ID сущности-игрока, которой принадлежит провинция.
    # Optional[int] означает, что значение может быть int или None.
    # None означает, что провинция нейтральна.
    owner_id: Optional[int] = None

    # Словарь с ресурсами. Легко расширять, добавляя новые типы ресурсов.
    resources: Dict[str, int] = field(default_factory=dict)

    # Множество ID сущностей-провинций, которые являются соседями.
    # Использование set гарантирует отсутствие дубликатов и быстрые проверки.
    neighbors: Set[int] = field(default_factory=set)

