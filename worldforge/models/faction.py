from dataclasses import dataclass, field
from typing import Any, Dict, Optional

from worldforge.models.base import BaseEntity, EntityType


@dataclass
class Faction(BaseEntity):
    faction_type: str = "guild"  # guild, empire, kingdom, order, clan
    headquarters_location_id: Optional[str] = None
    leader_character_id: Optional[str] = None
    influence_level: str = "Regional"
    alignment: str = ""

    def __post_init__(self) -> None:
        self.entity_type = EntityType.FACTION
        super().__post_init__()

    def to_dict(self) -> Dict[str, Any]:
        base = super().to_dict()
        base["attributes"] = {
            "faction_type": self.faction_type,
            "headquarters_location_id": self.headquarters_location_id,
            "leader_character_id": self.leader_character_id,
            "influence_level": self.influence_level,
            "alignment": self.alignment,
        }
        return base

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Faction":
        base_kwargs = cls.base_from_dict(data)
        attrs = data.get("attributes", {})
        return cls(
            id=base_kwargs["id"],
            entity_type=EntityType.FACTION,
            name=base_kwargs["name"],
            summary=base_kwargs["summary"],
            description=base_kwargs["description"],
            tags=base_kwargs["tags"],
            custom_attributes=base_kwargs["custom_attributes"],
            created_at=base_kwargs["created_at"],
            updated_at=base_kwargs["updated_at"],
            faction_type=attrs.get("faction_type", "guild"),
            headquarters_location_id=attrs.get("headquarters_location_id"),
            leader_character_id=attrs.get("leader_character_id"),
            influence_level=attrs.get("influence_level", "Regional"),
            alignment=attrs.get("alignment", ""),
        )
