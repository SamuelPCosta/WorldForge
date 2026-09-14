```mermaid
flowchart TD
    A["ui<br/>(Camada Gráfica PyQt)"] --> B["services<br/>(Regras de Domínio)"]
    B --> C["repository<br/>(WorldRepository e Repositórios Concretos)"]
    C --> D["models<br/>(BaseEntity, Character, Faction, Location, Relationship)"]
    C --> E[("Persistência Local<br/>JSON & Arquivos em disco")]

    classDef planned fill:#f3f4f6,stroke:#9ca3af,stroke-width:2px,stroke-dasharray: 5 5,color:#4b5563;
    classDef core fill:#e0f2fe,stroke:#0284c7,stroke-width:2px,color:#0369a1;
    class A,B planned;
    class C,D,E core;