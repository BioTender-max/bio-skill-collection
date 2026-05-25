# bio-innovation-check

**Step 1: Innovation assessment (创新性检测)**

Estimate whether a research idea is sufficiently novel for a strong methods-style paper by expanding the topic and searching the literature.

## Purpose

1. Generate multiple topic variants and synonyms
2. Search PubMed, bioRxiv, and arXiv q-bio
3. Count and de-duplicate related papers
4. Assign a novelty level
5. Suggest how to sharpen or reposition the idea if needed

## Input Format

```text
topic: [research topic]
```

## Workflow

### Step 1.1: Topic expansion

Use several types of expansions:

1. Core term substitution
2. Phrase re-ordering
3. Parent / child concept expansion
4. Adjacent-domain vocabulary borrowing
5. Method keyword enrichment

Example:

- "spatial multi-omics integration"
- "integration of spatial transcriptomics and proteomics"
- "spatial multi-modal data fusion"

Target output: 15-20 topic variants by default.

### Step 1.2: Literature search

Search these sources:

- PubMed
- bioRxiv
- arXiv q-bio

Suggested pattern:

```python
for variant in topic_variants:
    results = search(variant, platforms=["PubMed", "bioRxiv", "arXiv"])
    all_papers.extend(results)

unique_papers = deduplicate(all_papers, threshold=0.8)
```

### Step 1.3: Novelty scoring

Use a simple first-pass threshold:

```python
if paper_count <= 2:
    level = "strong novelty / methods-journal candidate"
elif paper_count <= 5:
    level = "promising but needs sharpening"
else:
    level = "needs repositioning"
```

This is only a heuristic. Final judgment should still use human reasoning.

### Step 1.4: Repositioning suggestions

If the project is not yet strong enough, suggest improvements from one or more of these angles:

1. Method angle
2. Task angle
3. Data / validation angle
4. Analysis angle

## Output Format

```markdown
# Innovation Assessment Report

## Search Strategy
- Number of variants:
- Search sources:
- Search date:

## Topic Variants
| No. | Variant |
|-----|---------|
| 1 | ... |

## Search Results Summary
| Variant | PubMed | bioRxiv | arXiv | Total |
|---------|--------|---------|-------|-------|
| ... | ... | ... | ... | ... |

## De-duplicated Counts
- Total related studies:
- Published papers:
- Preprints:

## Novelty Decision
- Level:
- Reason:

## Representative Related Work
1. [title]
   - Source:
   - Year:
   - Main method:
   - Overlap with the proposed idea:

## Repositioning Suggestions
1. Method:
2. Task:
3. Data / validation:

## Next Step
- If novelty is strong: continue to Step 2
- If the idea needs sharpening: refine and continue
- If it needs repositioning: redesign before proceeding
```

## Usage

```bash
/bio-innovation-check "spatial multi-omics integration"
```

## Notes

1. Use timeouts because search latency varies by source.
2. De-duplication matters; otherwise novelty will be overestimated or underestimated.
3. Overlap scoring still needs human judgment.
4. Journal-specific novelty expectations can differ by field.
