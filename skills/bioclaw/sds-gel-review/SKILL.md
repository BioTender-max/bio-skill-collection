---
name: sds-gel-review
description: Review SDS-PAGE or protein purification gel images using DNA sequence, protein sequence, base-pair length, expected protein size, and lane labels. Use when the user wants to judge whether a gel ran well, whether the main band matches the expected product, or whether there may be impurities, degradation, aggregation, or low expression.
---

# SDS-Gel Review

Use this skill when the user provides a gel image plus any of:

- DNA sequence
- protein sequence
- coding sequence length in bp
- expected protein size in kDa
- tag, construct, host, purification step, or lane labels

This is an interpretation skill, not a definitive assay. Distinguish what is directly observed from what is inferred.

## Main goal

Given a gel image and partial sequence/context, produce a practical lab-style judgment:

- did the gel run cleanly or poorly
- is there a plausible main band
- does the main band roughly match the expected target
- are there obvious impurities, degradation, smearing, or aggregation
- what extra information would most improve confidence

## Inputs to request or infer

Collect as many of these as possible before judging:

- gel image
- whether the image is SDS-PAGE, western blot, or native gel
- DNA sequence or protein sequence
- if only bp is given, whether it is coding sequence length
- expected protein name
- expected molecular weight in kDa
- expression host
- tag or fusion partner
- purification step or lane meaning
- whether reducing conditions were used
- whether a ladder is visible

If some are missing, continue with a lower-confidence interpretation.

## How to reason

### 1. Normalize the sequence information

- If the user provides a protein sequence, use it directly.
- If the user provides a DNA sequence, treat it as coding sequence only if the context supports that.
- If the user provides only bp length, estimate protein length as `bp / 3` aa only when it is likely a coding region.
- Estimate theoretical protein mass with the rough rule `110 Da per amino acid`.
- Convert to kDa and note that tags, signal peptides, cleavage, glycosylation, oligomerization, and unusual composition may shift apparent migration.

### 2. Read the gel image conservatively

Inspect the image for:

- lane count and lane boundaries
- visible labels above or below lanes
- presence or absence of ladder
- strongest band in each relevant lane
- approximate relative migration of the strongest band
- extra lower bands suggesting degradation
- extra upper bands suggesting dimers, aggregates, uncleaved fusion, or contaminants
- smearing, overloaded lanes, distorted fronts, or uneven running
- enrichment or loss across purification lanes if the labels indicate flow-through, wash, elution, pellet, or lysate

If the ladder is missing, use labeled lane order and relative migration only. Do not invent exact kDa values.

### 3. Compare expectation vs observation

Decide whether the image most supports one of these:

- likely target band at approximately expected size
- possible target band but confidence limited
- target band not clearly visible
- strong expression but poor purity
- purified sample but with degradation
- aggregation or high-MW species likely
- gel quality too poor for a reliable call

### 4. Explain confidence

Confidence is higher when:

- ladder is visible
- expected protein size is provided
- lane labels are clear
- construct/tag information is available
- the gel has multiple purification steps that tell a consistent story

Confidence is lower when:

- only bp count is provided
- ladder is absent
- lane labels are missing
- image quality is low
- the construct may include tags or cleavage not described

## Important guardrails

- Never claim a precise molecular weight from the image when no ladder is visible.
- Never claim a band is definitely the target protein from DNA length alone.
- Clearly separate:
  - Observation: what the image visibly shows
  - Inference: what might explain it
- If the image quality or metadata are insufficient, say so plainly.
- Prefer practical lab wording over overconfident structural biology language.

## Output format

Use this structure:

### Overall judgment
- One short paragraph on whether the gel looks interpretable and whether the target seems present.

### What I can directly see
- lane pattern
- strongest band(s)
- impurities, smear, aggregation, or degradation
- whether purification appears to improve the sample

### Expected size estimate
- from protein sequence, DNA sequence, or bp count
- state assumptions clearly

### Does the observed band roughly match?
- yes / maybe / unclear / no
- explain why

### Main concerns
- 1 to 3 likely issues only

### What would help next
- ask for the smallest missing item that would improve confidence, such as:
  - ladder annotation
  - lane labels
  - exact coding sequence length
  - tag/fusion information
  - expected kDa
  - original uncropped image

## Practical heuristics

- Approximate aa count from coding sequence: `bp / 3`
- Rough protein mass: `aa * 110 Da`
- His-tag or small peptide tags usually shift size only slightly
- Large fusion tags can meaningfully shift migration
- Smear below the main band often suggests degradation or proteolysis
- Signal near the top or stacking boundary can suggest aggregation or incomplete denaturation
- A very thick single band with little else may still reflect overloading

## Example task types

- "Here is a DNA sequence and SDS-PAGE image. Did my purification work?"
- "This construct is 978 bp. Does the main band in this gel make sense?"
- "I expect a 42 kDa protein. Which lane looks best?"
- "No ladder on this gel, but the lanes are labeled lysate, wash, elution. Please judge whether the elution looks clean."
