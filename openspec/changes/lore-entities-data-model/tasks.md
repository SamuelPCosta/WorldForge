## 1. Modelos de Dados JSON e Persistência Local

- [ ] 1.1 Definir e implementar os esquemas e modelos Python (dataclasses/Pydantic) para `Character`, `Location`, `Faction` e `Relationship` e verificar validação com testes unitários
- [ ] 1.2 Implementar o repositório local `WorldRepository` para carregar, salvar e manter a integridade referencial em arquivos JSON e verificar salvamento/carregamento correto

## 2. Interface Gráfica e Navegação PyQt

- [ ] 2.1 Criar views PyQt para listar e visualizar detalhes de entidades (`EntityDetailView`) com links interativos de relacionamento e verificar renderização das fichas
- [ ] 2.2 Criar diálogos de formulário (`EntityEditorDialog` e `RelationshipEditorDialog`) para cadastro e conexão de entidades e verificar inserção/edição via UI
- [ ] 2.3 Implementar o controlador de navegação (`LoreNavigator`) para alternar entre entidades conectadas via hiperlinks na UI e verificar histórico de navegação (voltar/avançar)

## 3. Validação e Testes Integrados

- [ ] 3.1 Executar suíte de testes unitários e de integração validando operação offline completa sem dependência de conexões de rede ou arquivos externos
