# ADR 0001 — Separar responsabilidades do `WorldRepository`

- **Status:** Aceito
- **Data:** 2026-09-13
- **Decisores:** Equipe WorldForge

## Contexto

O `WorldRepository` concentra persistência JSON, CRUD em memória, validação e limpeza de referências, buscas, consultas de domínio, geração do grafo de relacionamentos e exportação Markdown. Isso torna alterações em uma dessas áreas capazes de afetar as demais, dificulta testes isolados e deixa a futura UI PyQt dependente de um componente com uma superfície de API excessiva.

Para desenvolvimento assistido por IA, limites explícitos entre módulos são especialmente importantes: cada agente deve poder alterar uma responsabilidade sem inferir ou reproduzir regras que pertencem a outro módulo.

## Decisão

O projeto adotará separação por responsabilidade, com estas fronteiras:

- `WorldRepository`: CRUD, estado em memória e leitura/gravação dos arquivos JSON.
- `LoreIntegrityService`: valida relacionamentos e remove ou reporta referências órfãs após exclusões.
- `LoreQueryService`: busca textual e consultas de domínio, como membros de uma facção e facção governante de um local.
- `LoreExportService`: constrói projeções de grafo/árvore e exporta relatórios Markdown.
- `ui/`: seguirá MVP. As views PyQt emitem somente `pyqtSignal` com DTOs/intenção do usuário; presenters coordenam serviços e devolvem DTOs próprios para exibição. Views não acessam repositórios diretamente.

`WorldRepository` não deverá receber novos algoritmos de consulta, exportação, regras de integridade ou lógica de interface. Durante a migração, fachadas temporárias poderão delegar aos serviços para preservar consumidores existentes; elas serão removidas em uma mudança posterior, após migração dos chamadores.

## Consequências

### Positivas

- Regras de domínio, persistência e apresentação podem ser testadas separadamente.
- A UI pode ser validada sem criar janelas gráficas nem manipular arquivos reais.
- Mudanças em formato de exportação ou busca não exigem alteração da camada de persistência.
- Dependências ficam explícitas, limitando o escopo de mudanças automatizadas ou assistidas por IA.

### Custos e riscos

- Haverá mais módulos e dependências por injeção de construtor.
- A migração exige atualizar testes e consumidores que chamam métodos de consulta diretamente no repositório.
- É necessário definir cuidadosamente transações de persistência para operações de domínio que alteram múltiplas coleções.

## Alternativas consideradas

1. **Manter o repositório como fachada com toda a lógica:** rejeitada porque preserva o acoplamento e a responsabilidade excessiva.
2. **Criar um serviço único `LoreService`:** rejeitada porque apenas deslocaria o componente monolítico.
3. **Aplicar CQRS completo e banco de dados:** rejeitada nesta fase; é desproporcional ao armazenamento offline em JSON.

## Plano de migração

1. Extrair integridade, consultas e exportação para os serviços definidos acima e cobri-los com testes unitários.
2. Migrar os testes existentes e os futuros presenters para depender dos serviços.
3. Manter compatibilidade delegada apenas enquanto houver consumidores do repositório legado.
4. Remover as fachadas legadas e atualizar o diagrama para a arquitetura-alvo.
