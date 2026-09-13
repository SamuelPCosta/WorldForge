import json
import os
from abc import ABC, abstractmethod
from typing import Dict, Generic, List, Optional, TypeVar

from worldforge.models.base import BaseEntity

T = TypeVar("T", bound=BaseEntity)


class BaseEntityRepository(ABC, Generic[T]):
    """Classe base abstrata para repositórios de entidades de lore."""

    def __init__(self, file_path: str) -> None:
        self.file_path = file_path
        self._entities: Dict[str, T] = {}

    @abstractmethod
    def serialize_entity(self, entity: T) -> dict:
        """Converte entidade para dicionário JSON."""
        pass

    @abstractmethod
    def deserialize_entity(self, data: dict) -> T:
        """Converte dicionário JSON para instância de entidade."""
        pass

    def get_all(self) -> List[T]:
        """Retorna todas as entidades gerenciadas."""
        return list(self._entities.values())

    def get_by_id(self, entity_id: str) -> Optional[T]:
        """Busca uma entidade por ID."""
        return self._entities.get(entity_id)

    def add(self, entity: T) -> T:
        """Adiciona uma nova entidade ao repositório."""
        self._entities[entity.id] = entity
        return entity

    def update(self, entity: T) -> T:
        """Atualiza uma entidade existente."""
        entity.touch()
        self._entities[entity.id] = entity
        return entity

    def delete(self, entity_id: str) -> bool:
        """Remove uma entidade pelo ID."""
        if entity_id in self._entities:
            del self._entities[entity_id]
            return True
        return False

    def load(self) -> None:
        """Carrega as entidades a partir do arquivo JSON local."""
        self._entities.clear()
        if not os.path.exists(self.file_path):
            return

        with open(self.file_path, "r", encoding="utf-8") as f:
            try:
                data_list = json.load(f)
                if isinstance(data_list, list):
                    for item in data_list:
                        entity = self.deserialize_entity(item)
                        self._entities[entity.id] = entity
            except json.JSONDecodeError:
                self._entities.clear()

    def save(self) -> None:
        """Salva todas as entidades no arquivo JSON local."""
        os.makedirs(os.path.dirname(os.path.abspath(self.file_path)), exist_ok=True)
        data_list = [self.serialize_entity(entity) for entity in self._entities.values()]
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(data_list, f, indent=2, ensure_ascii=False)
