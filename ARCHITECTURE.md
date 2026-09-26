# ElderEase AI — Architecture

## Overview

ElderEase AI is a single-page Streamlit application with no external API dependencies, no database, and no authentication. All processing is synchronous, in-process, and session-scoped.

```
User browser
     │
     ▼
┌─────────────────────────────────────────────────────────┐
│                    app.py  (UI layer)                    │
│  Session state: mood_history[], chat_history[]           │
│                                                          │
│  1. detect_safety_concern(text)  ──► mood_engine.py      │
│  2. detect_mood(text)            ──► mood_engine.py      │
│  3. generate_support_response()  ──► mood_engine.py      │
│  4. get_mood_trend(sequence)     ──► mood_engine.py      │
│  5. get_activity(mood)           ──► activity_engine.py  │
└─────────────────────────────────────────────────────────┘
```

---

## Files and Responsibilities

### `app.py`
The Streamlit UI layer. Owns:
- Page configuration and CSS injection
- `MOOD_BORDER_COLORS` and `MOOD_ICONS` display dicts
- All `st.session_state` management (`mood_history`, `chat_history`)
- User input handling (mood selector, text area, two buttons)
- Rendering logic: response card, trend notice, activity card, mood diary, disclaimer
- Safety-first branch: `detect_safety_concern` is called before `detect_mood`

`app.py` contains **no business logic**. All decisions delegate to the engine modules.

### `mood_engine.py`
The core logic module. Owns:
- `_DISTRESS_KEYWORDS` — 17 distress phrases (private constant)
- `SAFETY_RESPONSE` — the India-localised Tele-MANAS escalation message (public constant)
- `detect_safety_concern(text)` — safety check, must run before `detect_mood`
- `detect_mood(text)` — keyword-based mood classification
- `_RESPONSE_TEMPLATES` — per-mood (opening, closing) template pairs (private)
- `generate_support_response(mood, user_message)` — personalised response builder
- `_MOOD_WEIGHTS` — wellbeing scoring for trend analysis (private)
- `get_mood_trend(mood_sequence)` — within-session trend classifier

Has **no imports** beyond the Python standard library. Zero external dependencies.

### `activity_engine.py`
Activity suggestion module. Owns:
- `ACTIVITIES` — curated dict of 3–4 activities per mood category (public constant)
- `get_activity(mood)` — returns a randomly selected activity for the given mood

Has one import: `random`. No external dependencies.

---

## Data Flow

### Normal chat path

```
User types message
       │
       ▼
detect_safety_concern(message)
       │
   True? ──► render SAFETY_RESPONSE card (red border) — STOP
       │
   False
       │
       ▼
detect_mood(message)
       │ returns mood label (str)
       ▼
generate_support_response(mood, message)
       │ returns personalised response (str)
       ▼
get_activity(mood)
       │ returns activity string (str)
       ▼
append to chat_history + mood_history
       │
       ▼
render response card (mood-coloured border)
       │
       ▼
get_mood_trend([c["mood"] for c in chat_history])
       │ returns "improving" | "declining" | "stable" | "not_enough_data"
       ▼
if trend in {"improving","declining"}: render trend-box
       │
       ▼
render activity card (green)
```

### Quick mood check-in path

```
User selects from dropdown → clicks "✅ Record this mood"
       │
       ▼
append {"mood": selected_mood, "time": timestamp} to mood_history
```

---

## Component Detail

### Mood Detection (`detect_mood`)

Algorithm: linear keyword scan, first-match-wins.

```
Input text → text.lower() → iterate mood_keywords dict
  → for each mood, for each keyword: if keyword in text → return mood
  → if no match → return "Okay"
```

**Mood keyword vocabulary:**

| Mood | Example keywords |
|---|---|
| Lonely | lonely, alone, miss my family, no one to talk |
| Sad | sad, unhappy, upset, cry, depressed, low |
| Anxious | anxious, worried, nervous, scared, afraid, stress |
| Tired | tired, exhausted, sleepy, weak, no energy |
| Happy | happy, great, wonderful, excited, good day |
| Okay | (fallback — no keywords required) |

**Known limitation:** First-match-wins means keyword order in the dict determines priority for overlapping inputs. A message containing both "lonely" and "happy" will return "Lonely" because Lonely is declared first.

---

### Safety Detection (`detect_safety_concern`)

Algorithm: substring search over 17 distress phrases on the lowercased input.

```
Input text → text.lower() → for each phrase in _DISTRESS_KEYWORDS:
  → if phrase in lowered → return True
→ return False
```

Must be called **before** `detect_mood` in the UI layer. This is enforced by the `elif` ordering in `app.py`.

**Distress phrase list (17 entries):**
```
don't want to go on, want to give up, nobody cares about me,
no one cares about me, feel like disappearing, thinking of hurting myself,
want to hurt myself, don't see the point, life feels meaningless,
life is meaningless, want to end it, can't go on, cannot go on,
end my life, kill myself, no reason to live, don't want to live
```

---

### Response Generation (`generate_support_response`)

Algorithm: mood-specific template with user message echo.

