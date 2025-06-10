# src/pgg_game/components/selected.py

from dataclasses import dataclass

@dataclass
class SelectedComponent:
    """
    Компонент-маркер, указывающий, что сущность в данный момент выбрана игроком.
    Не содержит данных. UISystem будет искать сущности с этим компонентом,
    чтобы отобразить по ним подробную информацию.
    """
    pass

