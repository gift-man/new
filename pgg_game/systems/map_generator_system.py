# src/pgg_game/systems/map_generator_system.py

import random
from ..world.game_world import GameWorld
from ..config import TILE_SIZE, GRID_WIDTH, GRID_HEIGHT
from ..components.transform import TransformComponent
from ..components.renderable import RenderableComponent, ShapeType
from ..components.province_info import ProvinceInfoComponent
from ..config import COLORS

class MapGenerationSystem:
    def __init__(self, width: int, height: int, tile_size: int):
        self.width = width
        self.height = height
        self.tile_size = tile_size
        self.map_generated = False

    def update(self, world: GameWorld):
        # Эта система должна сработать только один раз.
        if self.map_generated:
            return

        print("MapGenerationSystem: Начало генерации карты...")
        
        # Простая генерация сетки провинций, как в вашем старом проекте.
        for y in range(self.height):
            for x in range(self.width):
                # Пропускаем некоторые тайлы для создания "воды" или пустот
                if random.random() < 0.1: # 10% шанс пропуска
                    continue
                
                # Создаем сущность для новой провинции
                province_entity = world.create_entity()
                
                # Добавляем компоненты
                world.add_component(province_entity, TransformComponent(
                    x=x * self.tile_size,
                    y=y * self.tile_size,
                    width=self.tile_size,
                    height=self.tile_size
                ))
                world.add_component(province_entity, RenderableComponent(
                    color=COLORS['province_neutral'],
                    shape=ShapeType.RECTANGLE,
                    layer=1 # Слой карты
                ))
                world.add_component(province_entity, ProvinceInfoComponent(
                    name=f"P-{x}-{y}" # Уникальное имя по координатам
                ))

        print(f"MapGenerationSystem: Генерация карты завершена.")
        self.map_generated = True

