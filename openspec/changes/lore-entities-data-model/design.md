## Context

WorldForge é uma aplicação desktop offline voltada para escritores, mestres de RPG e criadores de mundos (*worldbuilders*). Para permitir o gerenciamento flexível e sem dependência de internet ou bancos de dados complexos, a aplicação adotará um modelo de dados baseado em arquivos JSON locais com interface gráfica construída em PyQt6/PyQt5.

Esta especificação de design detalha a arquitetura do modelo de dados JSON, o esquema de relacionamentos e a estrutura de persistência local.

## Goals / Non-Goals

**Goals:**
- Definir esquemas JSON declarativos e extensíveis para Personagens (`Character`), Locais (`Location`) e Facções (`Faction`).
- Definir um modelo de relacionamentos direcionados e tipados entre quaisquer entidades.
- Estabelecer a arquitetura de armazenamento em arquivos JSON locais para operação 100% offline.
- Especificar os padrões de navegação e componentes da UI em PyQt para apresentação e edição de dados.

**Non-Goals:**
- Suporte a sincronização em nuvem ou bancos de dados relacionais/NoSQL remotos nesta fase.
- Suporte a upload/processamento de imagens ou binários (foco exclusivo em lore estruturada em texto/JSON).
- Mecanismo de colaboração em tempo real multiusuário.

## Decisions

### 1. Modelo de Dados de Entidades (JSON Schema)

Cada entidade possui um identificador único (`id`), um tipo base (`entity_type`), campos comuns de metadados e um bloco estendido específico para o seu tipo.

