Introduction to BioMaster
=========================

**BioMaster** is an advanced, multi-agent framework designed to automate and manage complex bioinformatics workflows using Large Language Models (LLMs), task decomposition, and retrieval-augmented knowledge integration.

By simulating expert-level reasoning and execution, BioMaster enables fast, reproducible, and accurate analysis across various omics modalities — all without requiring extensive programming skills.

Key Capabilities
----------------

- **🧠 Multi-Agent Collaboration**  
  Specialized agents (Plan, Task, Check, and Debug) work cooperatively to handle planning, execution, validation, and automatic error recovery.

- **⚡ Fully Automated Pipelines**  
  From raw data to final results, BioMaster manages the entire bioinformatics pipeline, including quality control, alignment, quantification, and downstream analysis.

- **🔍 Retrieval-Augmented Generation (RAG)**  
  Combines preloaded domain knowledge and live script/tool documentation to dynamically plan and execute workflows with adaptive flexibility.

- **💡 Robust Debugging & Self-healing Execution**  
  Automatically detects failed steps and regenerates corrected commands using LLM-powered analysis and error recovery.

- **🖥️ Interactive GUI**  
  A user-friendly web interface allows non-expert users to configure tasks, launch pipelines, and review results intuitively.

- **🧩 Extensible & Customizable**  
  Easily integrates custom scripts, tools, or workflows by updating structured knowledge in PLAN/EXECUTE RAG modules.

Supported Workflows
-------------------

BioMaster supports a broad spectrum of omics and sequencing workflows, including but not limited to:

- **🧬 RNA-seq**: DEG analysis, splicing, APA, fusion genes, circRNA, functional enrichment  
- **🔬 ChIP-seq**: Peak calling, motif discovery  
- **🧫 Single-cell RNA-seq (scRNA-seq)**: Clustering, marker gene detection  
- **🗺️ Spatial transcriptomics**: Cell type annotation, SVG detection, neighborhood analysis  
- **🧩 Hi-C**: Mapping, contact matrix construction, loop/TAD detection  
- **🧪 Nanopore & Long-read**: Isoform quantification, methylation calling, de novo assembly  
- **🧬 miRNA & specialized assays**: miRNA detection, Ribo-seq, Bisulfite-seq, DNase-seq, CAGE-seq, metagenomics, and more

For full details and example workflows, visit the GitHub repository or refer to the RAG knowledge base.

Resources
---------

- 🔗 [GitHub Repository](https://github.com/yourusername/BioMaster)
- 📄 [BioRxiv Preprint](https://www.biorxiv.org/content/10.1101/2025.01.23.634608v1.abstract)
- 🧭 [Workflow Knowledge Documentation](../doc/Plan_Knowledge.json)

