# WorldForge

**WorldForge** é uma aplicação em Python projetada para auxílio na criação, gerenciamento e navegação de universos de ficção e worldbuilding. Permite registrar entidades ricas de lore (como Personagens, Facções e Locais), estabelecer relacionamentos entre elas e visualizar/exportar o grafo de conexões do mundo de forma integrada e offline.

---

## 🚀 Funcionalidades

- **Gerenciamento de Entidades de Lore**:
  - **Personagens (`Character`)**: Atributos ricas, resumo, tags, facção primária e local de origem.
  - **Facções (`Faction`)**: Tipo de organização, líder e sede.
  - **Locais (`Location`)**: Categoria/tipo de local, facção governante e local pai (hierarquia geográfica).
  - **Relacionamentos (`Relationship`)**: Vínculos direcionados entre entidades com tipos parametrizados (ex: `member_of`, `leader_of`, `controls`, `ally_of`, `enemy_of`).

- **Persistência Local e Integridade Referencial**:
  - Armazenamento em arquivos JSON estruturados por categoria.
  - Manutenção e limpeza automática de referências órfãs e relacionamentos ao deletar uma entidade.

- **Navegação e Exportação de Conexões**:
  - **Árvore de Relacionamentos (`get_relationship_tree`)**: Estrutura em formato de grafo contendo nós (*nodes*) e arestas (*edges*).
  - **Exportação em Markdown (`export_relationships_markdown`)**: Exporta a lista de relacionamentos agrupada por categorias (Personagens, Facções, Locais) e ordenada alfabeticamente para um arquivo `.md`.

---

## 🛠️ Estrutura do Projeto

```text
WorldForge/
├── worldforge/
│   ├── models/           # Schemas e dataclasses (BaseEntity, Location, Faction, Relationship)
│   ├── repository/       # Camada de persistência local (BaseEntityRepository, WorldRepository)
│   └── __init__.py
├── tests/                # Suíte de testes unitários e de integração
│   ├── test_models.py
│   └── test_repository.py
├── openspec/             # Documentação de especificação de mudanças e tarefas
└── README.md
```

---

## 🧪 Como Rodar os Testes

Certifique-se de estar na raiz do projeto e execute os testes automatizados via `pytest`:

### Executar toda a suíte de testes
```powershell
python -m pytest
```

### Executar apenas os testes de repositório
```powershell
python -m pytest tests/test_repository.py
```

### Executar com saída detalhada
```powershell
python -m pytest -v
```
