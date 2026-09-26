# Changelog — ElderEase AI

All notable changes to this project are documented here.
Developed with **IBM Bob 2.0** as the primary development assistant.

---

## [Phase 4] — Improvement 2: Within-Session Mood Trend Awareness

### Added
- `get_mood_trend(mood_sequence)` function in `mood_engine.py`
  - Analyses the sequence of moods from the current session's chat history
  - Returns one of: `"improving"`, `"declining"`, `"stable"`, `"not_enough_data"`
  - Requires minimum 3 entries before computing a trend
  - Uses a 1–5 wellbeing weight scale (Happy=5, Okay=4, Tired=3, Lonely=2, Anxious=2, Sad=1)
  - Threshold of ±1.0 point difference to declare a directional trend
  - Unknown/invalid mood labels silently ignored
- `_MOOD_WEIGHTS` and `_TREND_MIN_ENTRIES` and `_TREND_THRESHOLD` constants
- `.trend-box` CSS class in `app.py` — light blue-tinted card, no alarming styling
- Trend notice rendered between response card and activity card (only when meaningful)
  - Improving: `"💚 Your recent check-ins seem to be moving in a more positive direction."`
  - Declining: `"💙 Your recent check-ins have been a little harder lately."`
  - Stable / insufficient: nothing rendered

### Tests added (18 new tests in `TestGetMoodTrend`)
- Empty, 1-entry, 2-entry sequences → `not_enough_data`
- 3-entry minimum threshold
- Clearly improving sequences (Sad→Happy, 4-entry, 5-entry)
- Clearly declining sequences (Happy→Sad, 4-entry, 5-entry)
- Stable sequences (identical moods, symmetric alternation)
- All-unknown input → `not_enough_data`
- Mixed known/unknown input → unknown labels ignored
- Return value contract: always a string, always one of four valid values

### Metrics
| Metric | Before | After |
|---|---|---|
| Total tests | 82 | **100** |
| Passing | 82 | **100** |
| `mood_engine.py` coverage | 100% | **100%** |

---

## [Phase 3] — Improvement 1: UI Polish + Accessibility

### Changed (`app.py` only)
- Body text: implicit ~16px → explicit **18px** with `line-height: 1.75` and `letter-spacing: 0.01em`
- Response cards: **20px** font size
- Section headings: **24px**, weight 700
- App title: **46px**, weight 800
- Disclaimer footer: `st.caption` (~12px) → styled `<p>` at **15px**, includes Tele-MANAS numbers
- `"Detected mood: Sad"` → `"😔 ElderEase hears you"` (removed all technical labels)
- `"Save my mood"` → `"✅ Record this mood"`
- `"Talk to ElderEase"` → `"💙 Send to ElderEase"`
- `"Sad conversation"` expander → `"😔 You said you felt Sad · 14 Jul 2025 – 10:30 AM"`
- `"Recent conversation"` → `"💬 Your recent chats with ElderEase"`
- `"Mood History"` → `"📅 Your mood diary"`
- Mood dropdown: bare labels → descriptive labels with emoji and plain-language explanation
- Activity card: distinct green-tinted background (`#f0f7ee`), green left border
- Mood history cards: soft blue border (`#d0e4f7`), subtle shadow
- Safety response card: red left border unchanged (`#c0392b`)
- Mood-coloured response borders per detected mood (6 distinct colours)
- `MOOD_BORDER_COLORS` and `MOOD_ICONS` dicts added to `app.py`
- `chat_history` entries now include `"time"` field

### Metrics
- No test count change (UI layer only, engines unchanged)
- 82/82 tests continue to pass after all UI changes

---

## [Phase 2b] — Safety + Quality Review

### Changed (`mood_engine.py`)
- `SAFETY_RESPONSE` helpline updated: **Samaritans 116 123 (UK)** → **Tele-MANAS 14416 / 1800-89-14416 (India)**
- `SAFETY_RESPONSE` text updated to reference India availability
- `_DISTRESS_KEYWORDS` expanded: **13 → 17 phrases**
  - Added: `"end my life"`, `"kill myself"`, `"no reason to live"`, `"don't want to live"`

