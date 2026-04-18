# Deadlock Ontology PoC

## Authoritative docs
- docs/HEURISTICS.md is classification policy
- docs/PROMPT.md is the task spec
- Follow both verbatim; do not rediscover known facts

## Hard rules
- NEVER cat, head, or read .vdata files into your context.
  They are large and regular — parse them in Python and emit aggregates only.
- All file reading goes through src/kv3_parser.py
- Outputs go to outputs/ as markdown/jsonl, never inline in chat
- Process ONE .vdata file per session. Heroes first.
- Preserve the "Modifer" typo verbatim. Do not autocorrect.
- Quarantine over delete: unknowns.jsonl is the safety net

## Workflow per file
1. Parse → emit generic_data_type, entity count, leaf-class histogram
2. Apply denylist from PROMPT.md → record drops as counts
3. Frequency analysis per class → append to frequency_report.md
4. Localization join sweep → wheat-by-default for hits
5. Manual H1/H2 pass on residue
6. Quarantine remainder to unknowns.jsonl

## Stop and ask
- A generic_data_type outside the known taxonomy
- Systematic localization join failures
- Cardinality patterns the heuristics can't explain