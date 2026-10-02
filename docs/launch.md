# Repository launch kit

Suggested repository: **`xi029/jev-lens`**. Project name: **JevLens**.

Description:

> Decide before you generate. Local evidence gates, threshold replay and inspectable RAG traces for Laya, Jev and Ollama.

Suggested GitHub topics:

`jev`, `laya`, `rag`, `ollama`, `local-ai`, `decision-models`, `system-one`, `explainable-ai`, `python`, `fastapi`, `qwen`

Use `docs/assets/hero.svg` as a starting point for a social preview; GitHub's social preview upload requires a raster image. The actual UI screenshot is `docs/assets/studio.jpg`.

## Release v0.1.0 draft

JevLens puts an inspectable decision layer between retrieval and generation. The local workbench supports Laya, hosted Jev, and Ollama; shows exact provider excerpts; gates generation; exports traces; and replays thresholds without new inference. An external evidence API lets existing RAG projects keep their retriever and generator.

Included: an account-free demo, original fictional knowledge samples, CLI and JSON API, Windows/Linux CI, Apache-2.0 licensing, and English/Chinese documentation.

Scope: Markdown/text, lexical retrieval, a local single-user workspace. LLM scores are uncalibrated and generated citations are checked for valid IDs only. The fixture is a smoke test, not a competitive benchmark.

## Demo outline

Show one supported refund question. Raise the support threshold and show the new replay route without changing the original response. Add the conflicting refund draft and show why generation is skipped. Finish by exporting the inspectable trace and switching to your local model.

## Optional announcement draft

I built JevLens, an open-source evidence workbench for Laya, Jev and Ollama. It asks whether your retrieved docs actually support an answer before calling the generator. The part I wanted most: move a threshold on a saved judgment and replay the route with zero model calls. It runs locally, includes an account-free demo, and exports the evidence and decision as JSON.

Try it: https://github.com/xi029/jev-lens

No claims about beating another model or eliminating hallucinations. Model errors and score semantics remain visible.

This is a draft for the maintainer. It has not been posted anywhere.

## Publish from this workspace

After installing [GitHub CLI](https://cli.github.com/) and authenticating with `gh auth login`, run `./scripts/publish.ps1` in PowerShell. It checks the signed-in account, requires a clean commit, refuses to overwrite an existing repository, creates `xi029/jev-lens` as public, pushes the current source and adds discovery topics.

`python scripts/prepare_release.py` produces a ZIP from tracked files only. It rejects local data, caches, `.env` and unexpectedly large files. This is suitable for manual upload or sharing the source before GitHub authentication is configured.
