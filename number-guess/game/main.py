# game/main.py
from game.core import GuessingGame
from game.score import save_highscore, pretty_highscores
from game.utils import get_int_input
from colorama import Fore, Style, init as colorama_init

colorama_init(autoreset=True)

def colored(text, color):
    return f"{color}{text}{Style.RESET_ALL}"

def choose_base_mode():
    print("Choose mode:")
    print("1) Casual (progressive levels) [default]")
    print("2) Fixed difficulty (easy/medium/hard)")
    choice = input("Enter choice (1/2): ").strip()
    if choice == "2":
        return "fixed"
    return "progressive"

def create_game_for_level(level: int, mode: str = "progressive", fixed_choice: str = "2"):
    # progressive mode: level 1 -> range 1..20, level 2 -> 1..40, etc.
    if mode == "progressive":
        base = 20
        high = base * level
        low = 1
        starting_score = 100 + (level - 1) * 20
        max_attempts = max(10, 20 - level)  # as level increases, attempts decrease slightly
        return GuessingGame(low=low, high=high, max_attempts=max_attempts, starting_score=starting_score)
    # fixed difficulties if chosen
    if fixed_choice == "1":
        return GuessingGame(low=1, high=50, starting_score=120, max_attempts=None)
    if fixed_choice == "3":
        return GuessingGame(low=1, high=500, starting_score=80, max_attempts=15)
    # default medium
    return GuessingGame(low=1, high=100, starting_score=100, max_attempts=20)

def show_hint_menu(game: GuessingGame):
    print(colored("\n--- HINT SHOP ---", Fore.CYAN))
    hints = game.available_hints()
    for i, h in enumerate(hints, 1):
        print(f"{i}) {h.name} — cost {h.cost} pts — {h.description}")
    print("0) Cancel")

    choice = input("Select hint number: ").strip()
    if not choice.isdigit():
        print("Invalid input.")
        return
    choice = int(choice)
    if choice == 0:
        return
    if 1 <= choice <= len(hints):
        h = hints[choice - 1]
        # if within_10, ask for optional anchor
        if h.name == "within_10":
            anchor = input("Enter anchor number to check around (leave blank to use last guess/midpoint): ").strip()
            anchor_val = None
            if anchor != "":
                try:
                    anchor_val = int(anchor)
                except ValueError:
                    print("Invalid anchor — using default.")
            ok, msg = game.buy_hint(h.name, anchor=anchor_val)
        else:
            ok, msg = game.buy_hint(h.name)
        if ok:
            print(colored(msg, Fore.MAGENTA))
        else:
            print(colored(msg, Fore.RED))
    else:
        print("Invalid choice.")

def play_level(level: int, mode: str):
    game = create_game_for_level(level, mode)
    print(colored(f"\n=== LEVEL {level} — Guess a number between {game.low} and {game.high} ===", Fore.GREEN))
    print(colored(f"Starting score: {game.starting_score} | Attempts allowed: {game.max_attempts}", Fore.YELLOW))

    while not game.is_over():
        # show eliminated segments summary if any
        if game.eliminated_summary():
            print(colored(game.eliminated_summary(), Fore.CYAN))

        print("\nOptions: [G]uess  [H]int Shop  [S]coreboard  [Q]uit level")
        opt = input("Choose option (G/H/S/Q): ").strip().lower()
        if opt == "h":
            show_hint_menu(game)
            continue
        if opt == "s":
            print(pretty_highscores())
            continue
        if opt == "q":
            print("Quitting level.")
            break
        # default to guess
        guess = get_int_input(f"Your guess ({game.low}-{game.high}): ")
        res = game.make_guess(guess)
        if res.correct:
            print(colored(res.message, Fore.GREEN))
            print(colored(f"Final score: {res.current_score}", Fore.YELLOW))
            name = input("Enter name to save highscore (leave blank to skip): ").strip()
            if name:
                # difficulty label includes level to show progression
                save_highscore(name, res.current_score, game.attempts, f"Level {level}")
            return True, game  # level was won
        else:
            # wrong guess prints
            print(colored(res.message, Fore.RED))
            if res.points_lost:
                print(colored(f" - Points lost: {res.points_lost}  Current score: {res.current_score}", Fore.YELLOW))
            if res.attempts_left is not None:
                print(colored(f"Attempts left: {res.attempts_left}", Fore.MAGENTA))
            if game.is_over():
                print(colored("Game over for this level.", Fore.RED))
                print(colored(f"The number was: {game.target}", Fore.CYAN))
                return False, game
    # if exited loop due to quit or score 0
    return False, game

def main():
    print(colored("NUMBER GUESSING GAME — Level Progression + Hint Shop", Fore.CYAN))
    mode = choose_base_mode()
    fixed_choice = None
    if mode == "fixed":
        print("Choose fixed difficulty: 1) Easy 2) Medium 3) Hard")
        fixed_choice = input("Enter 1/2/3: ").strip() or "2"

    level = 1
    while True:
        won, game = play_level(level, mode)
        if won:
            print(colored(f"Great — you cleared level {level}!", Fore.GREEN))
            # move to next level automatically
            level += 1
            cont = input("Proceed to next level? (y/n): ").strip().lower()
            if cont != "y":
                print("Returning to menu.")
                break
        else:
            # lost or quit — offer retry or exit
            resp = input("Retry same level? (y)  or Quit (n): ").strip().lower()
            if resp == "y":
                continue
            else:
                break

    print("Thanks for playing. Final highscores:")
    print(pretty_highscores())

if __name__ == "__main__":
    main()
