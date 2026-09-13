## Why

Aspirantes a escritores, mestres de RPG e criadores de mundos frequentemente necessitam de uma ferramenta desktop 100% offline e estruturada para organizar elementos complexos de *worldbuilding* (personagens, locais e facções) e suas interconexões de maneira rápida, persistida em arquivos JSON locais, sem dependência de acesso à internet, serviços na nuvem ou gerenciamento manual de imagens.

## What Changes

- Definição do modelo de dados JSON padronizado para as entidades fundamentais de lore: Personagens (`Character`), Locais (`Location`) e Facções (`Faction`).
- Definição da estrutura de relacionamentos direcionados e tipados entre entidades (ex: Personagem pertence a Facção, Personagem reside em Local, Facção controla Local).
- Especificação de persistência offline em arquivos JSON locais com validação de integridade referencial entre entidades e relacionamentos.
- Estruturação inicial da arquitetura da interface gráfica (PyQt) para cadastro, visualização, filtragem e navegação fluida por hiperlinks/conexões entre entidades.

## Capabilities

### New Capabilities

- `lore-entities`: Permite cadastrar, editar, interconectar e navegar entre entidades de lore (personagens, locais e facções) através de um modelo de dados estruturado em arquivos JSON locais e interface gráfica em PyQt.

### Modified Capabilities

*(Nenhuma capacidade existente modificada nesta versão inicial)*

## Impact

- **Armazenamento e Persistência**: Criação do esquema de arquivos JSON locais no projeto WorldForge.
- **Interface Gráfica**: Definição inicial de componentes PyQt para gerenciamento e navegação gráfica das entidades e seus relacionamentos.
- **Segurança e Confiabilidade**: Operação estritamente local (offline), garantindo privacidade e controle total dos dados ao criador.
