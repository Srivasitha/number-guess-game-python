# game/utils.py
def get_int_input(prompt: str, default: int = None):
    while True:
        raw = input(prompt).strip()
        if raw == "" and default is not None:
            return default
        try:
            return int(raw)
        except ValueError:
            print("Please enter a valid integer.")
