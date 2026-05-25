# COPYRIGHT NOTICE
# This file is part of the "Universal Biomedical Skills" project.
# Copyright (c) 2026 MD BABU MIA, PhD <md.babu.mia@mssm.edu>
# All Rights Reserved.
#
# This code is proprietary and confidential.
# Unauthorized copying of this file, via any medium is strictly prohibited.
#
# Provenance: Authenticated by MD BABU MIA

import os
import re
import glob
import json
import gradio as gr
from agents.Biomaster import Biomaster

# Global manager object, convenient for sharing between different button callbacks
manager = None

def parse_datalist(datalist_text: str):
    """Convert multi-line string to list, removing empty lines."""
    return [line.strip() for line in datalist_text.splitlines() if line.strip()]

def load_knowledge_file(file_path):
    """Read knowledge file and return contents"""
    try:
        # If file doesn't exist, create an empty JSON array
        if not os.path.exists(file_path):
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump([], f)
            return []
            
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data
    except Exception as e:
        return {"error": str(e)}

def show_plan_knowledge():
    """Show Plan Knowledge content"""
    knowledge_data = load_knowledge_file("./doc/Plan_Knowledge.json")
    
    # Build HTML table
    html = """
    <div id="knowledge-title">Plan Knowledge</div>
    <style>
    .knowledge-table {
        width: 100%;
        border-collapse: collapse;
        margin-bottom: 20px;
    }
    .knowledge-table th, .knowledge-table td {
        border: 1px solid #ddd;
        padding: 8px;
        vertical-align: top;
    }
    .knowledge-table th {
        background-color: #f2f2f2;
        text-align: left;
    }
    .knowledge-table tr:nth-child(even) {
        background-color: #f9f9f9;
    }
    .content-cell {
        max-height: 150px;
        overflow-y: auto;
        display: block;
    }
    </style>
    <table class="knowledge-table">
    <tr>
        <th style="width:15%">Source</th>
        <th style="width:10%">Page</th>
        <th style="width:75%">Content</th>
    </tr>
    """
    
    if "error" in knowledge_data:
        html += f"<tr><td colspan='3'>Error loading file: {knowledge_data['error']}</td></tr>"
    else:
        # Assume knowledge file is an array
        for i, item in enumerate(knowledge_data):
            source = item.get("metadata", {}).get("source", "")
            page = item.get("metadata", {}).get("page", "")
            content = item.get("content", "").replace("\n", "<br>")
            
            html += f"""
            <tr>
                <td>{source}</td>
                <td>{page}</td>
                <td><div class="content-cell">{content}</div></td>
            </tr>
            """
    
    html += """</table>"""
    return gr.update(value=html)

def show_task_knowledge():
    """Show Task Knowledge content"""
    knowledge_data = load_knowledge_file("./doc/Task_Knowledge.json")
    
    # Build HTML table
    html = """
    <div id="knowledge-title">Task Knowledge</div>
    <style>
    .knowledge-table {
        width: 100%;
        border-collapse: collapse;
        margin-bottom: 20px;
    }
    .knowledge-table th, .knowledge-table td {
        border: 1px solid #ddd;
        padding: 8px;
        vertical-align: top;
    }
    .knowledge-table th {
        background-color: #f2f2f2;
        text-align: left;
    }
    .knowledge-table tr:nth-child(even) {
        background-color: #f9f9f9;
    }
    .content-cell {
        max-height: 150px;
        overflow-y: auto;
        display: block;
    }
    </style>
    <table class="knowledge-table">
    <tr>
        <th style="width:15%">Source</th>
        <th style="width:10%">Page</th>
        <th style="width:75%">Content</th>
    </tr>
    """
    
    if "error" in knowledge_data:
        html += f"<tr><td colspan='3'>Error loading file: {knowledge_data['error']}</td></tr>"
    else:
        # Assume knowledge file is an array
        for i, item in enumerate(knowledge_data):
            source = item.get("metadata", {}).get("source", "")
            page = item.get("metadata", {}).get("page", "")
            content = item.get("content", "").replace("\n", "<br>")
            
            html += f"""
            <tr>
                <td>{source}</td>
                <td>{page}</td>
                <td><div class="content-cell">{content}</div></td>
            </tr>
            """
    
    html += """</table>"""
    return gr.update(value=html)

