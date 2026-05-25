# survival-analysis

Time-to-event analysis for cancer clinical data. Covers the full pipeline from Kaplan-Meier estimation through Cox regression, competing risks, and RMST.

```mermaid
graph TD
    A["survival-analysis<br>SKILL.md"] --> B["Kaplan-Meier<br>ggsurvfit · log-rank"]
    A --> C["Cox PH<br>coxph · cox.zph"]
    A --> D["Competing risks<br>tidycmprsk · Fine-Gray"]
    A --> E["RMST<br>survRM2"]
    A --> F["Cutpoints & forest plots<br>maxstat · forestmodel"]
    style A fill:#1a1a2e,stroke:#00d9ff,color:#fff,stroke-width:2px
    style B fill:#1a1a2e,stroke:#4ecdc4,color:#fff,stroke-width:2px
    style C fill:#1a1a2e,stroke:#ff6b6b,color:#fff,stroke-width:2px
    style D fill:#1a1a2e,stroke:#87b13f,color:#fff,stroke-width:2px
    style E fill:#1a1a2e,stroke:#276DC3,color:#fff,stroke-width:2px
    style F fill:#1a1a2e,stroke:#e84d3c,color:#fff,stroke-width:2px
```

## Usage

```bash
# Claude Code
cp SKILL.md your-project/.claude/skills/

# Cursor
cp SKILL.md your-project/.cursor/skills/
```

## Methods covered

| Method | Package | Use case |
|--------|---------|----------|
| Kaplan-Meier | survival, ggsurvfit | Non-parametric survival curves with risk tables |
| Log-rank test | survival | Two-group or multi-group comparison |
| Cox PH | survival | Multivariate hazard ratio estimation |
| PH diagnostics | survival (cox.zph) | Schoenfeld residuals, time-varying coefficients |
| Competing risks | tidycmprsk | Cause-specific and Fine-Gray subdistribution hazards |
| RMST | survRM2 | Alternative to HR when PH violated |
| Optimal cutpoints | survminer, maxstat | Data-driven biomarker thresholds (with validation caveats) |
| Forest plots | forestmodel | Multivariate Cox results visualization |
