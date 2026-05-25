# QA checklist (taxonomy work is fragile)

Use this before delivering results.

---

## Release/version hygiene
- [ ] Every “most recent” claim includes authority + identifier + date.
- [ ] Every classification output includes tool + database/reference versions.
- [ ] If the user asked for “latest”, you actually checked the authoritative source pages.

## Environment hygiene
- [ ] QuickClade runs note the **container image tag** (and digest if available).
- [ ] QuickClade was run with `percontig` for assemblies or mixed-bin inputs.
- [ ] GTDB-Tk routes passed `gtdbtk check_install` with the intended `GTDBTK_DATA_PATH`.
- [ ] Pixi environment is reproducible (pixi.toml present; lockfile if used).

## Identifier hygiene
- [ ] NCBI taxids included where relevant.
- [ ] TaxonKit warnings (merged/deleted taxids) are surfaced, not ignored.
- [ ] Names are not used as join keys without IDs.

## Rank hygiene
- [ ] “No rank” clades preserved (not coerced).
- [ ] Viral realm/domain differences handled explicitly.
- [ ] Report distinguishes taxonomy vs nomenclature vs informal group names.

## Cross-validation
- [ ] Prokaryotes: GTDB-Tk vs NCBI taxonomy mismatches flagged.
- [ ] Viruses: vConTACT3 clustering interpreted with ICTV context.
- [ ] Euks: EukCC used instead of bacterial QC marker toolchains.

## Output usability
- [ ] Results include a machine-readable table (TSV/CSV/JSON).
- [ ] Caveats and uncertainty are explicit.
