# ADR-0003: License — MIT, self-host only

- Status: Accepted
- Date: 2026-04-17

## Context

The project is open source from commit #1. License choice affects three things: contributor goodwill, user freedom, and the maintainers' future options for a hosted offering.

Options considered: MIT, Apache 2.0, AGPL, Elastic License / BSL.

## Decision

**MIT.** No separate hosted / commercial edition in this repo. If a hosted offering emerges later, it will live in a separate repo under a separate entity.

## Consequences

Positive:
- Maximally permissive — fewest barriers to contribution and adoption.
- Easy enterprise adoption (no copyleft concerns, no commercial-license-required fears).
- Clear alignment with "OSS from day one" — MIT is what every OSS newcomer already knows.

Negative:
- A cloud vendor could, in principle, run a hosted version of this code and compete with a future hosted offering we might build. We accept this risk — if we build a hosted product it will differentiate on hosted-specific value (team features, eval infra, support), not on exclusivity of the code.

Follow-ups:
- DCO (Developer Certificate of Origin) is enabled on PRs. We explicitly do **not** require a CLA — CLAs chill contribution and an MIT project doesn't need one.

## Alternatives considered

- **Apache 2.0.** Permissive + explicit patent grant. Slightly safer for enterprise. Rejected because MIT is more familiar to first-time contributors and the incremental patent protection doesn't justify the friction.
- **AGPL.** Protects a hosted offering from cloud-vendor resale, but deters many corporate contributors. Rejected in favor of permissive + speed of contribution.
- **BSL / Elastic.** Source-available, not OSI-approved. Rejected — inconsistent with "invite contributions from day one" posture.
