import os
import shutil
import tempfile
import unittest

from worldforge.models import (
    Character,
    EntityType,
    Faction,
    Location,
    Relationship,
    RelationType,
)
from worldforge.repository import WorldRepository


class TestWorldRepository(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.repo = WorldRepository(self.temp_dir)

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    def test_save_and_load_world(self):
        char = Character(name="Eldrin", summary="Mago")
        loc = Location(name="Aethelgard", location_type="city")
        fac = Faction(name="Ordem Arcana", faction_type="guild")

        self.repo.add_character(char)
        self.repo.add_location(loc)
        self.repo.add_faction(fac)

        rel = Relationship(
            source_id=char.id,
            source_type=EntityType.CHARACTER,
            target_id=fac.id,
            target_type=EntityType.FACTION,
            relation_type=RelationType.MEMBER_OF.value,
        )
        self.repo.add_relationship(rel)

        # Salvar em disco
        self.repo.save_all()

        # Recarregar em um novo repositório
        new_repo = WorldRepository(self.temp_dir)
        new_repo.load_all()

        self.assertIsNotNone(new_repo.character_repo.get_by_id(char.id))
        self.assertIsNotNone(new_repo.location_repo.get_by_id(loc.id))
        self.assertIsNotNone(new_repo.faction_repo.get_by_id(fac.id))
        self.assertEqual(len(new_repo.get_all_relationships()), 1)
        self.assertEqual(new_repo.get_all_relationships()[0].source_id, char.id)

    def test_referential_integrity_on_character_deletion(self):
        char = Character(name="Heroi")
        fac = Faction(name="Facção")

        self.repo.add_character(char)
        self.repo.add_faction(fac)

        rel = Relationship(
            source_id=char.id,
            source_type=EntityType.CHARACTER,
            target_id=fac.id,
            target_type=EntityType.FACTION,
            relation_type="member_of",
        )
        self.repo.add_relationship(rel)

        fac.leader_character_id = char.id
        self.repo.update_faction(fac)

        self.assertEqual(len(self.repo.get_relationships_for_entity(char.id)), 1)
        self.assertEqual(self.repo.faction_repo.get_by_id(fac.id).leader_character_id, char.id)

        # Remover personagem
        self.repo.delete_character(char.id)

        # Verificar integridade referencial: relacionamento removido e chave estrangeira zerada
        self.assertEqual(len(self.repo.get_relationships_for_entity(char.id)), 0)
        self.assertIsNone(self.repo.faction_repo.get_by_id(fac.id).leader_character_id)

    def test_referential_integrity_on_location_deletion(self):
        loc = Location(name="Capital")
        char = Character(name="Cidadão", home_location_id=loc.id)

        self.repo.add_location(loc)
        self.repo.add_character(char)

        self.assertEqual(self.repo.character_repo.get_by_id(char.id).home_location_id, loc.id)

        # Remover local
        self.repo.delete_location(loc.id)

        # Deve zerar home_location_id
        self.assertIsNone(self.repo.character_repo.get_by_id(char.id).home_location_id)

    def test_search_entities(self):
        c1 = Character(name="Arthur Pendragon", summary="Rei lendário")
        c2 = Character(name="Merlin", summary="Conselheiro arcano", tags=["mago"])
        f1 = Faction(name="Távola Redonda", summary="Cavaleiros do reino")

        self.repo.add_character(c1)
        self.repo.add_character(c2)
        self.repo.add_faction(f1)

        results = self.repo.search_entities_by_name("merlin")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].name, "Merlin")

        results_tag = self.repo.search_entities_by_name("mago")
        self.assertEqual(len(results_tag), 1)
        self.assertEqual(results_tag[0].name, "Merlin")

        results_all = self.repo.search_entities_by_name("")
        self.assertEqual(len(results_all), 3)

    def test_add_relationship_validation(self):
        rel = Relationship(
            source_id="inexistente_1",
            source_type=EntityType.CHARACTER,
            target_id="inexistente_2",
            target_type=EntityType.FACTION,
        )
        with self.assertRaises(ValueError):
            self.repo.add_relationship(rel)

    def test_get_relationship_tree_empty(self):
        # Repositório sem entidades/relacionamentos deve retornar uma árvore vazia
        tree = self.repo.get_relationship_tree()
        self.assertEqual(tree, {"nodes": [], "edges": []})

    def test_get_relationship_tree_with_nodes(self):
        # Repositório com entidades e relacionamentos deve retornar os nós e arestas da árvore
        char = Character(name="Eldrin", summary="Mago")
        fac = Faction(name="Ordem Arcana", faction_type="guild")
        self.repo.add_character(char)
        self.repo.add_faction(fac)

        rel = Relationship(
            source_id=char.id,
            source_type=EntityType.CHARACTER,
            target_id=fac.id,
            target_type=EntityType.FACTION,
            relation_type=RelationType.MEMBER_OF.value,
        )
        self.repo.add_relationship(rel)

        tree = self.repo.get_relationship_tree()
        self.assertIn("nodes", tree)
        self.assertIn("edges", tree)

        # Verificar presença dos nós das entidades
        node_ids = [n["id"] for n in tree["nodes"]]
        self.assertIn(char.id, node_ids)
        self.assertIn(fac.id, node_ids)

        # Verificar presença da aresta do relacionamento
        self.assertEqual(len(tree["edges"]), 1)
        edge = tree["edges"][0]
        self.assertEqual(edge["source_id"], char.id)
        self.assertEqual(edge["target_id"], fac.id)
        self.assertEqual(edge["relation_type"], RelationType.MEMBER_OF.value)


if __name__ == "__main__":
    unittest.main()

