# 💙 ElderEase AI

### A gentle AI companion for everyday emotional wellbeing

ElderEase AI is a simple, accessible, and safety-aware companion designed for older adults. It listens to how a user is feeling, responds with genuine care, suggests a small meaningful activity, and keeps a quiet record of the day's emotional pattern.

---

## 🌱 Problem

Older adults in India frequently experience loneliness, anxiety, sadness, and social isolation. Many digital wellbeing tools are complicated, impersonal, or designed for younger users. Simple human connection — someone to talk to, without judgment — is often what is most needed.

ElderEase AI provides that: a calm, respectful, and accessible digital companion that older adults can use without instruction.

**Target users:** Adults aged 60 and above who want a simple way to express how they are feeling and receive gentle, non-medical support.

---

## 💡 Solution

A single-page Streamlit application with no login, no complex navigation, and no technical jargon. The user types how they are feeling. ElderEase listens, responds with warmth, and suggests one small activity.

### Core Experience

```
Talk → Understand → Support → Suggest → Remember
```

1. **Talk** — The user writes a few words or sentences about how they feel.
2. **Understand** — ElderEase identifies the emotional mood from the message.
3. **Support** — ElderEase responds compassionately, echoing the user's own words.
4. **Suggest** — ElderEase recommends one small, gentle activity.
5. **Remember** — The interaction is recorded in the session's mood diary.

---

## ✨ Features

| Feature | Description |
|---|---|
| 😊 Quick mood check-in | Descriptive dropdown with emoji and plain-language labels |
| 💬 Free-text expression | Write how you feel in your own words |
| 🧠 Mood detection | Identifies six moods: Happy, Okay, Sad, Lonely, Anxious, Tired |
| 💙 Personalised response | Echoes the user's own message in a warm, non-generic reply |
| 🌿 Activity suggestion | One gentle, relevant activity per mood |
| 📈 Mood trend awareness | Notices when check-ins are improving or declining across the session |
| 📅 Mood diary | Records every check-in with timestamp |
| 🛡️ Safety escalation | Detects serious distress language and surfaces the Tele-MANAS helpline |
| 👴 Elderly-first UI | Large text (18–20px), mood-coloured cards, plain language throughout |

---

## 🛡️ Safety Approach

ElderEase AI includes a dedicated safety layer that operates **before** ordinary mood detection.

- 17 distress phrases are monitored (e.g. "I don't want to go on", "I want to end my life")
- If any phrase is detected, the standard response path is bypassed entirely
- The user receives a warm, non-medical message with the **Tele-MANAS** helpline:
  - **14416** (short number)
  - **1800-89-14416** (toll-free, 24 hours, available across India)
- ElderEase does **not** diagnose, prescribe, or act as a crisis service

---

## ♿ Accessibility

The interface is designed specifically for older adults:

- Minimum **18px** body text, **20px** response cards, **24px** section headings
- `line-height: 1.75` and `letter-spacing: 0.01em` for comfortable reading
- Descriptive dropdown labels: `"😔 Sad — I am feeling low or upset"` instead of just `"Sad"`
- Mood-coloured response cards (each mood has a distinct border colour)
- Warm, plain-language button labels: `"✅ Record this mood"` and `"💙 Send to ElderEase"`
- No technical language shown to the user (no "detected mood", no "classification")
- Disclaimer footer visible at 15px with Tele-MANAS numbers

---

## 📈 Mood Trend Awareness

After at least three chat interactions in a session, ElderEase quietly notices the emotional direction:

- **Improving:** `"💚 Your recent check-ins seem to be moving in a more positive direction. That is good to notice."`
- **Declining:** `"💙 Your recent check-ins have been a little harder lately. You do not have to face that alone."`
- **Stable / insufficient data:** Nothing shown — no noise

