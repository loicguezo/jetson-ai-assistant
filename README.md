# AI-Assistant

## workflow

```mermaid
graph TD
    classDef default fill:#fffdf5,stroke:#2b2b2b,stroke-width:2px,color:#2b2b2b,font-family:'Chalkboard SE', 'Comic Sans MS', cursive, sans-serif;
    classDef cloud fill:#f0f7ff,stroke:#3b82f6,stroke-width:2px,stroke-dasharray: 4 4,color:#1e3a8a;

    CAM(Camera) --> VLA[VLA]
    CAM --> STT[Speech-To-Text STT]
    CAM --> LLM{LLM / VLM<br>Gemma4}

    VLA --> REC[Recenter camera if<br>human detected]
    VLA --> JSON[JSON description of<br>all detected beings]

    STT --> LLM
    JSON --> LLM

    LLM <--> MCP[MCP Servers]
    LLM <--> RAG[RAG System]
    subgraph Resources
        subgraph Local Storage
            RAG <--> VDB[(Vectorial Database)]
        end

        subgraph External Sources
            RAG <--> NET[Internet / Web Search]
            RAG <--> OTH[Other Specialized AIs]
        end
    end

%%    subgraph Cloud Storage
%%        SUP[(Supabase pgvector)]
%%    end

%%    VDB -.->|Offline-First<br>Async Sync| SUP

    class SUP cloud;
```

## links

- [jetson containers](https://github.com/dusty-nv/jetson-containers)
- [jetson ai labs](https://www.jetson-ai-lab.com)
- [Ultralytics](https://docs.ultralytics.com/guides/deepstream-nvidia-jetson#what-is-nvidia-deepstream)
