<!--
# COPYRIGHT NOTICE
# This file is part of the "Universal Biomedical Skills" project.
# Copyright (c) 2026 MD BABU MIA, PhD <md.babu.mia@mssm.edu>
# All Rights Reserved.
#
# This code is proprietary and confidential.
# Unauthorized copying of this file, via any medium is strictly prohibited.
#
# Provenance: Authenticated by MD BABU MIA

-->

# Quick Architecture Overview

## System Architecture (Simplified)

```
┌─────────────────────────────────────────────────────────────┐
│                        Clients                               │
├─────────────┬──────────────┬──────────────┬─────────────────┤
│     CLI     │    Claude    │  Python SDK  │  Custom Client  │
└──────┬──────┴──────┬───────┴──────┬───────┴─────────┬───────┘
       │             │              │                 │
       └─────────────┴──────────────┴─────────────────┘
                            │
                    ┌───────▼────────┐
                    │   BioMCP Core   │
                    │  (MCP Server)   │
                    └───────┬────────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
┌───────▼────────┐ ┌────────▼────────┐ ┌───────▼────────┐
│ Article Handler │ │  Trial Handler  │ │ Variant Handler │
└───────┬────────┘ └────────┬────────┘ └───────┬────────┘
        │                   │                   │
┌───────▼────────┐ ┌────────▼────────┐ ┌───────▼────────┐
│ PubMed/PubTator│ │ ClinicalTrials  │ │  MyVariant.info │
│   cBioPortal   │ │    NCI CTS      │ │   AlphaGenome   │
└────────────────┘ └─────────────────┘ └────────────────┘
```

## Data Flow

```
User Query → Think → Plan → Search → Enrich → Format → Response
     │                        │         │                    │
     └────────────────────────┴─────────┴────────────────────┘
                          Cache Layer
```

## Quick Command Flow

```
$ biomcp article search --gene BRAF
         │
         ▼
    Parse Args → Validate → Route to Handler
                               │
                               ▼
                         Check Cache
                          Hit? │ Miss?
                           │   │
                           │   └→ Fetch from API → Store
                           │                         │
                           └─────────────────────────┘
                                       │
                                       ▼
                                Format & Return
```


<!-- AUTHOR_SIGNATURE: 9a7f3c2e-MD-BABU-MIA-2026-MSSM-SECURE -->