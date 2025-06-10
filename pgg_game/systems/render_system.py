# src/pgg_game/systems/render_system.py

import pygame
from ..world.game_world import GameWorld
from ..components.transform import TransformComponent
from ..components.renderable import RenderableComponent, ShapeType
from ..config import COLORS

class RenderSystem:
    """
    Система отрисовки. Теперь отвечает ТОЛЬКО за отрисовку сущностей.
    Очистка экрана и обновление дисплея вынесены в Engine.
    """
    def __init__(self, screen: pygame.Surface):
        self.screen = screen

    def update(self, world: GameWorld):
        """
        Рисует все видимые сущности из мира на экране.
        """
        # Получаем все сущности, которые можно отрисовать
        entities_to_render = world.get_entities_with_components(
            TransformComponent,
            RenderableComponent
        )
        
        # Сортируем по слою для правильного порядка отрисовки
        sorted_entities = sorted(
            entities_to_render,
            key=lambda e: world.get_component(e, RenderableComponent).layer
        )

        # Проходим по сущностям и рисуем каждую
        for entity in sorted_entities:
            transform = world.get_component(entity, TransformComponent)
            renderable = world.get_component(entity, RenderableComponent)

            if not transform or not renderable:
                continue

            if renderable.shape == ShapeType.RECTANGLE:
                rect = pygame.Rect(transform.x, transform.y, transform.width, transform.height)
                pygame.draw.rect(self.screen, renderable.color, rect)
            
            elif renderable.shape == ShapeType.CIRCLE:
                center = (transform.x + transform.width // 2, transform.y + transform.height // 2)
                radius = min(transform.width, transform.height) // 2
                pygame.draw.circle(self.screen, renderable.color, center, radius)

        # ОБРАТИТЕ ВНИМАНИЕ: self.screen.fill() и pygame.display.flip() отсюда УБРАНЫ.
