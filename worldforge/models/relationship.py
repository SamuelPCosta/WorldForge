import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict

from worldforge.models.base import EntityType


class RelationType(str, Enum):
    MEMBER_OF = "member_of"
    LEADER_OF = "leader_of"
    EXILED_FROM = "exiled_from"
    RESIDES_IN = "resides_in"
    BORN_IN = "born_in"
    LOCATED_IN = "located_in"
    ALLY_OF = "ally_of"
    ENEMY_OF = "enemy_of"
    RIVAL_OF = "rival_of"
    CONTROLS = "controls"
    PROTECTS = "protects"
    OCCUPIES = "occupies"
    CUSTOM = "custom"


@dataclass
class Relationship:
    source_id: str
    source_type: EntityType
    target_id: str
    target_type: EntityType
    relation_type: str = RelationType.MEMBER_OF.value
    label: str = ""
    description: str = ""
    is_bidirectional: bool = False
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )

    def __post_init__(self) -> None:
        if not self.source_id or not self.source_id.strip():
            raise ValueError("O identificador de origem (source_id) não pode ser vazio.")
        if not self.target_id or not self.target_id.strip():
            raise ValueError("O identificador de destino (target_id) não pode ser vazio.")

        if isinstance(self.source_type, str):
            self.source_type = EntityType(self.source_type)
        if isinstance(self.target_type, str):
            self.target_type = EntityType(self.target_type)

        if not self.label and isinstance(self.relation_type, str):
            self.label = self.relation_type.replace("_", " ").title()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "source_id": self.source_id,
            "source_type": self.source_type.value,
            "target_id": self.target_id,
            "target_type": self.target_type.value,
            "relation_type": self.relation_type,
            "label": self.label,
            "description": self.description,
            "is_bidirectional": self.is_bidirectional,
            "created_at": self.created_at,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Relationship":
        return cls(
            id=data.get("id", str(uuid.uuid4())),
            source_id=data["source_id"],
            source_type=EntityType(data["source_type"]),
            target_id=data["target_id"],
            target_type=EntityType(data["target_type"]),
            relation_type=data.get("relation_type", RelationType.MEMBER_OF.value),
            label=data.get("label", ""),
            description=data.get("description", ""),
            is_bidirectional=data.get("is_bidirectional", False),
            created_at=data.get(
                "created_at", datetime.now(timezone.utc).isoformat()
            ),
        )
