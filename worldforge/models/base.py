import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional


class EntityType(str, Enum):
    CHARACTER = "character"
    LOCATION = "location"
    FACTION = "faction"


@dataclass
class BaseEntity:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    entity_type: EntityType = EntityType.CHARACTER
    name: str = ""
    summary: str = ""
    description: str = ""
    tags: List[str] = field(default_factory=list)
    custom_attributes: Dict[str, str] = field(default_factory=dict)
    created_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    updated_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )

    def __post_init__(self) -> None:
        if not self.name or not self.name.strip():
            raise ValueError("O nome da entidade não pode ser vazio.")
        if isinstance(self.entity_type, str) and not isinstance(
            self.entity_type, EntityType
        ):
            self.entity_type = EntityType(self.entity_type)

    def touch(self) -> None:
        """Atualiza o timestamp updated_at para o momento atual."""
        self.updated_at = datetime.now(timezone.utc).isoformat()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "entity_type": self.entity_type.value,
            "name": self.name,
            "summary": self.summary,
            "description": self.description,
            "tags": list(self.tags),
            "custom_attributes": dict(self.custom_attributes),
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    @classmethod
    def base_from_dict(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "id": data.get("id", str(uuid.uuid4())),
            "entity_type": EntityType(data.get("entity_type", "character")),
            "name": data.get("name", ""),
            "summary": data.get("summary", ""),
            "description": data.get("description", ""),
            "tags": list(data.get("tags", [])),
            "custom_attributes": dict(data.get("custom_attributes", {})),
            "created_at": data.get(
                "created_at", datetime.now(timezone.utc).isoformat()
            ),
            "updated_at": data.get(
                "updated_at", datetime.now(timezone.utc).isoformat()
            ),
        }
