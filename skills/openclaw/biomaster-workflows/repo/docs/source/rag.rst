Knowledge Management with RAG
=============================

BioMaster employs a dual Retrieval-Augmented Generation (RAG) system to dynamically access and utilize relevant domain knowledge for planning and execution:

- **PLAN RAG** – Guides high-level workflow decomposition
- **EXECUTE RAG** – Provides detailed tool/script usage for task execution

PLAN RAG
--------

The PLAN Agent retrieves step-by-step analysis workflows using PLAN RAG. To add a new workflow:

1. **Collect a reference**  
   Find a reliable source or protocol (e.g., from nf-core, published papers, or existing pipelines).

2. **Describe the workflow**  
   Use a standardized, concise format that includes:
   
   - **Step description**
   - **Input required (with data format)**
   - **Expected output**
   - **Tools used**

   Example:

   .. code-block:: text

      Step 2: Alignment – Align reads to the reference genome.  
      Input: Cleaned FASTQ files and the reference genome  
      Output: Sorted BAM file  
      Tools: BWA-MEM, STAR

3. **Add entry to `doc/Plan_Knowledge.json`**  
   Use the following JSON format:

   .. code-block:: json

      {
        "content": "Full workflow steps in plain text...",
        "metadata": {
          "source": "workflow",
          "page": 1
        }
      }

EXECUTE RAG
-----------

The TASK Agent uses EXECUTE RAG to generate shell scripts for each step. To contribute:

1. **Document script/tool/function usage**

   - Include input/output specifications
   - Provide example commands
   - Note usage location (e.g., `./scripts/`, `functions.py`)

2. **Add entry to `doc/Task_Knowledge.json`**  
   Example:

   .. code-block:: json

      {
        "content": "run-sort-bam.sh:\nSorts BAM file by coordinate...\nUsage:\nbash ./scripts/run-sort-bam.sh <input.bam> <output_prefix>",
        "metadata": {
          "source": "run-sort-bam.sh",
          "page": 6
        }
      }

Best Practices
--------------

- ✅ Be **specific and concise**
- ✅ Mention **file formats** where applicable
- 🚫 Avoid **redundant or vague** entries
- 🔁 After any change, delete the local vector store:

  .. code-block:: bash

     rm -rf ./chroma_db

- 📌 Use the `metadata.source` field to tag by tool/script/workflow name for better retrieval

Updating Knowledge
------------------

To update or remove knowledge:

- Edit the corresponding JSON file (`Plan_Knowledge.json` or `Task_Knowledge.json`)
- Then delete `./chroma_db/` to force regeneration of knowledge embeddings