def hide_knowledge():
    """Hide knowledge display area"""
    return gr.update(visible=False)

def generate_plan(api_key, base_url, goal, datalist, sample_id):
    """
    First button: Generate Plan
    Call manager.execute_PLAN(goal, datalist), and return status message.
    """
    global manager
    # Create a new Biomaster instance each time a Plan is generated
    manager = Biomaster(api_key, base_url, excutor=True, id=sample_id)
    manager.execute_PLAN(goal, parse_datalist(datalist))
    return "Plan generated."

def execute_plan(api_key, base_url, goal, datalist, sample_id):
    """
    Second button: Execute Plan
    Call manager.execute_TASK(datalist), and return status message.
    """
    global manager
    # If manager hasn't been created yet, create it here
    if manager is None:
        manager = Biomaster(api_key, base_url, excutor=True, id=sample_id)
    manager.execute_TASK(parse_datalist(datalist))
    return "Plan executed."

def stop_task():
    """
    Third button: Stop task
    Call manager.stop().
    """
    global manager
    if manager is not None:
        manager.stop()
        return "Task stopped."
    return "No running task."

def load_outputs(api_key, base_url, goal, datalist_text, sample_id):
    """
    Load and display current outputs:
    1) {id}_PLAN.json
    2) The maximum step number corresponding to {id}_Step_{step_number}.sh
    3) Corresponding {id}_Debug_Output_{step_number}.json
    4) List all files in ./output/{id}/ folder
    """
    # ---------- 1. Read PLAN ----------
    plan_file = f"./output/{sample_id}_PLAN.json"
    plan_content = ""
    if os.path.exists(plan_file):
        with open(plan_file, "r", encoding="utf-8") as f:
            plan_content = f.read()

    # ---------- 2. Find the maximum step_number ----------
    step_sh_files = glob.glob(f"./output/{sample_id}_Step_*.sh")
    max_step = 0
    for file_path in step_sh_files:
        match = re.search(r"_Step_(\d+)\.sh$", file_path)
        if match:
            step_num = int(match.group(1))
            if step_num > max_step:
                max_step = step_num

    # Read corresponding step.sh content
    step_content = ""
    if max_step > 0:
        step_file = f"./output/{sample_id}_Step_{max_step}.sh"
        if os.path.exists(step_file):
            with open(step_file, "r", encoding="utf-8") as f:
                step_content = f.read()

    # ---------- 3. Read Debug_Output_{step_number}.json ----------
    debug_content = ""
    if max_step > 0:
        debug_file = f"./output/{sample_id}_DEBUG_Output_{max_step}.json"
        if os.path.exists(debug_file) and os.path.getsize(debug_file) > 0:
            with open(debug_file, "r", encoding="utf-8") as f:
                debug_content = f.read()

    # ---------- 4. List all files in ./output/{sample_id}/ folder ----------
    folder_path = f"./output/{sample_id}/"
    all_files_str = ""
    if os.path.isdir(folder_path):
        files_in_dir = os.listdir(folder_path)
        all_files_str = "\n".join(files_in_dir)

    # Dynamically update labels based on found step_number
    if max_step > 0:
        step_label = f"STEP {max_step}.sh Content"
        debug_label = f"DEBUG {max_step}.json Content"
    else:
        step_label = "STEP .sh Content (Not found)"
        debug_label = "DEBUG .json Content (Not found)"

    return [
        plan_content,                           # Block 1: PLAN
        gr.update(value=step_content, label=step_label),   # Block 2: STEP
        gr.update(value=debug_content, label=debug_label), # Block 3: DEBUG
        all_files_str                           # Block 4: Folder contents
    ]

