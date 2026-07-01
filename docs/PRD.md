# PRD: MBTI 虚拟圆桌修罗场 (Web MVP)

This is the product spec. Implementation architecture, once code exists, belongs in CLAUDE.md — this file should describe intended product behavior, not be re-derived from code comments.

## Product summary

"MBTI 虚拟圆桌修罗场" — a Web MVP where multiple LLM-driven MBTI personality agents free-for-all debate/chat around a user-supplied scenario in a "virtual roundtable." Positioning is pure entertainment / high interactivity / viral screenshot-sharing (电子斗蟋蟀). The user can rename characters (改名代餐) and has a limited number of interjections (拱火) to stir the pot.

## Core mechanics (must-read before implementing backend logic)

**No moderator — impulse-driven speaker selection.** There is no fixed turn order or host. After each message, the backend computes a "speaking impulse" score for every remaining candidate character and picks the next speaker by highest impulse (or weighted-random among top candidates). Only that one character's LLM call is triggered per turn.

Impulse score is a weighted combination of:
- **Recency decay** — characters who haven't spoken in a while accumulate a rising boost, so no one goes silent for the whole session.
- **Direct address** — being named/@'d in the immediately preceding message gives a strong boost (this is also how a user's interjection reaches the character(s) it targets).
- **MBTI relationship matrix** — a predefined pairwise friction/affinity score between the last speaker's type and each candidate's type (see below) biases who's most likely to jump in.
- **Random jitter** — a small random term so outcomes aren't fully deterministic/predictable.

**MBTI relationship matrix.** A predefined table of pairwise friction/affinity between the 16 types, used by both the impulse score (who jumps in) and the persona prompt (how they react to whom). For MVP, derive it algorithmically from dichotomy overlap (e.g., opposing letters → higher friction, shared letters → higher affinity) rather than hand-authoring all 120 pairs; it can be replaced with hand-tuned "MBTI drama folklore" values later without changing the engine's interface to it.

**Session context payload.** Each LLM call sends `[persona System Prompt] + [pinned scenario] + [sliding window history]` — the user's original scenario is pinned and included in every call *in addition to* the sliding window, not just as message #1, so it doesn't scroll out of context after ~8 messages and characters don't forget the premise mid-roast.

**Sliding-window context (token cost control).** The backend keeps a global message queue capped at 5–8 messages for the rolling conversation portion of the payload (the pinned scenario above is separate and always included). This window, not the full log, is the source of truth for recent-turn context; the full history is persisted separately for the right-side Log Viewer (and for shareable replays — see Persistence below).

**Session length cap.** A session auto-ends after a fixed number of total character turns or elapsed time (a config constant), independent of the user's 3-message allowance — this bounds LLM spend even if the user leaves the tab open.

**User interjection = high-priority injection.** When the user speaks, their message is pushed into the sliding window with high priority and directly boosts the affected characters' impulse values, forcing a near-immediate reaction. This is a distinct code path from normal turn advancement, not just another queued message.

**Seat capacity & unlock hook.** User manually picks which types are seated (not random assignment): up to 8 distinct MBTI characters for the free tier, chosen from all 16. Design the character-roster/session config with a hard-coded extension point for a future paid/ad-unlock path to seating all 16 at once — don't hardcode "8" as a magic number scattered across the codebase.

**Rename substitution (改名代餐).** Users can rename any seated MBTI character (e.g. `ESTJ` → `老板`). The backend must dynamically substitute the display name for the MBTI label when building the System Prompt / context sent to the LLM, so agents address each other by the custom name in-conversation — not just in UI.

**Display always keeps the MBTI label.** Regardless of renaming, every on-screen reference to a character shows the type alongside the name: `SomeName (INFJ)` when renamed, or just `INFJ` when not renamed (no redundant `INFJ (INFJ)`). This applies on the Stage, in the Log Viewer, and in the Config screen.

**Output contract enforced server-side.** Every character turn must be one short sentence, ≤20 characters (zh) / ≤20 words (en), no preamble/meta-commentary, no politeness hedging. The backend enforces this by truncating and stripping any violating output (extra prefixes, meta-commentary, over-length text) before it enters the sliding window or reaches the frontend — no retry call to the LLM, to keep latency/cost predictable per turn.

**Content guardrail.** Blunt, personality-based roasting is the point of the app and should not be softened — but an app-level filter (on top of whatever the LLM provider's own safety layer already blocks) should catch content that crosses from "bit" into real slurs, protected-class attacks, or genuine harassment, and prevent it from being sent to the frontend.

**User participation limits.** The user has a fixed reserved seat ("吃瓜群众（你）") and can send at most 3 messages per session; input is disabled (grayed out) after the 3rd. Enforce this server-side, not just via frontend disabling.

**Emotion/expression state.** Each character carries an `emotion_state` derived from engine-level events it already knows about (e.g. "just got roasted," "impulse just spiked for this character") — no extra LLM call or text classification needed. For MVP this renders as an emoji overlay on the avatar; the same field is designed to later drive skin changes and animated facial expressions without a data-model change, per the planned next milestone.

**Persistence & sharing.** No accounts/login for MVP. A session's roster and transcript persist server-side under a shareable session ID so a finished roundtable can be viewed via link later (supports the "screenshot and share" virality goal) — this requires a lightweight datastore, not just in-memory state, even though there's no user auth.

**Language scope.** Chinese-only for MVP — UI copy, scenario input, and character dialogue. No i18n scaffolding needed yet.

## Agent prompt template

Each of the 16 MBTI types needs its own System Prompt built from this structure (name and MBTI-relationship-driven reactions are dynamic per session, not static):

```
[Role Definition]
You are an extreme, stereotyped [MBTI_TYPE], now using the name [USER_CUSTOM_NAME].

[Personality & Constraints]
- Your core driver: [e.g., Efficiency-first for ESTJ / Emotional resonance for INFP].
- Speak ONLY ONE concise sentence (Max 20 words). Never blabber.
- Never be overly polite. Never say "I understand your point."
- React heavily based on your MBTI relationship dynamics. If someone offends your value, roast them bluntly.

[Context Output Instruction]
Read the recent chat history and output your next text line directly. No prefixes, no meta-commentary.
```

## UI structure (70/30 split)

- **Left (70%) — The Stage:** 2D flat/pixel-style round table, characters (incl. the user's seat) absolutely-positioned around it. Active speaker gets a streaming (token-by-token, WebSocket/SSE) speech bubble and a highlight/scale-up effect. Emotionally "worn down" or rebutted characters can trigger a CSS grayscale filter or emoji overlay.
- **Right (30%) — Log Viewer:** scrollable full chat history (persisted, unlike the backend's sliding window). Clicking a character's avatar on the Stage scrolls/highlights that character's latest message here, for one-click screenshot sharing.

## Tech stack (confirmed)

- Frontend: React + Tailwind CSS (absolute positioning for the round-table seating).
- Backend: Python (FastAPI).
- Real-time: SSE for token-level streaming to the frontend.
- LLM API: any provider with fast streaming completions (e.g. DeepSeek, or an OpenAI/Claude aggregation gateway) — see CLAUDE.md's "LLM provider behind an interface" convention.
