from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from worldforge.models.base import BaseEntity, EntityType


@dataclass
class Character(BaseEntity):
    aliases: List[str] = field(default_factory=list)
    status: str = "alive"  # alive, deceased, unknown
    role: str = ""
    species: str = ""
    age: str = ""
    home_location_id: Optional[str] = None
    primary_faction_id: Optional[str] = None

    def __post_init__(self) -> None:
        self.entity_type = EntityType.CHARACTER
        super().__post_init__()

    def to_dict(self) -> Dict[str, Any]:
        base = super().to_dict()
        base["attributes"] = {
            "aliases": list(self.aliases),
            "status": self.status,
            "role": self.role,
            "species": self.species,
            "age": self.age,
            "home_location_id": self.home_location_id,
            "primary_faction_id": self.primary_faction_id,
        }
        return base

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Character":
        base_kwargs = cls.base_from_dict(data)
        attrs = data.get("attributes", {})
        return cls(
            id=base_kwargs["id"],
            entity_type=EntityType.CHARACTER,
            name=base_kwargs["name"],
            summary=base_kwargs["summary"],
            description=base_kwargs["description"],
            tags=base_kwargs["tags"],
            custom_attributes=base_kwargs["custom_attributes"],
            created_at=base_kwargs["created_at"],
            updated_at=base_kwargs["updated_at"],
            aliases=list(attrs.get("aliases", [])),
            status=attrs.get("status", "alive"),
            role=attrs.get("role", ""),
            species=attrs.get("species", ""),
            age=attrs.get("age", ""),
            home_location_id=attrs.get("home_location_id"),
            primary_faction_id=attrs.get("primary_faction_id"),
        )
