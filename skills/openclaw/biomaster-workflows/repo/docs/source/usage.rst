How to Use BioMaster
====================

BioMaster can be used both via **command-line (CLI)** and through a **graphical user interface (GUI)**. It supports fully automated multi-agent orchestration and task execution with detailed output tracking.

Using from Terminal (CLI)
-------------------------

1. **Configure your environment**

   - Ensure dependencies are installed:
     
     .. code-block:: bash

        conda create -n agent python=3.12
        conda activate agent
        pip install -r requirements.txt

   - Set your OpenAI API key and base URL in `run.py` or `examples/file.py`.

2. **Prepare your working directory**

   - Move the example script (e.g. `examples/file.py`) into the root folder:

     .. code-block:: bash

        mv examples/file.py ./BioMaster/

   - Download and place required data in the `./data/` directory:
   
     - Example dataset: https://drive.google.com/drive/folders/1vA3WIAVXVo4RZSqXKsItEZHVaBgIIv_E?usp=sharing

3. **Set a unique task ID** in your script:

   .. code-block:: python

      manager = Biomaster(api_key, base_url, excutor=True, id='001')

4. **Run the script**

   .. code-block:: bash

      conda activate agent
      python run.py

   Or, for examples:

   .. code-block:: bash

      python example1.py

5. **Inspect the output**

   Results are saved in the following structure:

   - Execution plan: ``./output/{id}_PLAN.json``
   - Execution scripts: ``./output/{id}_Step_{step}.sh``
   - Step logs: ``./output/{id}_DEBUG_Output_{step}.json``
   - All files: ``./output/{id}/``

Using from UI (GUI)
-------------------

1. **Start the GUI**

   .. code-block:: bash

      conda activate agent
      python runv.py

2. **Open the browser**

   Navigate to:

   .. code-block:: none

      http://127.0.0.1:7860/

3. **Interactively configure your task**

   - Set your **API Key** and **Base URL**
   - Assign a unique **Task ID**
   - Specify your **data paths**
   - Define your **goal** (e.g., "WGS variant calling")
   - Click **"Generate Plan"**, then **"Execute Plan"**

4. **View and manage results**

   - Click **"Load and Show"** to inspect results
   - Click **"Stop PLAN"** to interrupt an ongoing task

Output Format
-------------

BioMaster generates structured outputs:

- **Execution Plan**:  
  ``output/{id}_PLAN.json`` – Full step-by-step plan

- **Execution Scripts**:  
  ``output/{id}_Step_{n}.sh`` – Shell script per step

- **Execution Logs**:  
  ``output/{id}_DEBUG_Output_{n}.json`` – Debug output with execution status

- **Data Output Directory**:  
  ``output/{id}/`` – Folder containing all intermediate and final results

Tips & Recommendations
----------------------

- Always use a **unique task ID** to avoid overwriting previous results.
- To modify the generated plan or script:
  
  - Comment out `manager.execute_PLAN(...)` and edit `output/{id}_PLAN.json`
  - Edit `Step_{n}.sh` to revise any command
  - Re-run `python run.py` to resume

- To retry a failed step, delete or set `stats: false` in its `DEBUG_Output_{n}.json`

- Before adding new tools or workflows, update the **PLAN RAG** or **EXECUTE RAG** JSON files in `./doc/`, then delete `./chroma_db/` to refresh embeddings.
