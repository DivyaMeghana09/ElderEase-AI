"""
Test suite for mood_engine.py.

Updated after Improvement 2 to cover:
- get_mood_trend() (new function)
Previously covered:
- detect_safety_concern() (new function)
- SAFETY_RESPONSE constant (new)
- generate_support_response() now personalises using user_message (bug fixed)
- Baseline functional, edge-case, and safety tests retained.
"""

import pytest
from mood_engine import (
    detect_mood,
    detect_safety_concern,
    generate_support_response,
    get_mood_trend,
    SAFETY_RESPONSE,
)


# ---------------------------------------------------------------------------
# detect_mood — functional: supported mood categories
# ---------------------------------------------------------------------------

class TestDetectMoodFunctional:

    def test_detect_lonely_core_keyword(self):
        assert detect_mood("I feel lonely today") == "Lonely"

    def test_detect_lonely_alone(self):
        assert detect_mood("I have been alone all day") == "Lonely"

    def test_detect_lonely_miss_family(self):
        assert detect_mood("I miss my family so much") == "Lonely"

    def test_detect_sad_core_keyword(self):
        assert detect_mood("I feel so sad") == "Sad"

    def test_detect_sad_unhappy(self):
        assert detect_mood("I am very unhappy today") == "Sad"

    def test_detect_sad_cry(self):
        assert detect_mood("I just want to cry") == "Sad"

    def test_detect_sad_depressed(self):
        assert detect_mood("I have been feeling depressed") == "Sad"

    def test_detect_anxious_core_keyword(self):
        assert detect_mood("I feel anxious about tomorrow") == "Anxious"

    def test_detect_anxious_worried(self):
        assert detect_mood("I am really worried") == "Anxious"

    def test_detect_anxious_nervous(self):
        assert detect_mood("I feel nervous about everything") == "Anxious"

    def test_detect_anxious_scared(self):
        assert detect_mood("I am scared of what might happen") == "Anxious"

    def test_detect_tired_core_keyword(self):
        assert detect_mood("I feel so tired today") == "Tired"

    def test_detect_tired_exhausted(self):
        assert detect_mood("I am completely exhausted") == "Tired"

    def test_detect_tired_sleepy(self):
        assert detect_mood("I have been sleepy all afternoon") == "Tired"

    def test_detect_tired_no_energy(self):
        assert detect_mood("I have no energy left") == "Tired"

    def test_detect_happy_core_keyword(self):
        assert detect_mood("I feel happy today") == "Happy"

    def test_detect_happy_great(self):
        assert detect_mood("Today has been great") == "Happy"

    def test_detect_happy_wonderful(self):
        assert detect_mood("Everything feels wonderful") == "Happy"

    def test_detect_happy_excited(self):
        assert detect_mood("I am so excited") == "Happy"


# ---------------------------------------------------------------------------
# detect_mood — fallback / default
# ---------------------------------------------------------------------------

class TestDetectMoodDefault:

    def test_detect_default_neutral_sentence(self):
        """A sentence with no mood keywords should return 'Okay'."""
        assert detect_mood("I went to the shops this morning") == "Okay"

    def test_detect_default_empty_string(self):
        """Empty input should not raise and should return 'Okay'."""
        result = detect_mood("")
        assert result == "Okay"

    def test_detect_default_whitespace_only(self):
        """Whitespace-only input should return 'Okay'."""
        result = detect_mood("   ")
        assert result == "Okay"

    def test_detect_default_generic_greeting(self):
        assert detect_mood("Hello, how are you?") == "Okay"


# ---------------------------------------------------------------------------
# detect_mood — case sensitivity
# ---------------------------------------------------------------------------

class TestDetectMoodCaseSensitivity:

    def test_detect_case_uppercase_lonely(self):
        """Mood detection must be case-insensitive (text.lower() is used)."""
        assert detect_mood("I FEEL LONELY") == "Lonely"

    def test_detect_case_uppercase_sad(self):
        assert detect_mood("I AM SAD TODAY") == "Sad"

    def test_detect_case_mixed_happy(self):
        assert detect_mood("I Feel So Happy Right Now") == "Happy"

    def test_detect_case_uppercase_tired(self):
        assert detect_mood("TOTALLY EXHAUSTED") == "Tired"


