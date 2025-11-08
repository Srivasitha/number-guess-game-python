# game/core.py
import random
from dataclasses import dataclass, field
from typing import Optional, List, Tuple

@dataclass
class GuessResult:
    correct: bool
    message: str
    points_lost: int
    current_score: int
    attempts_left: Optional[int] = None
    guess: Optional[int] = None

@dataclass
class HintInfo:
    name: str
    cost: int
    description: str

class GuessingGame:
    def __init__(
        self,
        low: int = 1,
        high: int = 100,
        max_attempts: Optional[int] = None,
        starting_score: int = 100,
        penalty_per_wrong: Optional[int] = None,
    ):
        self.low = low
        self.high = high
        self.max_attempts = max_attempts
        self.starting_score = starting_score
        self.penalty_per_wrong = penalty_per_wrong
        self.reset()

    def reset(self):
        self.target = random.randint(self.low, self.high)
        self.attempts = 0
        self.guesses: List[int] = []
        self.score = self.starting_score
        range_size = self.high - self.low + 1
        if self.penalty_per_wrong is None:
            self.penalty_per_wrong = max(1, range_size // 20)
        self.last_distance: Optional[int] = None
        # track eliminated segments for hints shop
        self.eliminated_segments: List[Tuple[int,int]] = []

    # ----- core guess logic -----
    def make_guess(self, guess: int) -> GuessResult:
        if guess < self.low or guess > self.high:
            return GuessResult(False, f"Guess must be between {self.low} and {self.high}.", 0, self.score, self.max_attempts - self.attempts if self.max_attempts else None, guess)

        # If guess falls into an eliminated segment, warn but allow
        for seg_low, seg_high in self.eliminated_segments:
            if seg_low <= guess <= seg_high:
                # allow guessing but inform
                break

        self.attempts += 1
        self.guesses.append(guess)
        distance = abs(self.target - guess)

        if guess == self.target:
            bonus = max(0, (self.high - self.low) // (self.attempts or 1))
            final_message = f"Correct! You guessed {self.target} in {self.attempts} attempts."
            self.score += bonus
            return GuessResult(True, final_message, 0, self.score, None, guess)

        # wrong guess
        points_lost = self.penalty_per_wrong
        self.score -= points_lost

        # warm/colder hint
        warm_colder = ""
        if self.last_distance is not None:
            if distance < self.last_distance:
                warm_colder = " (Warmer than previous)"
            elif distance > self.last_distance:
                warm_colder = " (Colder than previous)"
            else:
                warm_colder = " (Same distance as previous)"
        self.last_distance = distance

        if guess < self.target:
            message = f"Too low.{warm_colder}"
        else:
            message = f"Too high.{warm_colder}"

        attempts_left = None
        if self.max_attempts is not None:
            attempts_left = self.max_attempts - self.attempts

        return GuessResult(False, message, points_lost, max(0, self.score), attempts_left, guess)

    def is_over(self) -> bool:
        if self.score <= 0:
            return True
        if self.max_attempts is not None and self.attempts >= self.max_attempts:
            return True
        return False

    # ----- hint shop -----
    def available_hints(self) -> List[HintInfo]:
        """Return list of available hint types with costs."""
        # costs scale with range size
        range_size = max(1, self.high - self.low + 1)
        return [
            HintInfo("parity", max(5, range_size // 20), "Reveal whether the number is even or odd."),
            HintInfo("within_10", max(8, range_size // 15), "Tell whether the target is within ±10 of an anchor you choose."),
            HintInfo("eliminate_third", max(12, range_size // 10), "Eliminate one third of the range that does NOT contain the number."),
            HintInfo("digit_sum", max(7, range_size // 25), "Reveal sum of digits of the target (useful for pattern reasoning)."),
        ]

    def buy_hint(self, hint_key: str, **kwargs):
        """
        Buy a hint. Returns (success:bool, message:str).
        hint_key: 'parity', 'within_10', 'eliminate_third', 'digit_sum'
        kwargs used by some hints (e.g., for within_10 you can supply 'anchor' int)
        """
        mapping = {h.name: h for h in self.available_hints()}
        if hint_key not in mapping:
            return False, "Invalid hint key."

        hint = mapping[hint_key]
        if self.score < hint.cost:
            return False, f"Not enough points to buy this hint. Cost: {hint.cost}, your score: {self.score}"

        # Deduct cost now
        self.score -= hint.cost

        if hint_key == "parity":
            parity = "even" if self.target % 2 == 0 else "odd"
            return True, f"The target is {parity}. (-{hint.cost} pts)"

        if hint_key == "digit_sum":
            s = sum(int(d) for d in str(abs(self.target)))
            return True, f"The sum of digits is {s}. (-{hint.cost} pts)"

        if hint_key == "within_10":
            # anchor is optional; if provided, tell whether target within ±10 of that anchor
            anchor = kwargs.get("anchor")
            if anchor is None:
                # provide a suggested anchor: last guess or midpoint
                anchor = self.guesses[-1] if self.guesses else (self.low + self.high) // 2
            within = abs(self.target - anchor) <= 10
            return True, f"Anchor: {anchor}. Target within ±10 of {anchor}? {'Yes' if within else 'No'}. (-{hint.cost} pts)"

        if hint_key == "eliminate_third":
            # split current [low, high] into 3 approx equal parts, eliminate one that doesn't contain target
            span = self.high - self.low + 1
            part = max(1, span // 3)
            segments = []
            start = self.low
            while start <= self.high:
                end = min(self.high, start + part - 1)
                segments.append((start, end))
                start = end + 1
            # find which segment contains target
            keep_index = 0
            for i, (a, b) in enumerate(segments):
                if a <= self.target <= b:
                    keep_index = i
                    break
            # choose one segment to eliminate that's not the keep one
            elim_index = (keep_index + 1) % len(segments) if len(segments) > 1 else None
            if elim_index is None:
                return True, "Range too small to eliminate a segment."
            elim_seg = segments[elim_index]
            self.eliminated_segments.append(elim_seg)
            return True, f"Eliminated numbers from {elim_seg[0]} to {elim_seg[1]}. (-{hint.cost} pts)"

        return False, "Hint implementation missing."

    # small helper for UI to show eliminated segments compactly
    def eliminated_summary(self) -> str:
        if not self.eliminated_segments:
            return ""
        parts = [f"{a}-{b}" for (a, b) in self.eliminated_segments]
        return "Eliminated: " + ", ".join(parts)
