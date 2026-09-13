import unittest
from worldforge.models import (
    BaseEntity,
    Character,
    EntityType,
    Faction,
    Location,
    Relationship,
    RelationType,
)


class TestEntityModels(unittest.TestCase):
    def test_base_entity_validation(self):
        with self.assertRaises(ValueError):
            BaseEntity(name="")

        with self.assertRaises(ValueError):
            BaseEntity(name="   ")

        entity = BaseEntity(name="Valen")
        self.assertEqual(entity.name, "Valen")
        self.assertIsNotNone(entity.id)
        self.assertEqual(entity.entity_type, EntityType.CHARACTER)

    def test_character_model_serialization(self):
        char = Character(
            name="Eldrin Sombrastratos",
            summary="Mago renegado",
            description="Antigo conselheiro arcano.",
            tags=["mago", "renegado"],
            aliases=["O Arquivista"],
            status="alive",
            role="Arquimago",
            species="Elfo",
            age="240",
        )
        data = char.to_dict()
        self.assertEqual(data["name"], "Eldrin Sombrastratos")
        self.assertEqual(data["entity_type"], "character")
        self.assertEqual(data["attributes"]["species"], "Elfo")
        self.assertEqual(data["attributes"]["aliases"], ["O Arquivista"])

        deserialized = Character.from_dict(data)
        self.assertEqual(deserialized.id, char.id)
        self.assertEqual(deserialized.name, char.name)
        self.assertEqual(deserialized.species, "Elfo")
        self.assertEqual(deserialized.aliases, ["O Arquivista"])

    def test_location_model_serialization(self):
        loc = Location(
            name="Cidadela de Aethelgard",
            summary="Fortaleza nas montanhas",
            location_type="city",
            climate="Subalpino",
            population_estimate="45000",
        )
        data = loc.to_dict()
        self.assertEqual(data["entity_type"], "location")
        self.assertEqual(data["attributes"]["location_type"], "city")

        deserialized = Location.from_dict(data)
        self.assertEqual(deserialized.name, "Cidadela de Aethelgard")
        self.assertEqual(deserialized.location_type, "city")
        self.assertEqual(deserialized.climate, "Subalpino")

    def test_faction_model_serialization(self):
        faction = Faction(
            name="Ordem Arcana",
            summary="Guilda de magos",
            faction_type="guild",
            influence_level="Global",
            alignment="Leal e Neutro",
        )
        data = faction.to_dict()
        self.assertEqual(data["entity_type"], "faction")
        self.assertEqual(data["attributes"]["alignment"], "Leal e Neutro")

        deserialized = Faction.from_dict(data)
        self.assertEqual(deserialized.name, "Ordem Arcana")
        self.assertEqual(deserialized.influence_level, "Global")

    def test_relationship_validation_and_serialization(self):
        with self.assertRaises(ValueError):
            Relationship(
                source_id="",
                source_type=EntityType.CHARACTER,
                target_id="fac-1",
                target_type=EntityType.FACTION,
            )

        with self.assertRaises(ValueError):
            Relationship(
                source_id="char-1",
                source_type=EntityType.CHARACTER,
                target_id="",
                target_type=EntityType.FACTION,
            )

        rel = Relationship(
            source_id="char-123",
            source_type=EntityType.CHARACTER,
            target_id="fac-456",
            target_type=EntityType.FACTION,
            relation_type=RelationType.MEMBER_OF.value,
            description="Membro sênior da guilda",
        )
        data = rel.to_dict()
        self.assertEqual(data["source_id"], "char-123")
        self.assertEqual(data["target_id"], "fac-456")
        self.assertEqual(data["relation_type"], "member_of")
        self.assertEqual(data["label"], "Member Of")

        deserialized = Relationship.from_dict(data)
        self.assertEqual(deserialized.id, rel.id)
        self.assertEqual(deserialized.source_id, "char-123")
        self.assertEqual(deserialized.target_id, "fac-456")


if __name__ == "__main__":
    unittest.main()