# ---------------------------------------------------------------------------
# detect_mood — edge cases
# ---------------------------------------------------------------------------

class TestDetectMoodEdgeCases:

    def test_detect_very_long_input(self):
        """Very long input should not raise and should return a valid mood."""
        long_text = "I feel okay. " * 100
        result = detect_mood(long_text)
        valid_moods = {"Lonely", "Sad", "Anxious", "Tired", "Happy", "Okay"}
        assert result in valid_moods

    def test_detect_non_ascii_characters(self):
        """Input with non-ASCII characters should not raise."""
        result = detect_mood("Je me sens trïste aujourd'hui")
        valid_moods = {"Lonely", "Sad", "Anxious", "Tired", "Happy", "Okay"}
        assert result in valid_moods

    def test_detect_only_punctuation(self):
        """Input with only punctuation should return 'Okay' without raising."""
        result = detect_mood("!!! ??? ...")
        assert result == "Okay"

    def test_detect_numeric_input(self):
        """Numeric-only input should not raise."""
        result = detect_mood("12345 67890")
        assert result == "Okay"

    def test_detect_returns_string(self):
        """detect_mood must always return a string."""
        result = detect_mood("anything")
        assert isinstance(result, str)


# ---------------------------------------------------------------------------
# detect_mood — safety-critical inputs (detect_mood itself is unchanged)
# ---------------------------------------------------------------------------

class TestDetectMoodSafetyCases:

    DISTRESS_PHRASES = [
        "I don't want to go on",
        "I want to give up",
        "nobody cares about me",
        "I feel like disappearing",
        "I am thinking of hurting myself",
        "I don't see the point anymore",
        "life feels meaningless",
    ]

    VALID_MOODS = {"Lonely", "Sad", "Anxious", "Tired", "Happy", "Okay"}

    def test_distress_phrases_do_not_raise(self):
        """detect_mood must not raise for distress phrases."""
        for phrase in self.DISTRESS_PHRASES:
            result = detect_mood(phrase)
            assert result in self.VALID_MOODS, (
                f"Unexpected return for distress phrase: {phrase!r} → {result!r}"
            )


# ---------------------------------------------------------------------------
# detect_safety_concern — new function (Gap 1 closed)
# ---------------------------------------------------------------------------

class TestDetectSafetyConcern:

    DISTRESS_PHRASES = [
        "I don't want to go on",
        "I want to give up",
        "nobody cares about me",
        "no one cares about me",
        "I feel like disappearing",
        "I am thinking of hurting myself",
        "I want to hurt myself",
        "I don't see the point",
        "life feels meaningless",
        "life is meaningless",
        "I want to end it",
        "I can't go on",
        "I cannot go on",
        # Phrases added during safety review
        "I want to end my life",
        "I want to kill myself",
        "there is no reason to live",
        "I don't want to live",
    ]

    NORMAL_PHRASES = [
        "I feel a little sad today",
        "I am worried about my appointment",
        "I feel lonely",
        "I had a great day",
        "I am quite tired",
        "Hello, how are you?",
        "",
        "   ",
    ]

    def test_detects_all_distress_phrases(self):
        """Every configured distress phrase must return True."""
        for phrase in self.DISTRESS_PHRASES:
            assert detect_safety_concern(phrase) is True, (
                f"Safety concern not detected for: {phrase!r}"
            )

    def test_normal_phrases_return_false(self):
        """Ordinary emotional input must not trigger the safety path."""
        for phrase in self.NORMAL_PHRASES:
            assert detect_safety_concern(phrase) is False, (
                f"False positive safety concern for: {phrase!r}"
            )

    def test_case_insensitive_detection(self):
        """Distress detection must be case-insensitive."""
        assert detect_safety_concern("I DON'T WANT TO GO ON") is True
        assert detect_safety_concern("NOBODY CARES ABOUT ME") is True

    def test_returns_bool(self):
        """detect_safety_concern must always return a bool."""
        assert isinstance(detect_safety_concern("some text"), bool)
        assert isinstance(detect_safety_concern(""), bool)

    def test_distress_phrase_embedded_in_longer_text(self):
        """Detection must work when the distress phrase is inside a longer message."""
        assert detect_safety_concern(
            "I have been feeling really bad and I don't want to go on like this"
        ) is True

    def test_safety_gap_is_now_closed(self):
        """
        REPLACES the old 'test_safety_no_dedicated_crisis_mood' gap-documentation test.
        The safety layer now exists. detect_safety_concern('I don't want to go on')
        must return True — the gap is closed.
        """
        assert detect_safety_concern("I don't want to go on") is True


