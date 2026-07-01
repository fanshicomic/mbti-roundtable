# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Agentic workflow

- Before starting, restate the task in your own words; if anything in this file or the request is ambiguous, ask before proceeding.
- For any complex or multi-step task, present a plan and get approval before executing. Use a todo list to track steps on anything with 3+ steps, and keep it updated as you go rather than batching updates at the end.
- Prefer the smallest change that satisfies the requirement. Don't refactor, add abstractions, or "improve" unrelated code while implementing a feature.
- After implementing, verify the change actually works rather than assuming it does: run build/lint/test commands (see Commands section) and fix failures before reporting done. For UI work, run the dev server and exercise the feature in a browser — don't rely on type-checking alone.
- Keep this file in sync with reality: once real commands, tooling, or architecture exist, update the relevant sections and delete stale "not yet applicable" placeholders. Don't let this file describe an aspirational state once code contradicts it.
- Match new code to whatever conventions the codebase has already established (naming, file layout, error handling style) rather than introducing a new pattern per feature.
- Don't invent scope: if a task seems to require a product decision not covered by [docs/PRD.md](docs/PRD.md), ask rather than guessing.

## Git workflow

- Remote: `origin` → https://github.com/fanshicomic/mbti-roundtable.git.
- Commit identity should be `fanshicomic@gmail.com`. Agents must not run `git config` themselves (identity changes are a human decision) — if `git config user.email`/`user.name` aren't already set in this repo, ask the user to set them rather than setting them yourself.
- Push regularly, but only commits that are tested and working (relevant tests pass, and for UI changes the feature was verified running) — never push broken or half-finished work-in-progress to `origin`.
- Never force-push. Regular commits/pushes to this repo don't need to be re-confirmed each time (already authorized), but destructive operations (reset --hard, history rewrites) still need explicit sign-off per the general git safety rules.

## Project status

Initial scaffold exists on both sides, with no feature logic implemented yet:

- `backend/`: FastAPI app with a working `/health` endpoint, and the module layout below with stub bodies (`raise NotImplementedError`) for `engine/`, `personas/`, `moderation/`, `llm/`, `store/` — signatures and docstrings point at the relevant PRD section, but nothing is implemented.
- `frontend/`: Vite + React + TS + Tailwind, with placeholder `Stage`/`LogViewer`/`Config`/`UserSeat` components wired into the 70/30 layout — no state, streaming, or real content yet.

Full product requirements live in [docs/PRD.md](docs/PRD.md) — read it before implementing any feature; the mechanics it describes (speaker-selection algorithm, sliding-window context, rename substitution, output contract, participation limits) are load-bearing and easy to get wrong from intuition alone. Keep this file and the PRD in sync: PRD = what it should do, CLAUDE.md = how the codebase actually does it — update both as features land instead of letting either go stale.

## Stack