### Tests changed/added (`TestSafetyResponse`, `TestDetectSafetyConcern`)
- `test_safety_response_contains_helpline_reference` (old UK assertion) → removed
- `test_safety_response_contains_tele_manas_short_number` — asserts `"14416"` present
- `test_safety_response_contains_tele_manas_tollfree_number` — asserts `"1800-89-14416"` present
- `test_safety_response_references_india` — asserts `"India"` present
- `test_safety_response_does_not_reference_uk_samaritans` — regression guard against reverting
- `test_safety_response_does_not_present_as_emergency_service` — confirms boundary
- `TestDetectSafetyConcern.DISTRESS_PHRASES` extended to include all 17 phrases

### Metrics
| Metric | Before | After |
|---|---|---|
| Total tests | 78 | **82** |
| Passing | 78 | **82** |
| Distress phrases covered | 13 | **17** |
| Correct India helpline | ❌ | **✅** |
| Medical terms in safety response | 0 | **0** |

---

## [Phase 2a] — DEBUG + IMPROVE

### Bug fixed: `generate_support_response` ignored `user_message`
- **Root cause:** `mood_engine.py:60` — the `user_message` parameter was accepted but the function body performed only a dictionary lookup on `mood`. The parameter was discarded.
- **Evidence:** Test `test_response_differs_for_different_user_messages_same_mood` **FAILED** on baseline run, confirming the bug.
- **Fix:** Response now built from a `(opening, closing)` template pair with the user's own message echoed in the middle. Messages longer than 80 characters are gracefully truncated with `"..."`.

### Safety gap closed: distress detection added
- New function `detect_safety_concern(text)` — scans 13 distress phrases before `detect_mood` is called
- New constant `SAFETY_RESPONSE` — warm, non-medical, with helpline reference
- `app.py` updated: `elif detect_safety_concern(user_message)` branch added before mood path
- Safety response styled with red left border (`#c0392b`)

### Tests added
- `TestDetectSafetyConcern` — 6 tests
- `TestSafetyResponse` — 4 tests (initial)
- `TestGenerateSupportResponseUserMessage` — 5 tests (replaces 2 old bug-documenting tests)
- 2 fallback tests updated to reflect user_message now being used

### Metrics
| Metric | Before | After |
|---|---|---|
| Total tests | 66 | **78** |
| Passing | 65 | **78** |
| Failing | **1** | **0** |
| Safety phrases covered | 0 | 13 |
| Bug: `user_message` discarded | ❌ Present | **✅ Fixed** |

---

## [Phase 1] — Baseline Test Suite

**IBM Bob 2.0 wrote the entire test suite from scratch against the unmodified codebase.**

### What was tested (no production code changed in this phase)
- `test_mood_engine.py` — 46 tests across 6 classes
- `test_activity_engine.py` — 20 tests across 4 classes

### Findings from baseline run
| Finding | Type | Severity |
|---|---|---|
| `generate_support_response` ignores `user_message` | **BUG** | High |
| No safety escalation path for distress language | Gap | High |
| Duplicate history entries possible | Gap | Medium |
| Activity suggestions have no deduplication | Gap | Low |

### Baseline metrics
| Metric | Result |
|---|---|
| Tests collected | 66 |
| Passing | 65 |
| **Failing** | **1** |
| `mood_engine.py` coverage | 100% |
| `activity_engine.py` coverage | 100% |

---

## [v0.1.0] — Original Prototype

Initial working prototype — not developed with IBM Bob.

### Features
- Mood selector (5 moods via dropdown)
- Free-text chat input
- Basic keyword-based mood detection (first-match-wins)
- Canned response dictionary (6 moods)
- Random activity selection (6 mood lists × 3–4 activities)
- Session-based mood history
- Static safety disclaimer footer
- Basic Streamlit CSS (no font size specification, grey border on all cards)

### Known issues at this stage
- `generate_support_response(mood, user_message)` — `user_message` parameter accepted but never used
- No distress phrase detection
- No safety escalation path
- Safety disclaimer referenced Samaritans 116 123 (UK) — incorrect for India
- Body font size not explicitly set (~16px browser default)
- Technical labels shown to user ("Detected mood: Sad")
- 0 automated tests
