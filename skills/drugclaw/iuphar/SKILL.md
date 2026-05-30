---
name: iuphar-pharmacology
description: >
  Query the IUPHAR/BPS Guide to Pharmacology REST API for drug targets, ligands
  (drugs/compounds), and their interactions. Use whenever the user asks about
  pharmacological targets, receptor–ligand relationships, drug mechanisms of
  action, or wants to look up any drug or target name in IUPHAR. Supports
  single entity or batch queries. No API key required.
---

# IUPHAR/BPS Guide to Pharmacology Skill

Query the expert-curated IUPHAR database for ligands (drugs/compounds), targets
(receptors/enzymes/channels), and ligand–target interactions.

- **Source**: <https://www.guidetopharmacology.org/>
- **API docs**: <https://www.guidetopharmacology.org/webServices.jsp>
- **Auth**: None (open access)

## Entity auto-detection

`query_entity(name)` tries ligand search first; if no hits, falls back to
target search.

| Input example | Detected as | What you get |
|---|---|---|
| `morphine` | ligand | ligandId, type, approved status, INN … |
| `5-HT1A receptor` | target | targetId, type, gene IDs, family IDs … |
| `GABA receptor` | target | target info + top 10 ligand–target interactions |

## API

| Function | Input | Returns |
|---|---|---|
| `query_entity(name)` | single entity string | dict with `entity`, `type`, `results`, `interactions` |
| `query_entities(names)` | list of entity strings | `{name: result_dict}` |
| `summarize(result)` | output of `query_entity` | concise human-readable text |
| `search_ligand(name)` | drug/compound name | list of ligand dicts |
| `get_ligand(id)` | numeric ligand ID | full ligand detail dict |
| `search_target(name)` | target name | list of target dicts |
| `get_target(id)` | numeric target ID | full target detail dict |
| `get_interactions(target_id)` | numeric target ID | list of interaction dicts |

## Usage

```python
from importlib.util import spec_from_file_location, module_from_spec
spec = spec_from_file_location("iuphar", "<path>/13_IUPHAR_BPS_Guide_to_Pharmacology.py")
iuphar = module_from_spec(spec); spec.loader.exec_module(iuphar)

# Single query
r = iuphar.query_entity("morphine")
print(iuphar.summarize(r))

# Batch query
results = iuphar.query_entities(["aspirin", "5-HT1A receptor"])
for name, res in results.items():
    print(iuphar.summarize(res))
```

See `if __name__ == "__main__"` block in the `.py` file for more runnable
examples (single ligand, single target, batch, direct ID lookup).

## Key fields returned

**Ligand**: `ligandId`, `name`, `type`, `approved`, `inn`, `species`

**Target**: `targetId`, `name`, `abbreviation`, `type`, `familyIds`, `geneIds`

**Interaction**: `ligandId`, `targetId`, `action`, `affinityRange`, `affinityType`, `endogenous`, `species`