```
template = _RESPONSE_TEMPLATES[mood]   # (opening, closing) tuple
trimmed  = user_message[:77] + "..."   # if > 80 chars
middle   = f'You mentioned: "{trimmed}" — that takes courage to share. '
return opening + middle + closing
```

This ensures every response is unique to what the user actually said. An empty `user_message` produces `opening + closing` with no middle section.

---

### Activity Recommendation (`get_activity`)

Algorithm: `random.choice` from a mood-keyed list.

```
activities = ACTIVITIES.get(mood, ACTIVITIES["Okay"])
return random.choice(activities)
```

Each mood has 3–4 activities. Unknown moods fall back to the "Okay" list.

---

### Mood Trend Analysis (`get_mood_trend`)

Algorithm: weighted average comparison across session halves.

```
Wellbeing weights: Happy=5, Okay=4, Tired=3, Lonely=2, Anxious=2, Sad=1

scored      = [weight for each known mood in sequence]
if len(scored) < 3 → "not_enough_data"

midpoint    = len(scored) // 2
avg_first   = mean(scored[:midpoint])
avg_second  = mean(scored[midpoint:])
delta       = avg_second - avg_first

if delta >=  1.0 → "improving"
if delta <= -1.0 → "declining"
            else → "stable"
```

**Design decisions:**
- Threshold of 1.0 on a 5-point scale is intentionally conservative to avoid false positives
- Lonely and Anxious share weight 2 — both represent similar wellbeing difficulty
- The function is pure (no side effects, no Streamlit dependency) and fully unit-testable

---

## Session State

All state is held in `st.session_state` (Streamlit's in-memory per-session store). It is not persisted across page refreshes.

| Key | Type | Contents |
|---|---|---|
| `mood_history` | `list[dict]` | `{"mood": str, "time": str}` — all check-ins and chat moods |
| `chat_history` | `list[dict]` | `{"user": str, "mood": str, "response": str, "activity": str, "time": str}` |

`mood_history` is written by both the quick check-in button and the chat path.
`chat_history` is written only by the chat path.
`get_mood_trend` reads from `chat_history` only (genuine expression, not self-selection).

---

## Streamlit UI Layer

### Rendering sequence
1. Page config + session state initialisation
2. CSS injection (single `st.markdown` block)
3. Header (title + subtitle)
4. Section 1: Quick mood check-in (dropdown + "Record" button)
5. Section 2: Chat input (text area + "Send" button)
   - Safety branch → SAFETY_RESPONSE card
   - Normal branch → response card + trend notice (if any) + activity card
6. Section 3: Recent chat history (last 3, expandable)
7. Section 4: Mood diary (all entries, reversed)
8. Disclaimer footer

### CSS architecture
All styles are injected as a single `unsafe_allow_html=True` markdown block.
Custom classes: `.main-title`, `.subtitle`, `.support-box`, `.trend-box`, `.activity-box`, `.mood-card`, `.disclaimer`.
Mood-coloured borders are passed as inline `style` overrides on the `.support-box` div.

---

## Testing Architecture

```
tests/
├── __init__.py
├── test_mood_engine.py      (80 tests, 11 classes)
└── test_activity_engine.py  (20 tests, 4 classes)
```

**Philosophy:** Tests cover the engine modules only (pure Python, no Streamlit dependency). UI behaviour is verified through visual review and smoke checks.

**Coverage:** 100% of all statements in `mood_engine.py` and `activity_engine.py`.

**Test categories covered:**
- Functional behaviour for all mood categories
- Default/fallback behaviour
- Case insensitivity
- Edge cases (empty, very long, non-ASCII, numeric, punctuation-only inputs)
- Safety-critical inputs (all 17 distress phrases, false-positive guard for 8 normal phrases)
- Response personalisation (user_message echoed, truncation, empty input)
- Trend analysis (insufficient data, improving, declining, stable, unknown moods)
- SAFETY_RESPONSE constant integrity (contains helpline numbers, references India, no medical language)
- Data integrity for ACTIVITIES dict (all keys present, all entries non-empty strings)

---

## Where IBM Bob 2.0 Assisted

| Phase | Bob's contribution |
|---|---|
| **PLAN** | Read all files; produced ranked bug/gap assessment with exact file:line references |
| **BUILD** | Wrote 66 baseline tests from scratch in one task; discovered live bug via test failure |
| **TEST** | Ran test suite; surfaced `user_message` bug and safety gap through evidence |
| **DEBUG** | Diagnosed root cause in `mood_engine.py:60`; implemented fix; updated tests |
| **IMPROVE (safety)** | Audited 13→17 distress phrases; corrected UK→India helpline; added 4 tests |
| **IMPROVE (UI)** | Rewrote CSS + all UI copy in one coherent pass aligned to product vision |
| **IMPROVE (trend)** | Designed, implemented, and tested `get_mood_trend()` end-to-end |
| **DOCUMENT** | Generated README, CHANGELOG, ARCHITECTURE with accurate metrics |

Bob operated in **Agent mode** throughout, reading multiple files in context before each task and running the test suite after each change to confirm no regression.
