# tests/test_core.py
import pytest
from game.core import GuessingGame

def test_correct_guess():
    g = GuessingGame(low=1, high=10)
    g.target = 5
    res = g.make_guess(5)
    assert res.correct
    assert "Correct" in res.message

def test_too_low_and_penalty():
    g = GuessingGame(low=1, high=10, starting_score=50, penalty_per_wrong=2)
    g.target = 8
    prev_score = g.score
    res = g.make_guess(3)
    assert not res.correct
    assert "Too low" in res.message
    assert res.points_lost == 2
    assert g.score == prev_score - 2