The algorithm uses a simple wellbeing scoring system (Happy=5, Okay=4, Tired=3, Lonely=2, Anxious=2, Sad=1), compares the first and second halves of the session, and requires a meaningful shift (≥1.0 points) before surfacing any message. It makes no medical or psychological claims.

---

## 🛠️ Technology

| Component | Technology |
|---|---|
| Application | Python 3.12 + Streamlit 1.40 |
| Mood detection | Rule-based keyword matching |
| Safety detection | Phrase-list screening |
| Response generation | Template-based personalisation |
| Activity suggestions | Deterministic selection from curated lists |
| Mood trend | Weighted average comparison (pure Python) |
| Testing | pytest + pytest-cov |
| Version control | Git |

**No external AI APIs. No database. No authentication. No paid services.**

---

## 🤔 Why Rule-Based AI?

ElderEase AI intentionally uses deterministic, rule-based logic rather than a large language model or external AI API. This is a deliberate design decision, not a limitation:

- **Reliability** — Every response is predictable and reviewable. There are no hallucinations, no unexpected outputs, and no model drift.
- **Transparency** — The logic is fully readable in source code. Anyone can verify exactly what the application will say for any given input.
- **Safety** — The distress-detection path is guaranteed to fire for all 17 configured phrases, every single time. An LLM could miss them or respond inconsistently.
- **Privacy** — No user message is ever sent to a third-party API. An older adult's emotional disclosure stays entirely on their own device.
- **Dependency-free** — No API key, no paid service, no network request required. The application runs fully offline.
- **Appropriate scope** — For a gentle daily check-in companion, consistent and compassionate templated responses serve the user better than non-deterministic generation.

This design is validated by 100 automated tests with 100% engine coverage — a level of confidence that is difficult to achieve with generative AI outputs.

---

## 📂 Project Structure

```text
ElderEase-AI/
├── app.py                   # Streamlit UI layer — session state, rendering, user flow
├── mood_engine.py           # Mood detection, safety detection, response generation, trend analysis
├── activity_engine.py       # Activity suggestion by mood category
├── requirements.txt         # Python dependencies (pinned)
├── .gitignore               # Excludes .venv, __pycache__, .env, etc.
│
├── tests/
│   ├── test_mood_engine.py  # 80 tests — mood, safety, response, trend
│   └── test_activity_engine.py  # 20 tests — activity generation and data integrity
│
└── docs/
    ├── PRODUCT_VISION.md    # Product principles and boundaries
    ├── ARCHITECTURE.md      # System design, data flow, component responsibilities
    └── CHANGELOG.md         # → see CHANGELOG.md at root
```

---

## ⚙️ Installation and Setup

```bash
# 1. Clone the repository
git clone https://github.com/DivyaMeghana09/ElderEase-AI.git
cd ElderEase-AI

# 2. Create a virtual environment
python -m venv .venv

# 3. Activate it
# Windows:
.venv\Scripts\activate
# macOS / Linux:
source .venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Run the application
streamlit run app.py
```

The application opens at `http://localhost:8501` in your browser.

---

## 🧪 Testing

```bash
# Run the full test suite with coverage
python -m pytest tests/ -v --cov=mood_engine --cov=activity_engine --cov-report=term-missing
```

### Current test results

| Metric | Result |
|---|---|
| Total tests | **100** |
| Passing | **100** |
| Failing | **0** |
| `mood_engine.py` coverage | **100%** |
| `activity_engine.py` coverage | **100%** |

### Test categories

