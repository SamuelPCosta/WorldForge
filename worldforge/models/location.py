from dataclasses import dataclass, field
from typing import Any, Dict, Optional

from worldforge.models.base import BaseEntity, EntityType


@dataclass
class Location(BaseEntity):
    location_type: str = "city"  # city, kingdom, continent, dungeon, tavern, region
    parent_location_id: Optional[str] = None
    governing_faction_id: Optional[str] = None
    climate: str = ""
    population_estimate: str = ""

    def __post_init__(self) -> None:
        self.entity_type = EntityType.LOCATION
        super().__post_init__()

    def to_dict(self) -> Dict[str, Any]:
        base = super().to_dict()
        base["attributes"] = {
            "location_type": self.location_type,
            "parent_location_id": self.parent_location_id,
            "governing_faction_id": self.governing_faction_id,
            "climate": self.climate,
            "population_estimate": self.population_estimate,
        }
        return base

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Location":
        base_kwargs = cls.base_from_dict(data)
        attrs = data.get("attributes", {})
        return cls(
            id=base_kwargs["id"],
            entity_type=EntityType.LOCATION,
            name=base_kwargs["name"],
            summary=base_kwargs["summary"],
            description=base_kwargs["description"],
            tags=base_kwargs["tags"],
            custom_attributes=base_kwargs["custom_attributes"],
            created_at=base_kwargs["created_at"],
            updated_at=base_kwargs["updated_at"],
            location_type=attrs.get("location_type", "city"),
            parent_location_id=attrs.get("parent_location_id"),
            governing_faction_id=attrs.get("governing_faction_id"),
            climate=attrs.get("climate", ""),
            population_estimate=attrs.get("population_estimate", ""),
        )
