# Authoritative sources to check (by domain)

Use these as “sources of truth” when the user asks for the **most recent** taxonomy proposals, releases, or consensus statements.

Rule: for “most recent” claims, record **(authority + identifier + date)**.

---

## Bacteria + Archaea (taxonomy + nomenclature)

### NCBI Taxonomy (curated taxonomy + schema announcements)
- NCBI Taxonomy guide / overview:
  https://www.ncbi.nlm.nih.gov/sites/guide/taxonomy/
- NCBI Insights taxonomy announcements (watch for rank schema and lineage-wide changes):
  https://ncbiinsights.ncbi.nlm.nih.gov/tag/ncbi-taxonomy/

What to extract:
- dates + scope of announced changes
- rank schema changes (domain/superkingdom/kingdom/etc.)
- notes about taxid merges/deletions and compatibility

Machine-readable dumps:
- NCBI taxdump / nodes.dmp / names.dmp (discover current FTP location via the guide above)

### GTDB (Genome Taxonomy Database) (genome-based prokaryote taxonomy)
- GTDB portal:
  https://gtdb.ecogenomic.org/
- Latest release stats (confirm current release ID and date):
  https://gtdb.ecogenomic.org/stats/
- Downloads index (confirm release folders):
  https://data.gtdb.ecogenomic.org/releases/

What to extract:
- release ID + date (e.g., “Rxx-RSyyy”)
- high-level naming changes (phyla/classes) and summary statistics
- guidance on GTDB vs NCBI mapping differences (when provided)

### ICNP / ICSP (nomenclature governance for prokaryotes)
- ICSP code page (locate current code edition and changes):
  https://the-icsp.org/index.php/code-of-nomenclatur

Optional name validity lookup:
- LPSN:
  https://lpsn.dsmz.de/

What to extract:
- official code changes affecting ranks and valid publication
- any committee statements relevant to “accepted” names vs database usage

---

## Viruses

### ICTV (International Committee on Taxonomy of Viruses)
- ICTV taxonomy portal:
  https://ictv.global/taxonomy
- Master Species List (MSL) downloads (treat as the current “ratified species list”):
  https://ictv.global/msl

What to extract:
- current MSL version identifier + date
- latest “ratified changes” paper(s) and scope
- notes about binomial species naming and any rank additions/changes (realm/kingdom/etc.)

### NCBI taxonomy (virus alignment with ICTV)
- NCBI Insights taxonomy posts:
  https://ncbiinsights.ncbi.nlm.nih.gov/tag/ncbi-taxonomy/

What to extract:
- implementation dates for virus taxonomy updates in NCBI
- compatibility notes (how old names are retained as synonyms/children)

---

## Eukaryotes

### Broad eukaryote classification frameworks (consensus-style)
- Adl et al. (2019) revised eukaryote classification (ISOP context):
  https://doi.org/10.1111/jeu.12691

Follow-ups:
- When asked “is there an updated version?”, search for:
  - “Revisions to the classification, nomenclature, and diversity of eukaryotes” + newer year
  - “International Society of Protistologists” + “classification” + update/erratum

### UniEuk (community framework, especially for protists)
- UniEuk:
  https://unieuk.net/

### Downstream reference taxonomy implementations
- SILVA eukaryotic taxonomy project:
  https://beta.arb-silva.de/projects/eukaryotic-taxonomy

What to extract:
- whether UniEuk updates were incorporated (and when)
- recommended names/lineages used in environmental sequencing pipelines