| File | Class | Tests |
|---|---|---|
| `test_mood_engine.py` | `TestDetectMoodFunctional` | 19 |
| `test_mood_engine.py` | `TestDetectMoodDefault` | 4 |
| `test_mood_engine.py` | `TestDetectMoodCaseSensitivity` | 4 |
| `test_mood_engine.py` | `TestDetectMoodEdgeCases` | 5 |
| `test_mood_engine.py` | `TestDetectMoodSafetyCases` | 1 |
| `test_mood_engine.py` | `TestDetectSafetyConcern` | 6 |
| `test_mood_engine.py` | `TestSafetyResponse` | 8 |
| `test_mood_engine.py` | `TestGenerateSupportResponseFunctional` | 8 |
| `test_mood_engine.py` | `TestGenerateSupportResponseUserMessage` | 5 |
| `test_mood_engine.py` | `TestGenerateSupportResponseFallback` | 2 |
| `test_mood_engine.py` | `TestGetMoodTrend` | 18 |
| `test_activity_engine.py` | `TestGetActivityFunctional` | 8 |
| `test_activity_engine.py` | `TestGetActivityFallback` | 4 |
| `test_activity_engine.py` | `TestActivitiesDataIntegrity` | 5 |
| `test_activity_engine.py` | `TestGetActivityVariety` | 3 |

---

## 🤖 IBM Bob 2.0 — Developer Workflow Contribution

This project was developed using **IBM Bob 2.0** as an active development partner across every phase of the PLAN → BUILD → TEST → DEBUG → IMPROVE → DOCUMENT lifecycle. Below is a precise account of which Bob capability was used at each step and what it produced.

### PLAN — Document Understanding + Code Analysis
Bob's **Agent mode** read all five project files in a single context window — including `PRODUCT_VISION.md`, `app.py`, `mood_engine.py`, `activity_engine.py`, and `requirements.txt`. Using **document understanding**, Bob cross-referenced the product vision against the implementation and produced a ranked, evidence-based assessment identifying two confirmed bugs, three design gaps, and ten prioritised improvements — all before any code was changed.

### BUILD — Baseline Tests via Agent Mode
Bob's **Agent mode** wrote **66 tests** from scratch across two test files, covering functional behaviour, edge cases, case sensitivity, and safety-critical inputs — all against the original unmodified code. Bob used **code analysis** to understand each function's actual behaviour (including its implicit contract) before writing assertions. This is the phase where the `user_message` bug was first captured as a failing assertion.

### TEST — Test Execution + Bug Discovery
Bob **ran the full test suite** and reported the single failure with its exact assertion error, confirmed that the `user_message` parameter was accepted but discarded at `mood_engine.py:60`, and identified two further gaps (no safety escalation path, no activity deduplication) as documented-but-passing tests. Test execution was used as the primary verification mechanism throughout — not manual review.

### DEBUG — Root Cause Analysis + Coordinated Multi-File Fix
Bob performed **root cause analysis** on the failing test, traced it to the dictionary-only lookup in `generate_support_response`, designed a template-based fix that incorporated the user's own message, and implemented a **coordinated multi-file change** across `mood_engine.py` and the corresponding test class in a single Agent task — updating the fix, the passing companion test, and the fallback tests simultaneously.

### IMPROVE — Multi-File Implementation with Continuous Regression Testing
Bob's **Agent mode** executed four distinct improvement tasks, each followed by a full test-suite run to confirm no regression:
1. **Safety escalation** — designed and implemented `detect_safety_concern()` and `SAFETY_RESPONSE`, wired the `elif` branch into `app.py`, added 10 new safety tests
2. **Safety review** — audited the 13 distress phrases, identified 4 gaps, corrected the helpline from UK Samaritans (116 123) to India Tele-MANAS (14416), added 4 regression-guard tests
3. **Accessibility overhaul** — rewrote CSS and all UI copy in `app.py` in a single coherent Agent pass informed by the `PRODUCT_VISION.md` constraints read earlier
4. **Mood trend** — designed `get_mood_trend()`, implemented it in `mood_engine.py`, integrated it into `app.py`, and wrote 18 dedicated tests — all in one Agent task

### DOCUMENT — Repository-Wide Documentation Generation
Bob used its full repository context (all source files, all test results, the product vision) to generate this README, `CHANGELOG.md`, and `docs/ARCHITECTURE.md` with metrics drawn directly from live test-suite output — not estimates. The ARCHITECTURE document includes accurate ASCII data-flow diagrams derived from reading the actual code, not assumed structure.