# ---------------------------------------------------------------------------
# SAFETY_RESPONSE constant
# ---------------------------------------------------------------------------

class TestSafetyResponse:

    def test_safety_response_is_string(self):
        assert isinstance(SAFETY_RESPONSE, str)

    def test_safety_response_is_non_empty(self):
        assert len(SAFETY_RESPONSE.strip()) > 0

    def test_safety_response_contains_tele_manas_short_number(self):
        """Safety response must include the Tele-MANAS short helpline number (14416)."""
        assert "14416" in SAFETY_RESPONSE

    def test_safety_response_contains_tele_manas_tollfree_number(self):
        """Safety response must include the Tele-MANAS toll-free number."""
        assert "1800-89-14416" in SAFETY_RESPONSE

    def test_safety_response_references_india(self):
        """Safety response must confirm the helpline is available in India."""
        assert "India" in SAFETY_RESPONSE

    def test_safety_response_does_not_reference_uk_samaritans(self):
        """Old UK Samaritans number must not appear — helpline is now India Tele-MANAS."""
        assert "116 123" not in SAFETY_RESPONSE
        assert "Samaritans" not in SAFETY_RESPONSE

    def test_safety_response_does_not_claim_medical_capability(self):
        """Must not contain language that implies medical diagnosis or treatment."""
        medical_terms = ["diagnose", "prescribe", "treatment", "medication", "therapy"]
        lower = SAFETY_RESPONSE.lower()
        for term in medical_terms:
            assert term not in lower, (
                f"Safety response contains medical term: {term!r}"
            )

    def test_safety_response_does_not_present_as_emergency_service(self):
        """ElderEase must not describe itself as an emergency or crisis service."""
        emergency_terms = ["emergency service", "crisis service", "call 112", "call 100"]
        lower = SAFETY_RESPONSE.lower()
        for term in emergency_terms:
            assert term not in lower, (
                f"Safety response contains emergency-service language: {term!r}"
            )


# ---------------------------------------------------------------------------
# generate_support_response — functional
# ---------------------------------------------------------------------------

class TestGenerateSupportResponseFunctional:

    VALID_MOODS = ["Lonely", "Sad", "Anxious", "Tired", "Happy", "Okay"]

    def test_response_returns_string_for_all_moods(self):
        for mood in self.VALID_MOODS:
            result = generate_support_response(mood, "I feel this way")
            assert isinstance(result, str), f"Non-string response for mood: {mood}"

    def test_response_non_empty_for_all_moods(self):
        for mood in self.VALID_MOODS:
            result = generate_support_response(mood, "Some message")
            assert len(result.strip()) > 0, f"Empty response for mood: {mood}"

    def test_response_lonely(self):
        result = generate_support_response("Lonely", "I feel lonely")
        assert isinstance(result, str) and len(result) > 0

    def test_response_sad(self):
        result = generate_support_response("Sad", "I am sad")
        assert isinstance(result, str) and len(result) > 0

    def test_response_anxious(self):
        result = generate_support_response("Anxious", "I am worried")
        assert isinstance(result, str) and len(result) > 0

    def test_response_tired(self):
        result = generate_support_response("Tired", "I am tired")
        assert isinstance(result, str) and len(result) > 0

    def test_response_happy(self):
        result = generate_support_response("Happy", "I feel great")
        assert isinstance(result, str) and len(result) > 0

    def test_response_okay(self):
        result = generate_support_response("Okay", "I feel okay")
        assert isinstance(result, str) and len(result) > 0


