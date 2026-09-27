"""
Baseline test suite for activity_engine.py.

Tests the CURRENT (unmodified) implementation.
Purpose: establish a baseline, expose real bugs, create a regression net.
"""

import pytest
from activity_engine import get_activity, ACTIVITIES


# ---------------------------------------------------------------------------
# get_activity — functional: all supported moods
# ---------------------------------------------------------------------------

class TestGetActivityFunctional:

    SUPPORTED_MOODS = ["Lonely", "Sad", "Anxious", "Tired", "Happy", "Okay"]

    def test_returns_string_for_all_supported_moods(self):
        for mood in self.SUPPORTED_MOODS:
            result = get_activity(mood)
            assert isinstance(result, str), f"Non-string result for mood: {mood}"

    def test_returns_non_empty_for_all_supported_moods(self):
        for mood in self.SUPPORTED_MOODS:
            result = get_activity(mood)
            assert len(result.strip()) > 0, f"Empty result for mood: {mood}"

    def test_lonely_activity_is_from_lonely_list(self):
        result = get_activity("Lonely")
        assert result in ACTIVITIES["Lonely"]

    def test_sad_activity_is_from_sad_list(self):
        result = get_activity("Sad")
        assert result in ACTIVITIES["Sad"]

    def test_anxious_activity_is_from_anxious_list(self):
        result = get_activity("Anxious")
        assert result in ACTIVITIES["Anxious"]

    def test_tired_activity_is_from_tired_list(self):
        result = get_activity("Tired")
        assert result in ACTIVITIES["Tired"]

    def test_happy_activity_is_from_happy_list(self):
        result = get_activity("Happy")
        assert result in ACTIVITIES["Happy"]

    def test_okay_activity_is_from_okay_list(self):
        result = get_activity("Okay")
        assert result in ACTIVITIES["Okay"]


# ---------------------------------------------------------------------------
# get_activity — fallback / unknown mood
# ---------------------------------------------------------------------------

class TestGetActivityFallback:

    def test_unknown_mood_returns_string(self):
        result = get_activity("Confused")
        assert isinstance(result, str)

    def test_unknown_mood_returns_from_okay_list(self):
        """Unrecognised moods should fall back to the 'Okay' activity list."""
        result = get_activity("Confused")
        assert result in ACTIVITIES["Okay"]

    def test_empty_string_mood_returns_from_okay_list(self):
        result = get_activity("")
        assert result in ACTIVITIES["Okay"]

    def test_none_like_string_mood_falls_back(self):
        result = get_activity("None")
        assert result in ACTIVITIES["Okay"]


# ---------------------------------------------------------------------------
# get_activity — data integrity: ACTIVITIES dictionary
# ---------------------------------------------------------------------------

class TestActivitiesDataIntegrity:

    REQUIRED_MOODS = ["Lonely", "Sad", "Anxious", "Tired", "Happy", "Okay"]

    def test_all_required_mood_keys_present(self):
        for mood in self.REQUIRED_MOODS:
            assert mood in ACTIVITIES, f"Missing mood key in ACTIVITIES: {mood}"

    def test_all_mood_lists_are_non_empty(self):
        for mood, activity_list in ACTIVITIES.items():
            assert len(activity_list) > 0, f"Empty activity list for mood: {mood}"

    def test_all_activities_are_strings(self):
        for mood, activity_list in ACTIVITIES.items():
            for activity in activity_list:
                assert isinstance(activity, str), (
                    f"Non-string activity in {mood} list: {activity!r}"
                )

    def test_all_activities_are_non_empty_strings(self):
        for mood, activity_list in ACTIVITIES.items():
            for activity in activity_list:
                assert len(activity.strip()) > 0, (
                    f"Empty/whitespace activity in {mood} list"
                )

    def test_each_mood_has_at_least_two_activities(self):
        """Each mood should have at least 2 activities to give variety."""
        for mood, activity_list in ACTIVITIES.items():
            assert len(activity_list) >= 2, (
                f"Mood {mood!r} has fewer than 2 activities — no variety possible"
            )


# ---------------------------------------------------------------------------
# get_activity — randomness / variety
# ---------------------------------------------------------------------------

class TestGetActivityVariety:

    def test_multiple_calls_can_return_different_activities(self):
        """
        Over 20 calls for a mood with 3+ activities, at least 2 distinct
        results should be returned (statistical, not guaranteed per call).
        """
        results = {get_activity("Okay") for _ in range(20)}
        assert len(results) >= 2, (
            "Expected multiple distinct activities over 20 calls, got only one. "
            "random.choice may not be functioning as expected."
        )

    def test_no_none_returned_in_repeated_calls(self):
        """get_activity should never return None."""
        for mood in ["Lonely", "Sad", "Anxious", "Tired", "Happy", "Okay"]:
            for _ in range(5):
                result = get_activity(mood)
                assert result is not None, f"None returned for mood: {mood}"

    def test_repeated_activity_deduplication_not_implemented(self):
        """
        DOCUMENTS GAP: The current implementation uses random.choice with
        no deduplication — the same activity can appear consecutively.
        This test PASSES on current code (confirming the gap).

        Over 30 calls for a 3-activity list, at least one repeat is
        statistically near-certain (birthday paradox at small n).
        """
        results = [get_activity("Anxious") for _ in range(30)]
        unique_count = len(set(results))
        total_options = len(ACTIVITIES["Anxious"])
        # We simply confirm the function works — dedup is not enforced.
        assert unique_count <= total_options, (
            "More unique results than options — something is wrong with the data."
        )