def save_plan_content(plan_content, sample_id):
    """Save PLAN content to file"""
    # Check if it conforms to JSON format
    try:
        json.loads(plan_content)  # Try parsing JSON
    except json.JSONDecodeError:
        return gr.Warning("Save failed: Content is not in JSON format").then(
            lambda: None, None, None  # Return None to prevent text box content from being modified
        )
    
    plan_file = f"./output/{sample_id}_PLAN.json"
    try:
        with open(plan_file, "w", encoding="utf-8") as f:
            f.write(plan_content)
        return gr.Info("PLAN saved successfully")
    except Exception as e:
        return gr.Warning(f"Save failed: {str(e)}")

def save_step_content(step_content, sample_id):
    """Save STEP content to file"""
    # Find the maximum step_number
    step_sh_files = glob.glob(f"./output/{sample_id}_Step_*.sh")
    max_step = 0
    for file_path in step_sh_files:
        match = re.search(r"_Step_(\d+)\.sh$", file_path)
        if match:
            step_num = int(match.group(1))
            if step_num > max_step:
                max_step = step_num
    
    if max_step > 0:
        step_file = f"./output/{sample_id}_Step_{max_step}.sh"
        try:
            with open(step_file, "w", encoding="utf-8") as f:
                f.write(step_content)
            return gr.Info(f"STEP {max_step}.sh saved successfully")
        except Exception as e:
            return gr.Warning(f"Save failed: {str(e)}")
    else:
        return gr.Warning("STEP file not found, cannot save")

def save_debug_content(debug_content, sample_id):
    """Save DEBUG content to file"""
    # Check if it conforms to JSON format
    try:
        json.loads(debug_content)  # Try parsing JSON
    except json.JSONDecodeError:
        return gr.Warning("Save failed: Content is not in JSON format").then(
            lambda: None, None, None  # Return None to prevent text box content from being modified
        )
    
    # Find the maximum step_number
    step_sh_files = glob.glob(f"./output/{sample_id}_Step_*.sh")
    max_step = 0
    for file_path in step_sh_files:
        match = re.search(r"_Step_(\d+)\.sh$", file_path)
        if match:
            step_num = int(match.group(1))
            if step_num > max_step:
                max_step = step_num
    
    if max_step > 0:
        debug_file = f"./output/{sample_id}_DEBUG_Output_{max_step}.json"
        try:
            with open(debug_file, "w", encoding="utf-8") as f:
                f.write(debug_content)
            return gr.Info(f"DEBUG {max_step}.json saved successfully")
        except Exception as e:
            return gr.Warning(f"Save failed: {str(e)}")
    else:
        return gr.Warning("DEBUG file not found, cannot save")

def add_knowledge_entry(knowledge_type, source, page, content):
    """Add a new knowledge entry to the corresponding knowledge base file"""
    # knowledge_type is now directly 'plan' or 'task'
    if knowledge_type == "plan":
        file_path = "./doc/Plan_Knowledge.json"
    else:
        file_path = "./doc/Task_Knowledge.json"
    
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        new_entry = {
            "content": content,
            "metadata": {
                "source": source,
                "page": page
            }
        }
        
        data.append(new_entry)
        
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        
        # Return updated HTML
        if knowledge_type == "plan":
            return show_plan_knowledge(), gr.update(visible=False)
        else:
            return show_task_knowledge(), gr.update(visible=False)
    
    except Exception as e:
        return gr.update(value=f"<div style='color:red'>Addition failed: {str(e)}</div>"), gr.update(visible=True)