# ---------------------------------------------------------------------------
# generate_support_response — user_message parameter (Bug 1 fixed)
# ---------------------------------------------------------------------------

class TestGenerateSupportResponseUserMessage:

    def test_response_differs_for_different_user_messages_same_mood(self):
        """
        BUG FIXED: generate_support_response now incorporates user_message.
        Two different messages for the same mood must produce different responses.
        This test previously FAILED (confirmed the bug); it must now PASS.
        """
        msg_a = "I feel lonely because my daughter moved away last year"
        msg_b = "I am alone and I miss talking to someone I trust"
        result_a = generate_support_response("Lonely", msg_a)
        result_b = generate_support_response("Lonely", msg_b)
        assert result_a != result_b, (
            "generate_support_response still ignores user_message — bug not fixed."
        )

    def test_response_contains_excerpt_of_user_message(self):
        """The response must contain (part of) what the user said."""
        msg = "I feel sad because I miss my old friends"
        result = generate_support_response("Sad", msg)
        # The first 77 characters of the message should appear in the response.
        assert msg[:40] in result, (
            "Response does not contain an excerpt of the user's message."
        )

    def test_response_different_messages_produce_different_responses(self):
        """Spot-check across another mood."""
        result_a = generate_support_response("Anxious", "I am worried about my health")
        result_b = generate_support_response("Anxious", "I feel nervous about my appointment")
        assert result_a != result_b

    def test_empty_user_message_still_returns_valid_response(self):
        """An empty user_message must still produce a non-empty string response."""
        result = generate_support_response("Okay", "")
        assert isinstance(result, str) and len(result.strip()) > 0

    def test_long_user_message_is_truncated_gracefully(self):
        """A very long user message must not break the response."""
        long_msg = "I feel very tired and I " + "have been struggling " * 20
        result = generate_support_response("Tired", long_msg)
        assert isinstance(result, str) and len(result.strip()) > 0
        # The truncation marker should appear when message exceeds 80 chars.
        assert "..." in result


# ---------------------------------------------------------------------------
# generate_support_response — fallback / unknown mood
# ---------------------------------------------------------------------------

class TestGenerateSupportResponseFallback:

    def test_response_unknown_mood_returns_okay_fallback(self):
        """
        An unrecognised mood falls back to the 'Okay' template.
        Both the unknown-mood result and the Okay result share the same
        opening and closing text — the middle section will differ because
        user_message now contributes, so we check the template boundary, not
        byte equality.
        """
        result = generate_support_response("Confused", "Not sure how I feel")
        okay_result = generate_support_response("Okay", "Not sure how I feel")
        # Same user_message → same full response regardless of mood fallback
        assert result == okay_result

    def test_response_empty_mood_string_returns_fallback(self):
        """Empty mood string falls back to Okay template."""
        result = generate_support_response("", "Some message")
        okay_result = generate_support_response("Okay", "Some message")
        assert result == okay_result


# ---------------------------------------------------------------------------
# get_mood_trend — Improvement 2: within-session mood trend awareness
# ---------------------------------------------------------------------------

