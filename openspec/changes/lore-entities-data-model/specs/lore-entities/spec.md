## Purpose

Permite que criadores de conteúdo cadastrem, editem e interconectem entidades de lore (personagens, locais e facções) em um formato JSON estruturado e naveguem por suas relações offline via PyQt.

## ADDED Requirements

### Requirement: Cadastro e Estruturação de Entidades de Lore
O sistema MUST permitir a criação, leitura, atualização e remoção (CRUD) de entidades do tipo Personagem (`Character`), Local (`Location`) e Facção (`Faction`) armazenadas como arquivos JSON locais.

#### Scenario: Criar nova entidade de personagem com sucesso
- **WHEN** o usuário envia os dados válidos de um novo personagem na interface PyQt
- **THEN** o sistema salva o arquivo JSON correspondente no repositório local e atualiza a lista de entidades disponíveis

#### Scenario: Tentar salvar entidade sem campos obrigatórios
- **WHEN** o usuário tenta salvar uma entidade sem preencher o campo obrigatório `id` ou `name`
- **THEN** o sistema exibe uma mensagem de validação no PyQt e impede a gravação do arquivo JSON

### Requirement: Gestão de Relacionamentos Inter-Entidades
O sistema MUST permitir definir e armazenar conexões direcionadas e tipadas entre quaisquer duas entidades de lore registradas (ex: Personagem A é membro de Facção B, Facção B controla Local C).

#### Scenario: Conectar duas entidades de lore
- **WHEN** o usuário seleciona uma entidade de origem, uma entidade de destino e o tipo de relacionamento
- **THEN** o sistema registra a conexão no modelo JSON e atualiza o mapeamento de relacionamentos da lore

#### Scenario: Remover um relacionamento existente
- **WHEN** o usuário solicita a exclusão de um relacionamento entre duas entidades
- **THEN** o sistema remove a referência do arquivo JSON sem afetar a existência das entidades originais

### Requirement: Navegação Offline por Hiperlinks e Grafo de Relações
O sistema MUST disponibilizar navegação fluida entre entidades na interface PyQt através de links de relacionamento e visualização interativa das conexões offline.

#### Scenario: Navegar para uma entidade vinculada
- **WHEN** o usuário clica em um relacionamento exibido na ficha de uma entidade
- **THEN** o sistema carrega e exibe imediatamente a ficha detalhada da entidade de destino sem requisições externas à rede