#### 1.1 Esquema Base de Entidade (`base_entity.json`)
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "BaseEntity",
  "type": "object",
  "required": ["id", "entity_type", "name", "created_at", "updated_at"],
  "properties": {
    "id": {
      "type": "string",
      "description": "Identificador único da entidade (UUID v4 ou slug tipado ex: char-123)"
    },
    "entity_type": {
      "type": "string",
      "enum": ["character", "location", "faction"]
    },
    "name": {
      "type": "string",
      "minLength": 1
    },
    "summary": {
      "type": "string",
      "description": "Resumo curto/linha de soco da entidade"
    },
    "description": {
      "type": "string",
      "description": "Descrição detalhada em texto puro ou Markdown"
    },
    "tags": {
      "type": "array",
      "items": { "type": "string" }
    },
    "custom_attributes": {
      "type": "object",
      "additionalProperties": { "type": "string" },
      "description": "Atributos customizados no formato chave-valor"
    },
    "created_at": { "type": "string", "format": "date-time" },
    "updated_at": { "type": "string", "format": "date-time" }
  }
}
```

#### 1.2 Entidade Personagem (`Character`)
```json
{
  "id": "char-8f4b2a1e-4c91-4d32-9a01-123456789abc",
  "entity_type": "character",
  "name": "Eldrin Sombrastratos",
  "summary": "Mago renegado e antigo conselheiro da Ordem Arcana",
  "description": "Nascido nas terras baixas de Valen, Eldrin estudou as artes proibidas antes de ser exilado...",
  "tags": ["mago", "renegado", "protagonista"],
  "attributes": {
    "aliases": ["O Arquivista Cinzento", "Sombra de Valen"],
    "status": "alive",
    "role": "Arquimago Renegado",
    "species": "Elfo",
    "age": "240",
    "home_location_id": "loc-1a2b3c4d-5e6f-7a8b-9c0d-112233445566",
    "primary_faction_id": "fac-99887766-5544-3322-1100-aabbccddeeff"
  },
  "custom_attributes": {
    "Nível de Ameaça": "Alto",
    "Elemento Principal": "Arcano/Sombra"
  },
  "created_at": "2026-09-13T19:00:00Z",
  "updated_at": "2026-09-13T19:00:00Z"
}
```

#### 1.3 Entidade Local (`Location`)
```json
{
  "id": "loc-1a2b3c4d-5e6f-7a8b-9c0d-112233445566",
  "entity_type": "location",
  "name": "Cidadela de Aethelgard",
  "summary": "Fortaleza milenar encravada nas Montanhas dos Suspiros",
  "description": "Construída na Primeira Era, Aethelgard serve como sede para a Ordem Arcana e ponto neutro de comércio...",
  "tags": ["fortaleza", "montanha", "capital"],
  "attributes": {
    "location_type": "city",
    "parent_location_id": "loc-00000000-0000-0000-0000-000000000001",
    "governing_faction_id": "fac-99887766-5544-3322-1100-aabbccddeeff",
    "climate": "Subalpino Frio",
    "population_estimate": "45000"
  },
  "custom_attributes": {
    "Recurso Principal": "Minério Arcano",
    "Defesa": "Muralhas Mágicas"
  },
  "created_at": "2026-09-13T19:00:00Z",
  "updated_at": "2026-09-13T19:00:00Z"
}
```

#### 1.4 Entidade Facção (`Faction`)
```json
{
  "id": "fac-99887766-5544-3322-1100-aabbccddeeff",
  "entity_type": "faction",
  "name": "Ordem Arcana",
  "summary": "Conselho de magos e guardiões do conhecimento proibido",
  "description": "Uma organização antiga dedicada a catalogar e conter artefatos perigosos por todo o continente...",
  "tags": ["magia", "governo", "antigo"],
  "attributes": {
    "faction_type": "guild",
    "headquarters_location_id": "loc-1a2b3c4d-5e6f-7a8b-9c0d-112233445566",
    "leader_character_id": "char-8f4b2a1e-4c91-4d32-9a01-123456789abc",
    "influence_level": "Global",
    "alignment": "Leal e Neutro"
  },
  "custom_attributes": {
    "Lema": "Conhecimento é Custódia",
    "Fundação": "Ano 120 da Era Dourada"
  },
  "created_at": "2026-09-13T19:00:00Z",
  "updated_at": "2026-09-13T19:00:00Z"
}
```

---

### 2. Modelo de Dados de Relacionamentos (`relationships.json`)

Os relacionamentos são direcionados (`source` → `target`), com tipo formal e descrição explicativa contextual da relação.

#### 2.1 Esquema de Relacionamento (`relationship.json`)
```json
{
  "id": "rel-3c2b1a0f-9e8d-7c6b-5a4f-001122334455",
  "source_id": "char-8f4b2a1e-4c91-4d32-9a01-123456789abc",
  "source_type": "character",
  "target_id": "fac-99887766-5544-3322-1100-aabbccddeeff",
  "target_type": "faction",
  "relation_type": "exiled_from",
  "label": "Exilado de",
  "description": "Eldrin foi banido da Ordem Arcana após realizar experimentos não autorizados na Cidadela.",
  "is_bidirectional": false,
  "created_at": "2026-09-13T19:00:00Z"
}
```

#### Tipos Padrão de Relacionamento (`relation_type`):
- `member_of` / `leader_of` / `exiled_from` (Character ↔ Faction)
- `resides_in` / `born_in` / `located_in` (Character / Faction ↔ Location)
- `ally_of` / `enemy_of` / `rival_of` (Character/Faction ↔ Character/Faction)
- `controls` / `protects` / `occupies` (Faction/Character ↔ Location)
- `custom` (Relacionamento personalizado definido pelo usuário)

---

### 3. Arquitetura de Persistência Local e Diretórios

Para manter a aplicação rápida e com fácil controle de versão ou backup, cada projeto de lore (`World`) é salvo em um diretório com a seguinte estrutura de arquivos JSON:

```text
meu_mundo_lore/
├── world.json                 # Metadados globais (nome, autor, versão da schema)
├── entities/
│   ├── characters.json        # Coleção de entidades do tipo Character
│   ├── locations.json         # Coleção de entidades do tipo Location
│   └── factions.json          # Coleção de entidades do tipo Faction
└── relationships.json         # Coleção global de interconexões
```

**Decisão Racional:** Armazenar as entidades agrupadas por tipo em arquivos JSON individuais evita milhares de arquivos no sistema operacional e simplifica o carregamento/salvamento por módulo na UI PyQt.

---

### 4. Arquitetura da Interface Gráfica (PyQt)

A UI será estruturada no padrão **Model-View-Controller (MVC)** com PyQt:

- **Store/Manager Layer (`WorldRepository`)**: Módulo Python responsável por ler, gravar e validar os arquivos JSON locais. Mantém um índice em memória (`dict[id, Entity]`) para buscas e resoluções de relacionamentos em tempo de execução O(1).
- **Navigation Controller (`LoreNavigator`)**: Gerencia o histórico de navegação (Back/Forward) estilo navegador web ao clicar nos relacionamentos entre entidades.
- **Views (Componentes PyQt)**:
  - `EntityTreeWidget` / `Sidebar`: Navegação por categorias (Personagens, Locais, Facções).
  - `EntityDetailView`: Exibe os dados da entidade ativa e lista clicável de seus relacionamentos de entrada/saída (`QListWidget` / `QLabel` interativo).
  - `EntityEditorDialog`: Formulário dinâmico para cadastrar e editar atributos da entidade.
  - `RelationshipEditorDialog`: Modal para selecionar entidade de destino e registrar novas conexões.

---

## Risks / Trade-offs

- **Integridade Referencial em JSON Local** → *Risco*: Excluir um personagem pode deixar um `relationship` órfão apontando para um `target_id` inexistente.
  - *Mitigação*: O `WorldRepository` executará limpeza em cascata ao remover uma entidade, expurgando todos os relacionamentos onde o `id` removido seja `source_id` ou `target_id`.
- **Desempenho com grandes coleções JSON** → *Risco*: Projetos com milhares de entidades podem atrasar a escrita em disco se reescreverem o JSON inteiro em cada alteração.
  - *Mitigação*: Manter o modelo em memória e realizar *autosave* assíncrono ou salvar sob demanda do usuário.