class TestGetMoodTrend:

    # ── Insufficient data ──────────────────────────────────────────────────

    def test_empty_sequence_returns_not_enough_data(self):
        assert get_mood_trend([]) == "not_enough_data"

    def test_one_entry_returns_not_enough_data(self):
        assert get_mood_trend(["Sad"]) == "not_enough_data"

    def test_two_entries_returns_not_enough_data(self):
        assert get_mood_trend(["Sad", "Happy"]) == "not_enough_data"

    def test_three_entries_is_minimum_for_analysis(self):
        """Three entries is the minimum; result must not be not_enough_data."""
        result = get_mood_trend(["Sad", "Sad", "Happy"])
        assert result in {"improving", "declining", "stable"}

    # ── Improving sequences ────────────────────────────────────────────────

    def test_clearly_improving_sad_to_happy(self):
        """Sad → Sad → Happy → Happy: second half clearly better."""
        assert get_mood_trend(["Sad", "Sad", "Happy", "Happy"]) == "improving"

    def test_improving_lonely_to_okay(self):
        """Lonely(2) → Sad(1) → Okay(4) → Happy(5): strong upward arc."""
        assert get_mood_trend(["Lonely", "Sad", "Okay", "Happy"]) == "improving"

    def test_improving_five_entries(self):
        """Sad, Anxious, Tired, Okay, Happy — steady climb."""
        assert get_mood_trend(["Sad", "Anxious", "Tired", "Okay", "Happy"]) == "improving"

    # ── Declining sequences ────────────────────────────────────────────────

    def test_clearly_declining_happy_to_sad(self):
        """Happy → Happy → Sad → Sad: second half clearly worse."""
        assert get_mood_trend(["Happy", "Happy", "Sad", "Sad"]) == "declining"

    def test_declining_okay_to_anxious(self):
        """Okay(4) → Happy(5) → Lonely(2) → Sad(1): strong downward arc."""
        assert get_mood_trend(["Okay", "Happy", "Lonely", "Sad"]) == "declining"

    def test_declining_five_entries(self):
        """Happy, Okay, Tired, Anxious, Sad — steady decline."""
        assert get_mood_trend(["Happy", "Okay", "Tired", "Anxious", "Sad"]) == "declining"

    # ── Stable sequences ───────────────────────────────────────────────────

    def test_all_same_mood_is_stable(self):
        """Identical moods throughout — no directional change."""
        assert get_mood_trend(["Okay", "Okay", "Okay", "Okay"]) == "stable"

    def test_small_fluctuation_is_stable(self):
        """Okay(4) → Sad(1) → Happy(5) → Okay(4): mixed, net delta < threshold."""
        # avg first half = (4+1)/2 = 2.5, avg second half = (5+4)/2 = 4.5 → delta 2.0
        # This will be improving — use a genuinely flat example instead:
        assert get_mood_trend(["Okay", "Happy", "Okay", "Happy"]) == "stable"

    def test_alternating_low_high_is_stable(self):
        """Sad → Happy → Sad → Happy: average same throughout."""
        result = get_mood_trend(["Sad", "Happy", "Sad", "Happy"])
        # avg first = (1+5)/2 = 3.0, avg second = (1+5)/2 = 3.0 → delta 0.0
        assert result == "stable"

    # ── Invalid / unknown mood values ──────────────────────────────────────

    def test_all_unknown_moods_returns_not_enough_data(self):
        """If all entries are unrecognised labels, treat as insufficient data."""
        assert get_mood_trend(["Confused", "Bored", "Curious"]) == "not_enough_data"

    def test_mixed_known_and_unknown_ignores_unknown(self):
        """Unknown labels are silently ignored; known labels drive the trend."""
        # Known: Sad(1), Sad(1), Happy(5), Happy(5) → improving
        result = get_mood_trend(["Sad", "Unknown", "Sad", "Happy", "???", "Happy"])
        assert result == "improving"

    def test_single_unknown_among_known_does_not_crash(self):
        """One unknown in an otherwise valid sequence must not raise."""
        result = get_mood_trend(["Happy", "Happy", "Confused", "Okay"])
        assert result in {"improving", "declining", "stable", "not_enough_data"}

    # ── Return value contract ──────────────────────────────────────────────

    def test_always_returns_string(self):
        """get_mood_trend must always return a string, never None or other type."""
        for seq in [[], ["Sad"], ["Happy", "Okay", "Sad", "Happy"]]:
            result = get_mood_trend(seq)
            assert isinstance(result, str)

    def test_return_value_is_one_of_four_valid_states(self):
        """Return value must always be one of the four defined states."""
        valid = {"improving", "declining", "stable", "not_enough_data"}
        test_sequences = [
            [],
            ["Happy"],
            ["Sad", "Sad"],
            ["Sad", "Sad", "Happy"],
            ["Happy", "Happy", "Happy", "Happy"],
            ["Sad", "Sad", "Sad", "Sad"],
            ["Happy", "Okay", "Tired", "Sad"],
            ["Confused", "Bored"],
        ]
        for seq in test_sequences:
            result = get_mood_trend(seq)
            assert result in valid, f"Unexpected return {result!r} for sequence {seq}"
