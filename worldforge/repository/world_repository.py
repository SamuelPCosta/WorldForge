import json
import os
from typing import Dict, List, Optional, Tuple, Union

from worldforge.models.base import BaseEntity, EntityType
from worldforge.models.character import Character
from worldforge.models.faction import Faction
from worldforge.models.location import Location
from worldforge.models.relationship import Relationship
from worldforge.repository.base_repository import BaseEntityRepository


class CharacterRepository(BaseEntityRepository[Character]):
    def serialize_entity(self, entity: Character) -> dict:
        return entity.to_dict()

    def deserialize_entity(self, data: dict) -> Character:
        return Character.from_dict(data)


class LocationRepository(BaseEntityRepository[Location]):
    def serialize_entity(self, entity: Location) -> dict:
        return entity.to_dict()

    def deserialize_entity(self, data: dict) -> Location:
        return Location.from_dict(data)


class FactionRepository(BaseEntityRepository[Faction]):
    def serialize_entity(self, entity: Faction) -> dict:
        return entity.to_dict()

    def deserialize_entity(self, data: dict) -> Faction:
        return Faction.from_dict(data)


class WorldRepository:
    """Gerenciador central do projeto de lore no WorldForge."""

    def __init__(self, root_dir: str) -> None:
        self.root_dir = root_dir
        self.entities_dir = os.path.join(root_dir, "entities")

        self.character_repo = CharacterRepository(
            os.path.join(self.entities_dir, "characters.json")
        )
        self.location_repo = LocationRepository(
            os.path.join(self.entities_dir, "locations.json")
        )
        self.faction_repo = FactionRepository(
            os.path.join(self.entities_dir, "factions.json")
        )

        self.relationships_file = os.path.join(root_dir, "relationships.json")
        self._relationships: Dict[str, Relationship] = {}

        self.world_metadata_file = os.path.join(root_dir, "world.json")
        self.world_metadata: dict = {
            "name": "Novo Mundo de Lore",
            "author": "Criador de Conteúdo",
            "version": "1.0.0",
        }

    # ---------------------------------------------------------
    # Persistência Global e Carregamento
    # ---------------------------------------------------------

    def load_all(self) -> None:
        """Carrega todas as entidades, relacionamentos e metadados."""
        self.character_repo.load()
        self.location_repo.load()
        self.faction_repo.load()
        self._load_relationships()
        self._load_world_metadata()

    def save_all(self) -> None:
        """Persiste todas as entidades, relacionamentos e metadados em disco."""
        os.makedirs(self.entities_dir, exist_ok=True)
        self.character_repo.save()
        self.location_repo.save()
        self.faction_repo.save()
        self._save_relationships()
        self._save_world_metadata()

    def _load_world_metadata(self) -> None:
        if os.path.exists(self.world_metadata_file):
            try:
                with open(self.world_metadata_file, "r", encoding="utf-8") as f:
                    self.world_metadata = json.load(f)
            except json.JSONDecodeError:
                pass

    def _save_world_metadata(self) -> None:
        os.makedirs(self.root_dir, exist_ok=True)
        with open(self.world_metadata_file, "w", encoding="utf-8") as f:
            json.dump(self.world_metadata, f, indent=2, ensure_ascii=False)

    def _load_relationships(self) -> None:
        self._relationships.clear()
        if os.path.exists(self.relationships_file):
            try:
                with open(self.relationships_file, "r", encoding="utf-8") as f:
                    data_list = json.load(f)
                    if isinstance(data_list, list):
                        for item in data_list:
                            rel = Relationship.from_dict(item)
                            self._relationships[rel.id] = rel
            except json.JSONDecodeError:
                self._relationships.clear()

    def _save_relationships(self) -> None:
        os.makedirs(self.root_dir, exist_ok=True)
        data_list = [rel.to_dict() for rel in self._relationships.values()]
        with open(self.relationships_file, "w", encoding="utf-8") as f:
            json.dump(data_list, f, indent=2, ensure_ascii=False)

    # ---------------------------------------------------------
    # Operações Genéricas de Entidades
    # ---------------------------------------------------------

    def get_entity(self, entity_id: str) -> Optional[BaseEntity]:
        """Obtém uma entidade pelo ID buscando em todas as categorias."""
        return (
            self.character_repo.get_by_id(entity_id)
            or self.location_repo.get_by_id(entity_id)
            or self.faction_repo.get_by_id(entity_id)
        )

    def get_all_entities(self) -> List[BaseEntity]:
        """Retorna a lista completa de entidades cadastradas."""
        result: List[BaseEntity] = []
        result.extend(self.character_repo.get_all())
        result.extend(self.location_repo.get_all())
        result.extend(self.faction_repo.get_all())
        return result

    def search_entities_by_name(self, query: str) -> List[BaseEntity]:
        """Busca entidades cujo nome ou resumo contenha a palavra-chave."""
        if not query or not query.strip():
            return self.get_all_entities()

        q = query.lower().strip()
        return [
            e
            for e in self.get_all_entities()
            if q in e.name.lower() or q in e.summary.lower() or any(q in t.lower() for t in e.tags)
        ]

    # ---------------------------------------------------------
    # Gerenciamento de Personagens
    # ---------------------------------------------------------

    def add_character(self, character: Character) -> Character:
        self.character_repo.add(character)
        return character

    def update_character(self, character: Character) -> Character:
        self.character_repo.update(character)
        return character

    def delete_character(self, character_id: str) -> bool:
        success = self.character_repo.delete(character_id)
        if success:
            self._enforce_referential_integrity(character_id)
        return success

    # ---------------------------------------------------------
    # Gerenciamento de Locais
    # ---------------------------------------------------------

    def add_location(self, location: Location) -> Location:
        self.location_repo.add(location)
        return location

    def update_location(self, location: Location) -> Location:
        self.location_repo.update(location)
        return location

    def delete_location(self, location_id: str) -> bool:
        success = self.location_repo.delete(location_id)
        if success:
            self._enforce_referential_integrity(location_id)
        return success

    # ---------------------------------------------------------
    # Gerenciamento de Facções
    # ---------------------------------------------------------

    def add_faction(self, faction: Faction) -> Faction:
        self.faction_repo.add(faction)
        return faction

    def update_faction(self, faction: Faction) -> Faction:
        self.faction_repo.update(faction)
        return faction

    def delete_faction(self, faction_id: str) -> bool:
        success = self.faction_repo.delete(faction_id)
        if success:
            self._enforce_referential_integrity(faction_id)
        return success

    # ---------------------------------------------------------
    # Gerenciamento de Relacionamentos e Integridade Referencial
    # ---------------------------------------------------------

    def add_relationship(self, relationship: Relationship) -> Relationship:
        """Adiciona um relacionamento validando existência das entidades envolvidas."""
        source = self.get_entity(relationship.source_id)
        target = self.get_entity(relationship.target_id)
        if not source:
            raise ValueError(
                f"Entidade de origem '{relationship.source_id}' não existe."
            )
        if not target:
            raise ValueError(
                f"Entidade de destino '{relationship.target_id}' não existe."
            )

        self._relationships[relationship.id] = relationship
        return relationship

    def delete_relationship(self, relationship_id: str) -> bool:
        if relationship_id in self._relationships:
            del self._relationships[relationship_id]
            return True
        return False

    def get_all_relationships(self) -> List[Relationship]:
        return list(self._relationships.values())

    def get_relationships_for_entity(self, entity_id: str) -> List[Relationship]:
        """Retorna todos os relacionamentos onde a entidade é origem ou destino."""
        return [
            rel
            for rel in self._relationships.values()
            if rel.source_id == entity_id or rel.target_id == entity_id
        ]

    def get_faction_members(self, faction_id: str) -> List[Character]:
        """Retorna personagens que são membros ou líderes de uma facção."""
        member_ids = set()
        # Via campo primário no personagem
        for char in self.character_repo.get_all():
            if char.primary_faction_id == faction_id:
                member_ids.add(char.id)

        # Via relacionamentos formais
        for rel in self._relationships.values():
            if rel.target_id == faction_id and rel.source_type == EntityType.CHARACTER:
                if rel.relation_type in ["member_of", "leader_of"]:
                    member_ids.add(rel.source_id)

        return [
            char
            for char in self.character_repo.get_all()
            if char.id in member_ids
        ]

    def get_location_governing_faction(self, location_id: str) -> Optional[Faction]:
        """Retorna a facção governante de um determinado local."""
        loc = self.location_repo.get_by_id(location_id)
        if loc and loc.governing_faction_id:
            return self.faction_repo.get_by_id(loc.governing_faction_id)

        # Buscar por relacionamento 'controls'
        for rel in self._relationships.values():
            if (
                rel.target_id == location_id
                and rel.source_type == EntityType.FACTION
                and rel.relation_type == "controls"
            ):
                return self.faction_repo.get_by_id(rel.source_id)

        return None

    def get_locations_governed_by_faction(self, faction_id: str) -> List[Location]:
        """Retorna locais governados ou controlados por uma facção."""
        locations = set()
        for loc in self.location_repo.get_all():
            if loc.governing_faction_id == faction_id:
                locations.add(loc.id)

        for rel in self._relationships.values():
            if (
                rel.source_id == faction_id
                and rel.target_type == EntityType.LOCATION
                and rel.relation_type == "controls"
            ):
                locations.add(rel.target_id)

        return [
            loc for loc in self.location_repo.get_all() if loc.id in locations
        ]

    def get_relationship_tree(self) -> dict:
        """Retorna as entidades e relacionamentos estruturados como nós e arestas de uma árvore de conexões."""
        nodes = []
        for entity in self.get_all_entities():
            entity_dict = entity.to_dict()
            nodes.append({
                "id": entity.id,
                "name": entity.name,
                "entity_type": entity.entity_type.value if isinstance(entity.entity_type, EntityType) else str(entity.entity_type),
                "details": entity_dict,
            })

        edges = []
        for rel in self.get_all_relationships():
            edges.append({
                "id": rel.id,
                "source_id": rel.source_id,
                "source_type": rel.source_type.value if isinstance(rel.source_type, EntityType) else str(rel.source_type),
                "target_id": rel.target_id,
                "target_type": rel.target_type.value if isinstance(rel.target_type, EntityType) else str(rel.target_type),
                "relation_type": rel.relation_type.value if hasattr(rel.relation_type, "value") else str(rel.relation_type),
            })

        return {
            "nodes": nodes,
            "edges": edges,
        }

    def export_relationships_markdown(self, filepath: Optional[str] = None) -> str:
        """Exporta os relacionamentos em formato Markdown para um arquivo em disco,

        agrupados por categorias de entidade (Personagens, Facções, Locais) e ordenados alfabeticamente.
        Retorna o caminho do arquivo exportado.
        """
        if filepath is None:
            filepath = os.path.join(self.root_dir, "exports", "relationships.md")

        lines = ["# Relacionamentos do Mundo", ""]

        # Agrupar e ordenar entidades alfabeticamente por tipo
        characters = sorted(self.character_repo.get_all(), key=lambda x: x.name.lower())
        factions = sorted(self.faction_repo.get_all(), key=lambda x: x.name.lower())
        locations = sorted(self.location_repo.get_all(), key=lambda x: x.name.lower())

        groups = [
            ("Personagens", characters),
            ("Facções", factions),
            ("Locais", locations),
        ]

        for group_title, entities in groups:
            lines.append(f"## {group_title}")
            lines.append("")
            if not entities:
                lines.append("*Nenhuma entidade cadastrada.*")
                lines.append("")
                continue

            has_relationships = False
            for entity in entities:
                rels = self.get_relationships_for_entity(entity.id)
                if not rels:
                    continue

                has_relationships = True
                lines.append(f"- **{entity.name}**")

                # Ordenar relacionamentos pelo nome da outra entidade
                rel_items = []
                for rel in rels:
                    if rel.source_id == entity.id:
                        other = self.get_entity(rel.target_id)
                        other_name = other.name if other else rel.target_id
                        other_type = (
                            other.entity_type.value
                            if (other and hasattr(other.entity_type, "value"))
                            else "desconhecido"
                        )
                        rel_str = f"  - {rel.relation_type} -> **{other_name}** ({other_type})"
                    else:
                        other = self.get_entity(rel.source_id)
                        other_name = other.name if other else rel.source_id
                        other_type = (
                            other.entity_type.value
                            if (other and hasattr(other.entity_type, "value"))
                            else "desconhecido"
                        )
                        rel_str = f"  - **{other_name}** ({other_type}) -> {rel.relation_type}"
                    rel_items.append((other_name.lower(), rel_str))

                rel_items.sort(key=lambda x: x[0])
                for _, rel_line in rel_items:
                    lines.append(rel_line)

            if not has_relationships:
                lines.append("*Nenhum relacionamento encontrado nesta categoria.*")
            lines.append("")

        content = "\n".join(lines)
        os.makedirs(os.path.dirname(os.path.abspath(filepath)), exist_ok=True)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)

        return filepath

    def _enforce_referential_integrity(self, deleted_entity_id: str) -> None:
        """Garante a eliminação de relacionamentos e referências órfãs."""
        # 1. Eliminar relacionamentos associados
        rel_ids_to_delete = [
            rel.id
            for rel in self._relationships.values()
            if rel.source_id == deleted_entity_id or rel.target_id == deleted_entity_id
        ]
        for rel_id in rel_ids_to_delete:
            del self._relationships[rel_id]

        # 2. Limpar referências diretas em Personagens
        for char in self.character_repo.get_all():
            modified = False
            if char.home_location_id == deleted_entity_id:
                char.home_location_id = None
                modified = True
            if char.primary_faction_id == deleted_entity_id:
                char.primary_faction_id = None
                modified = True
            if modified:
                self.character_repo.update(char)

        # 3. Limpar referências diretas em Locais
        for loc in self.location_repo.get_all():
            modified = False
            if loc.parent_location_id == deleted_entity_id:
                loc.parent_location_id = None
                modified = True
            if loc.governing_faction_id == deleted_entity_id:
                loc.governing_faction_id = None
                modified = True
            if modified:
                self.location_repo.update(loc)

        # 4. Limpar referências diretas em Facções
        for fac in self.faction_repo.get_all():
            modified = False
            if fac.headquarters_location_id == deleted_entity_id:
                fac.headquarters_location_id = None
                modified = True
            if fac.leader_character_id == deleted_entity_id:
                fac.leader_character_id = None
                modified = True
            if modified:
                self.faction_repo.update(fac)
