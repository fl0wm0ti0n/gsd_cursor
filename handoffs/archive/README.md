# Handoff archive packs

Deterministic archive packs for `handoffs/po_to_tl.md` hot-surface rollover
(`US-0072` / `DEC-0054`).

- Pack name pattern: `po-to-tl-pack-YYYYMMDD.md` (disambiguation suffix if needed).
- Packs are append-only; do not rewrite historical packs.
- Enforcement entrypoint: `scripts/enforce-triad-hot-surface.py` (`--check` /
  `--rollover`).