with gr.Blocks(css="""
    #hide-btn {
        position: fixed;
        left: 10px;
        top: 55%;
        z-index: 300; /* Highest level */
        transform: translateY(-50%);
        font-size: 1em !important;
        padding: 0.6em 1em !important;
        opacity: 0.9;
        border-radius: 4px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.2);
        width: auto !important;
        min-width: 100px !important;
        max-width: 150px !important;
        background-color: #607d8b !important;
        color: white !important;
        font-weight: bold !important;
    }
    #hide-btn:hover {
        opacity: 1;
        background-color: #455a64 !important;
        box-shadow: 0 4px 8px rgba(0,0,0,0.3);
    }
    #add-btn {
        position: fixed;
        left: 10px;
        top: 45%;
        z-index: 300; /* Highest level */
        transform: translateY(-50%);
        font-size: 1em !important;
        padding: 0.6em 1em !important;
        opacity: 0.9;
        border-radius: 4px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.2);
        width: auto !important;
        min-width: 100px !important;
        max-width: 150px !important;
        background-color: #8bc34a !important;
        color: white !important;
        font-weight: bold !important;
    }
    #add-btn:hover {
        opacity: 1;
        background-color: #689f38 !important;
        box-shadow: 0 4px 8px rgba(0,0,0,0.3);
    }
    #knowledge-overlay {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-color: rgba(255, 255, 255, 0.97);
        z-index: 200; /* Middle level */
        padding: 30px;
        overflow-y: auto;
        box-shadow: 0 0 15px rgba(0,0,0,0.3);
    }
    #knowledge-title {
        font-size: 1.5em;
        font-weight: bold;
        margin-bottom: 15px;
        padding-bottom: 10px;
        border-bottom: 1px solid #ddd;
    }
    #add-form {
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        background-color: white;
        padding: 20px;
        border-radius: 8px;
        box-shadow: 0 0 20px rgba(0,0,0,0.4);
        z-index: 400; /* Highest level */
        width: 60%;
        max-width: 600px;
    }
    .main-content {
        z-index: 100; /* Lowest level */
        position: relative;
    }
    
    /* Custom button colors */
    .knowledge-btn {
        background-color: #9c27b0 !important;
        color: white !important;
        transition: all 0.3s ease !important;
    }
    .knowledge-btn:hover {
        background-color: #7b1fa2 !important;
        box-shadow: 0 4px 8px rgba(0,0,0,0.3) !important;
    }
    
    .generate-btn {
        background-color: #2196f3 !important;
        color: white !important;
        transition: all 0.3s ease !important;
    }
    .generate-btn:hover {
        background-color: #1976d2 !important;
        box-shadow: 0 4px 8px rgba(0,0,0,0.3) !important;
    }
    
    .execute-btn {
        background-color: #ff9800 !important;
        color: white !important;
        transition: all 0.3s ease !important;
    }
    .execute-btn:hover {
        background-color: #f57c00 !important;
        box-shadow: 0 4px 8px rgba(0,0,0,0.3) !important;
    }
    
    .stop-btn {
        background-color: #f44336 !important;
        color: white !important;
        transition: all 0.3s ease !important;
    }
    .stop-btn:hover {
        background-color: #d32f2f !important;
        box-shadow: 0 4px 8px rgba(0,0,0,0.3) !important;
    }
    
    .load-btn {
        background-color: #4caf50 !important;
        color: white !important;
        transition: all 0.3s ease !important;
    }
    .load-btn:hover {
        background-color: #388e3c !important;
        box-shadow: 0 4px 8px rgba(0,0,0,0.3) !important;
    }
    
    .cancel-btn {
        background-color: #9e9e9e !important;
        color: white !important;
        transition: all 0.3s ease !important;
    }
    .cancel-btn:hover {
        background-color: #757575 !important;
        box-shadow: 0 4px 8px rgba(0,0,0,0.3) !important;
    }
    
    .save-btn {
        background-color: #009688 !important;
        color: white !important;
        transition: all 0.3s ease !important;
    }
    .save-btn:hover {
        background-color: #00796b !important;
        box-shadow: 0 4px 8px rgba(0,0,0,0.3) !important;
    }
""", js="""
function() {
    let intervalId;
    
    // Wait for the page to load
    document.addEventListener("DOMContentLoaded", function() {
        // Set up interval to click the load button every 3 seconds
        intervalId = setInterval(function() {
            const loadButton = document.querySelector('.load-btn');
            if (loadButton) {
                loadButton.click();
            }
        }, 3000); // 3000 milliseconds = 3 seconds
    });
    
    // Return cleanup function
    return () => {
        if (intervalId) clearInterval(intervalId);
    };
}
""") as demo:
    gr.Markdown("## Biomaster")

    # Create hidden sample_id storage for button callbacks
    sample_id_state = gr.State("")
    
    # Knowledge display area (initially hidden, floating on top of the page)
    with gr.Column(visible=False, elem_id="knowledge-overlay") as knowledge_container:
        knowledge_html = gr.HTML()
    
    # Add knowledge form (initially hidden)
    with gr.Column(visible=False, elem_id="add-form") as add_form:
        gr.Markdown("## Add New Knowledge Entry")
        knowledge_type = gr.Radio(["plan", "task"], label="Knowledge Type")
        source_input = gr.Textbox(label="Source")
        page_input = gr.Textbox(label="Page")
        content_input = gr.Textbox(label="Content", lines=5)
        with gr.Row():
            cancel_add_btn = gr.Button("Cancel", elem_classes="cancel-btn")
            save_add_btn = gr.Button("Save", variant="primary", elem_classes="save-btn")
    
    # Floating buttons (initially hidden)
    add_knowledge_btn = gr.Button("Add Knowledge", variant="secondary", visible=False, elem_id="add-btn")
    hide_knowledge_btn = gr.Button("Close Windows", variant="secondary", visible=False, elem_id="hide-btn")
    
    # Main content area (marked as main-content for z-index setting)
    with gr.Column(elem_classes="main-content"):
        # Top knowledge buttons
        with gr.Row():
            with gr.Column(scale=1):
                with gr.Row():
                    plan_knowledge_btn = gr.Button("Plan Knowledge", variant="primary", elem_classes="knowledge-btn")
                    task_knowledge_btn = gr.Button("Task Knowledge", variant="primary", elem_classes="knowledge-btn")
        
        with gr.Row(equal_height=True):
            # Left side inputs and buttons
            with gr.Column(scale=1):
                base_url_in = gr.Textbox(label="Base URL", value="openAI base URL here")
                api_key_in = gr.Textbox(label="API Key", value="your openAI key here")
                goal_in = gr.Textbox(label="Goal", value="please do rna-seq analysis.")
                datalist_in = gr.Textbox(
                    label="Data List (One item per line. Format: Path: Description)",
                    value="data/rnaseq_1.fastq.gz: RNA-Seq read 1 data\n"
                          "data/rnaseq_2.fastq.gz: RNA-Seq read 2 data",
                    lines=5
                )
                sample_id_in = gr.Textbox(label="ID", value="010")

                # 3 new buttons
                generate_plan_button = gr.Button("Generate Plan", elem_classes="generate-btn")
                execute_plan_button = gr.Button("Execute Plan", elem_classes="execute-btn")
                stop_button = gr.Button("STOP Plan", elem_classes="stop-btn")

                # Original "Load and Show" button
                load_button = gr.Button("Load and Show", elem_classes="load-btn")

                # Status message output
                status_box = gr.Textbox(label="Status", lines=2)

            # Right side display area (four blocks from top to bottom)
            with gr.Column(scale=1):
                # First box: PLAN, editable
                with gr.Row():
                    plan_box = gr.Textbox(label="PLAN JSON Content", lines=10, max_lines=10, interactive=True)
                    with gr.Column(scale=0, min_width=100):
                        plan_cancel_btn = gr.Button("Cancel", elem_classes="cancel-btn")
                        plan_save_btn = gr.Button("Save", variant="primary", elem_classes="save-btn")
                
                # Second box: STEP, editable
                with gr.Row():
                    step_box = gr.Textbox(label="STEP .sh Content", lines=5, max_lines=5, interactive=True)
                    with gr.Column(scale=0, min_width=100):
                        step_cancel_btn = gr.Button("Cancel", elem_classes="cancel-btn")
                        step_save_btn = gr.Button("Save", variant="primary", elem_classes="save-btn")
                
                # Third box: DEBUG, editable
                with gr.Row():
                    debug_box = gr.Textbox(label="DEBUG .json Content", lines=5, max_lines=5, interactive=True)
                    with gr.Column(scale=0, min_width=100):
                        debug_cancel_btn = gr.Button("Cancel", elem_classes="cancel-btn")
                        debug_save_btn = gr.Button("Save", variant="primary", elem_classes="save-btn")
                
                # Fourth box: file list, non-editable
                files_box = gr.Textbox(label="Ouput dir Content", lines=5, max_lines=5, interactive=False)

    # Button callbacks - Load and Execute
    generate_plan_button.click(
        fn=generate_plan,
        inputs=[api_key_in, base_url_in, goal_in, datalist_in, sample_id_in],
        outputs=status_box
    )
    execute_plan_button.click(
        fn=execute_plan,
        inputs=[api_key_in, base_url_in, goal_in, datalist_in, sample_id_in],
        outputs=status_box
    )
    stop_button.click(
        fn=stop_task,
        inputs=[],
        outputs=status_box
    )

    # Load and display output files, while updating sample_id_state
    def load_and_update_id(api_key, base_url, goal, datalist, sample_id):
        outputs = load_outputs(api_key, base_url, goal, datalist, sample_id)
        return outputs + [sample_id]  # Return sample_id as additional output

    load_button.click(
        fn=load_and_update_id,
        inputs=[api_key_in, base_url_in, goal_in, datalist_in, sample_id_in],
        outputs=[plan_box, step_box, debug_box, files_box, sample_id_state]
    )

    # PLAN Save and Cancel button callbacks
    plan_save_btn.click(
        fn=save_plan_content,
        inputs=[plan_box, sample_id_state],
        outputs=None
    )
    plan_cancel_btn.click(
        fn=lambda sample_id: load_outputs(None, None, None, None, sample_id)[0],
        inputs=[sample_id_state],
        outputs=plan_box
    )

    # STEP Save and Cancel button callbacks
    step_save_btn.click(
        fn=save_step_content,
        inputs=[step_box, sample_id_state],
        outputs=None
    )
    step_cancel_btn.click(
        fn=lambda sample_id: load_outputs(None, None, None, None, sample_id)[1].value,
        inputs=[sample_id_state],
        outputs=step_box
    )

    # DEBUG Save and Cancel button callbacks
    debug_save_btn.click(
        fn=save_debug_content,
        inputs=[debug_box, sample_id_state],
        outputs=None
    )
    debug_cancel_btn.click(
        fn=lambda sample_id: load_outputs(None, None, None, None, sample_id)[2].value,
        inputs=[sample_id_state],
        outputs=debug_box
    )

    # Knowledge button callbacks
    def show_plan_and_controls():
        return [gr.update(visible=True), gr.update(visible=True), gr.update(visible=True), gr.update(visible=True)]
        
    plan_knowledge_btn.click(
        fn=show_plan_knowledge,
        inputs=[],
        outputs=[knowledge_html]
    ).then(
        fn=show_plan_and_controls,
        inputs=[],
        outputs=[knowledge_html, knowledge_container, add_knowledge_btn, hide_knowledge_btn]
    )
    
    task_knowledge_btn.click(
        fn=show_task_knowledge,
        inputs=[],
        outputs=[knowledge_html]
    ).then(
        fn=show_plan_and_controls,
        inputs=[],
        outputs=[knowledge_html, knowledge_container, add_knowledge_btn, hide_knowledge_btn]
    )
    
    # Hide button callback
    hide_knowledge_btn.click(
        fn=lambda: [gr.update(visible=False), gr.update(visible=False), gr.update(visible=False), gr.update(visible=False)],
        inputs=[],
        outputs=[knowledge_html, knowledge_container, add_knowledge_btn, hide_knowledge_btn]
    )
    
    # Add knowledge button callback
    add_knowledge_btn.click(
        fn=lambda: gr.update(visible=True),
        inputs=[],
        outputs=[add_form]
    )
    
    # Cancel add button callback
    cancel_add_btn.click(
        fn=lambda: gr.update(visible=False),
        inputs=[],
        outputs=[add_form]
    )
    
    # Save add button callback
    save_add_btn.click(
        fn=add_knowledge_entry,
        inputs=[knowledge_type, source_input, page_input, content_input],
        outputs=[knowledge_html, add_form]
    )

if __name__ == "__main__":
    demo.launch(share=True, height=800)
__AUTHOR_SIGNATURE__ = "9a7f3c2e-MD-BABU-MIA-2026-MSSM-SECURE"