### Measurable impact

| Metric | Before Bob | After Bob |
|---|---|---|
| Tests | 0 | **100** |
| Test failures | N/A | **0** |
| Engine coverage | 0% | **100%** |
| Known bugs | 1 (undetected) | **0** |
| Safety phrases covered | 0 | **17** |
| Correct helpline for India | ❌ | **✅** |
| Accessible font size (body) | Implicit ~16px | **18px explicit** |
| Medical language in safety response | N/A | **0 medical terms** |
| Distress phrases with no escalation path | All | **0** |

---

## IBM Bob 2.0 Development Evidence

IBM Bob 2.0 was used throughout the ElderEase AI development lifecycle:

**PLAN → BUILD → TEST → DEBUG → IMPROVE → DOCUMENT → VERIFY**

Bob was used to assess the existing project, identify engineering and product gaps, implement targeted improvements, review safety and accessibility, improve mood continuity, and verify the final implementation.

### Bob-assisted development highlights

#### 1. Initial Project Assessment

Bob analyzed the existing application and identified gaps in testing, personalization, safety, accessibility, and developer workflow.

![Initial Bob Assessment](P1-01 Executive Assessment and Architecture.png)

#### 2. 360° Product & Hackathon Review

Bob reviewed ElderEase AI across product experience, AI quality, safety, engineering quality, business value, originality, demo potential, and hackathon readiness.

![Bob 360 Assessment](![Uploading P1 B - Bob 360 Assessment.png…]()
Day2_P1_360_Assessment.png)

#### 3. Bob-Assisted Product Improvement

Bob helped implement and verify mood trend awareness, allowing ElderEase to recognize whether recent check-ins are moving in a more positive or difficult direction.

![Mood Trend Improvement](docs/bob-evidence/Day2_P3_Mood_Trend.png)

#### 4. Final Verification

The final Bob-assisted verification confirmed:

**100 tests · 100 passed · 0 failed · 0 errors**

with **100% coverage for `mood_engine.py` and `activity_engine.py`**.

![Final Bob Verification](docs/bob-evidence/FINAL_Bob_Verification_100_Tests.png)

[View all Bob development evidence](docs/bob-evidence/)



## 🎬 Demo Flow

1. **Open the app** — large title, readable subtitle, clean light background
2. **Quick check-in** — use the descriptive dropdown, click "✅ Record this mood"
3. **Send a message** — type "I feel quite lonely today, I miss talking to my children" — observe the mood-coloured response card using the user's own words
4. **Mood trend** — after 3+ messages with a pattern, observe the gentle trend notice
5. **Safety path** — type "I don't want to go on" — observe the red-bordered safety card with Tele-MANAS numbers (no activity suggested)
6. **Mood diary** — scroll down to see the timestamped mood history
7. **Test evidence** — show terminal: `100 passed in 0.59s`

---

## ⚠️ Limitations

- Mood detection is keyword-based; nuanced or indirect emotional language may not be captured
- Session data is not persisted — history resets on page refresh
- The trend algorithm requires at least 3 chat interactions per session
- The application is in English only
- ElderEase is not a substitute for professional mental health support

---

## 🔮 Future Improvements

- Persistent mood diary (file-based, no cloud dependency needed)
- Multi-language support (Hindi, Tamil, Bengali)
- Voice input for users with limited typing ability
- Family caregiver view (read-only mood summary)
- Expanded activity library with regional cultural suggestions

---

## 📋 Disclaimer

ElderEase AI offers gentle emotional support and simple wellbeing suggestions. It is not a medical service, therapist, or emergency service. If you or someone you know is in distress, please speak to a trusted person or call **Tele-MANAS: 14416** or **1800-89-14416** (free, 24 hours, available across India).