Frontend: React + Tailwind CSS. Backend: Python (FastAPI). Real-time: SSE (simpler than WebSocket for the one-directional server→client token stream this app needs; only move to WebSocket if the user's 3 interjections need to interrupt an in-flight stream mid-token).

## Project structure

```
backend/                  # Python 3.13, venv at backend/.venv
  app/
    main.py                # FastAPI app, CORS, router mounting — DONE (health check only)
    api/                    # HTTP routes: health done; session config, rename, SSE stream endpoint still to add
    engine/                 # the no-moderator turn engine — kept free of FastAPI/HTTP concerns so it's unit-testable in isolation
      window.py              # sliding-window message queue (cap 5-8) + pinned scenario, high-priority injection path — DONE
      impulse.py             # speaking-impulse scoring (recency + direct-address + relationship magnitude + jitter) + next-speaker selection — DONE (RNG is injectable for deterministic tests)
      relationships.py       # dichotomy-overlap friction/affinity score in [-1,1] — DONE (still swappable for a hand-tuned table later)
      session.py             # per-session runtime state: roster, rename map, user message count, turn/time cap — implemented, not yet wired to api/
    personas/               # one system-prompt builder per MBTI type, template from docs/PRD.md — template in place, build_system_prompt() + all 16 CORE_DRIVERS still to add
    moderation/             # app-level content filter + output-contract enforcement — stubbed
    llm/                    # streaming completion client behind a provider-agnostic interface (llm/base.py) — interface only, no provider implementation yet
    schemas/                # Pydantic models — DONE: Character, Message, SessionConfig/State, MBTIType, EmotionState
    store/                  # persistence for shareable session transcripts — stubbed, no DB wired yet (SQLite is enough for MVP)
    tests/                  # test_health.py, test_relationships.py, test_window.py, test_impulse.py
  pyproject.toml           # pytest + ruff config
  requirements.txt
frontend/                 # Vite + React 19 + TypeScript + Tailwind v4
  src/
    components/
      Stage/                 # placeholder only — round table seating/streaming bubbles still to build
      LogViewer/             # placeholder only
      Config/                # placeholder only
      UserSeat/              # placeholder only
    hooks/                  # not yet created — useMessageStream (SSE consumer), useTypewriter
    state/                  # not yet created — global store: message log, active speaker, roster/rename map
    types/                  # not yet created — TS types mirroring backend Pydantic schemas
    api/                    # not yet created — REST + SSE client
  vite.config.ts           # dev server pinned to port 5174 (5173 was occupied by an unrelated local project)
docs/
  PRD.md
```

## Coding conventions (proposed — apply once scaffolding starts)

- **Engine is pure and I/O-free.** `engine/window.py`, `engine/impulse.py`, and `engine/relationships.py` must not import FastAPI, touch the network, or hit `store/` — they take/return plain data structures. This is the highest-risk-of-bugs part of the app (turn order, token cost), so it needs to be testable without spinning up a server or mocking an LLM.
- **One schema, two languages.** Define message/character/session shapes once in `schemas/` (Pydantic) and hand-mirror them in `frontend/src/types/`; keep field names identical (e.g. `mbti_type`/`mbtiType` per language casing convention below) so the PRD's mechanics don't drift between client and server. Include `emotion_state` and the always-shown MBTI label in the character shape from the start, even though today it only drives an emoji — this is the hook the next milestone's skin/animation system builds on.
- **LLM provider behind an interface.** Nothing outside `llm/` should know which provider is in use — swapping DeepSeek/OpenAI/Claude must not touch `engine/` or `personas/`.
- **Moderation and output-contract enforcement happen server-side, after generation, before persistence.** Truncation/stripping (length, meta-commentary) and the content guardrail both run in the request path between `llm/` and `store/`/the SSE stream — never trust the raw LLM output to already satisfy the contract, and never filter only on the frontend.
- **Naming casing:** Python — `snake_case` for functions/variables, `PascalCase` for Pydantic models. TypeScript/React — `camelCase` for functions/variables, `PascalCase` for components and types.
- **No magic numbers for tunable constants** (seat cap 8/16, window size 5-8, user message limit 3, output length 20). Define them once in `backend/app/config.py` and import everywhere, since these are exactly the numbers most likely to change per the PRD's paid-unlock hook.
- **Seat geometry lives in one place.** Round-table absolute-positioning math (angle/radius per seat index) belongs in a single helper in `Stage/`, not recomputed per component.

## Commands

**Backend** (from `backend/`, with `source .venv/bin/activate` first):
- Run dev server: `uvicorn app.main:app --reload --port 8000`
- Run all tests: `python -m pytest -q`
- Run a single test: `python -m pytest -q tests/test_health.py::test_health`
- Lint: `ruff check .`

**Frontend** (from `frontend/`):
- Install deps: `npm install`
- Dev server: `npm run dev` (http://localhost:5174)
- Type-check + production build: `npm run build`
- Lint: `npm run lint` (oxlint)
- Preview via the Launch Preview tooling: server name `frontend` in `.claude/launch.json`.

No single-test runner is set up on the frontend yet since there are no component tests — add one (e.g. Vitest) when the first test is written.
