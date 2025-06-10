# src/pgg_game/world/game_world.py

from typing import Dict, Type, Any, Set, Optional, List
from collections import defaultdict

# Это базовые типы, которые мы будем использовать для ясности.
# Entity — это просто уникальный идентификатор (число).
Entity = int
# ComponentType — это любой из наших классов компонентов (например, TransformComponent).
ComponentType = Type[Any]


class GameWorld:
    """
    Класс GameWorld действует как центральное хранилище данных для игры.
    Он управляет всеми сущностями (Entities) и их компонентами (Components).

    Эта структура похожа на базу данных:
    - Сущности — это просто уникальные ID.
    - Компоненты — это объекты данных, привязанные к этим ID.
    - Системы (Systems) будут запрашивать у этого мира данные для обработки.

    Сам GameWorld не содержит никакой игровой логики, только управляет данными.
    """
    def __init__(self):
        # Счетчик для генерации уникальных ID для каждой новой сущности.
        self.next_entity_id: Entity = 0

        # Основное хранилище компонентов.
        # Это словарь словарей, структурированный для быстрого доступа:
        # { ComponentType: { EntityID: ComponentInstance } }
        # Например:
        # { TransformComponent: { 0: Transform(...), 1: Transform(...) },
        #   RenderableComponent: { 0: Renderable(...) } }
        # Использование defaultdict(dict) упрощает добавление первого компонента
        # нового типа, так как не требует предварительной проверки ключа.
        self.components: Dict[ComponentType, Dict[Entity, Any]] = defaultdict(dict)

    def create_entity(self) -> Entity:
        """
        Создает новую сущность и возвращает ее уникальный ID.
        """
        entity_id = self.next_entity_id
        self.next_entity_id += 1
        return entity_id

    def add_component(self, entity_id: Entity, component_instance: Any):
        """
        Привязывает экземпляр компонента к определенной сущности.

        :param entity_id: ID сущности, к которой добавляется компонент.
        :param component_instance: Экземпляр компонента (например, TransformComponent(0, 0, 32, 32)).
        """
        component_type = type(component_instance)
        self.components[component_type][entity_id] = component_instance

    def get_component(self, entity_id: Entity, component_type: ComponentType) -> Optional[Any]:
        """
        Возвращает экземпляр компонента заданного типа для указанной сущности.

        :param entity_id: ID сущности, чей компонент мы ищем.
        :param component_type: Класс компонента (например, TransformComponent).
        :return: Экземпляр компонента или None, если он не найден.
        """
        return self.components[component_type].get(entity_id)

    def get_entities_with_components(self, *component_types: ComponentType) -> Set[Entity]:
        """
        Возвращает множество ID всех сущностей, которые имеют ВСЕ указанные компоненты.
        Это ключевой метод для систем. Например, RenderSystem запросит сущности,
        у которых есть и TransformComponent, и RenderableComponent.

        :param component_types: Один или несколько классов компонентов.
        :return: Множество ID сущностей.
        """
        # Если типы компонентов не переданы, возвращаем пустое множество.
        if not component_types:
            return set()
        
        # Начинаем с множества сущностей, имеющих первый тип компонента.
        # Используем .get(component_types[0], {}) для безопасности, если
        # ни одна сущность не имеет такого компонента.
        try:
            result_entities = set(self.components[component_types[0]].keys())
        except KeyError:
            # Если ни одна сущность не имеет первого компонента, то результат - пустое множество.
            return set()

        # Если запрошен только один тип компонента, возвращаем результат.
        if len(component_types) == 1:
            return result_entities

        # Для остальных типов компонентов, мы последовательно "пересекаем" множества.
        # Это эффективно оставляет только те сущности, которые есть во всех списках.
        for component_type in component_types[1:]:
            entities_with_comp = set(self.components.get(component_type, {}).keys())
            result_entities.intersection_update(entities_with_comp)

            # Оптимизация: если на каком-то шаге результат стал пустым,
            # нет смысла продолжать.
            if not result_entities:
                return set()

        return result_entities

    def delete_entity(self, entity_id: Entity):
        """
        Полностью удаляет сущность и все связанные с ней компоненты.
        """
        for component_storage in self.components.values():
            if entity_id in component_storage:
                del component_storage[entity_id]

