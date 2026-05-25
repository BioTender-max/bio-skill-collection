# Dashboard QA Checklist (Definition of Done)

## Visual & UX

- [ ] Page has a clear title + “last updated”
- [ ] Filters are grouped and have sensible defaults
- [ ] Layout uses consistent spacing and alignment
- [ ] Cards/sections have clear headings
- [ ] Charts have readable titles and axis labels (or units in title)
- [ ] Tooltips include units and clean formatting
- [ ] Legend placement is consistent and not covering data
- [ ] No chart is “rainbow colored” without meaning
- [ ] Empty states are handled (no blank white cards)
- [ ] Mobile/tablet view is usable (no horizontal scroll unless intentional)

## Interaction

- [ ] Interactions are predictable (click-to-filter is obvious and reversible)
- [ ] There is a clear “reset/clear” action for complex filtering
- [ ] Dashboard state (selected filters) is visible

## Performance

- [ ] Common interactions feel fast (< ~300ms when possible)
- [ ] Expensive work is cached or moved to background callbacks
- [ ] Large tables use virtualization / AG Grid
- [ ] No callback chains that create “spaghetti” dependencies

## Code quality

- [ ] Project has a clear structure (pages/components/callbacks/utils)
- [ ] Callbacks are small and readable
- [ ] Reusable figure helpers exist (no repeated styling code)
- [ ] Requirements are pinned or versioned appropriately

## Documentation

- [ ] README includes:
  - purpose and audience
  - how to run locally
  - configuration/env vars
  - data sources
  - screenshots (or GIF)
- [ ] Data dictionary defines key metrics
- [ ] Known caveats are documented

