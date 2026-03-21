# Architecture archive packs

Deterministic archive packs for `docs/engineering/architecture.md` hot-surface
rollover (`US-0072` / `DEC-0054`).

- Pack name pattern: `architecture-pack-YYYYMMDD.md` (disambiguation suffix if needed).
- Packs preserve full removed story sections; hot file remains history-preserving per `DEC-0043`.
- Enforcement entrypoint: `scripts/enforce-triad-hot-surface.py` (`--check` /
  `--rollover`).
