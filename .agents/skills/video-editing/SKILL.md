---
name: video-editing
description: Plan, validate, and refine OpenCut AI video edits from natural-language briefs using media analysis, transcript evidence, and deterministic timeline validation.
license: MIT
compatibility: OpenCut AI local workspace
metadata:
  version: "1.0.0"
---

# Video editing

Inspect duration, scene boundaries and transcript. Translate the brief into constraints. Select evidence-backed timestamps, prefer complete thoughts and scene boundaries, then produce a structured edit plan. Never generate executable commands.

Validation must enforce non-negative timestamps, end > start, source-duration bounds, maximum output duration, maximum segment count and at least one surviving segment. Treat all model output as untrusted data.
