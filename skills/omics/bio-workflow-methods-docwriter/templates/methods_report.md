# Workflow Summary
{{workflow_summary}}

**Run ID:** {{run_id}}  
**Date:** {{run_date}}  
**Workflow engine:** {{engine}} {{engine_version}}  
**Pipeline:** {{pipeline_name}} ({{pipeline_version_or_commit}})  
**Container / env:** {{container_or_env_summary}}

---

# Methods and Run Documentation

## 1. Purpose
{{purpose}}

## 2. Inputs
- **Datasets:** {{datasets}}
- **Reference assets:** {{reference_assets}}

## 3. Reproducibility (exact rerun)
```bash
{{exact_rerun_command}}
```

### 3.1 Configuration used
- Params: {{params_files}}
- Config: {{config_files}}

### 3.2 Software environment
- Tool versions: {{tool_versions}}
- Containers/images (name + digest): {{container_digests}}
- Conda env export / lockfile: {{conda_lock_or_export}}

## 4. Workflow steps (as executed)
> Rule: include the verbatim command for each step (or NOT CAPTURED).

{{steps_block}}

## 5. Quality control
{{qc_block}}

## 6. Outputs
{{outputs_block}}

## 7. Limitations / deviations
{{limitations}}

## Appendix A. Evidence files used
{{evidence_inventory}}

