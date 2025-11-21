import random
from typing import Dict, List, Tuple


Poem = Dict[str, List[str]]


POEMS: List[Poem] = [
    {
        "title": "Dawn Market",
        "lines": [
            "Lantern light trembles on fresh morning bread",
            "Vendors hum softly, chasing away the dark",
            "Coins clink like sparrows startled from the shed",
            "Steam curls in alleys, drawing daydreams to embark",
        ],
    },
    {
        "title": "Quiet Library",
        "lines": [
            "Dust motes drift like stars between the shelves",
            "Footsteps hush themselves to not disturb the thought",
            "Old maps remember continents that redefined themselves",
            "Ink waits for questions that the silence almost caught",
        ],
    },
    {
        "title": "Rainy Arcade",
        "lines": [
            "Neon reflections ripple in the puddled street",
            "Joystick battles echo over thunder's sigh",
            "Ticket ribbons pile beside forgotten seats",
            "Lightning applauds another pixelated try",
        ],
    },
    {
        "title": "Rooftop Garden",
        "lines": [
            "Tomatoes blush above the city roar",
            "Bees navigate a maze of mirrored glass",
            "A child plants wishes in a pot beside the door",
            "Clouds rest on railings while the subway currents pass",
        ],
    },
    {
        "title": "Night Train",
        "lines": [
            "Window frames repeat a moonlit reel",
            "Stations drift by wearing names of sleep",
            "Suitcases whisper secrets they conceal",
            "Coffee cups sway with promises to keep",
        ],
    },
    {
        "title": "Seaside Festival",
        "lines": [
            "Kites mimic gulls above the salted light",
            "Calliope tunes fold into the tide",
            "Fishers trade stories only told at night",
            "A ferris wheel reflects the harbor's pride",
        ],
    },
    {
        "title": "Snowy Courtyard",
        "lines": [
            "Footprints braid paths to the wooden gate",
            "Icicles tune wind chimes with frozen grace",
            "Children sculpt dragons learning how to wait",
            "Tea steam fogs the panes like gentle lace",
        ],
    },
    {
        "title": "Summer Workshop",
        "lines": [
            "Saw dust confetti glows in golden beams",
            "Blueprints unroll like stories yet to start",
            "A radio hums of far-off winning teams",
            "Fresh paint remembers every beating heart",
        ],
    },
]


def prompt_player_count() -> int:
    while True:
        raw = input("How many players? (2-5): ").strip()
        if not raw.isdigit():
            print("Please enter a number between 2 and 5.")
            continue
        count = int(raw)
        if 2 <= count <= 5:
            return count
        print("Player count must be between 2 and 5.")


def prompt_player_names(count: int) -> List[str]:
    names: List[str] = []
    for idx in range(1, count + 1):
        while True:
            name = input(f"Enter player {idx} name: ").strip()
            if not name:
                name = f"Player {idx}"
            if name not in names:
                names.append(name)
                break
            print("Names must be unique. Try again.")
    return names


def select_poems_for_players(count: int) -> List[Poem]:
    shuffled = random.sample(POEMS, k=len(POEMS))
    return shuffled[:count]


def prompt_line_ranking(player: str, poem_title: str, line: str, line_number: int) -> int:
    while True:
        raw = input(
            f"{player}, rate line {line_number} of '{poem_title}' (1-5): "
        ).strip()
        if not raw.isdigit():
            print("Please enter a number between 1 and 5.")
            continue
        value = int(raw)
        if 1 <= value <= 5:
            return value
        print("Ranking must be 1 through 5.")


def play_round(players: List[str], assigned_poems: List[Poem]) -> List[Tuple[str, Poem, List[int]]]:
    round_results: List[Tuple[str, Poem, List[int]]] = []
    for player, poem in zip(players, assigned_poems):
        print("\n" + "=" * 50)
        print(f"{player}, here is your random poem: {poem['title']}")
        print("-" * 50)
        for idx, line in enumerate(poem["lines"], start=1):
            print(f"{idx}. {line}")
        print("-" * 50)

        scores: List[int] = []
        for idx, line in enumerate(poem["lines"], start=1):
            score = prompt_line_ranking(player, poem["title"], line, idx)
            scores.append(score)
        round_results.append((player, poem, scores))
    return round_results


def summarize_results(results: List[Tuple[str, Poem, List[int]]]) -> None:
    print("\n" + "#" * 50)
    print("Ranking summary")
    print("#" * 50)
    for player, poem, scores in results:
        average = sum(scores) / len(scores)
        print(f"\n{player} rated '{poem['title']}' with an average of {average:.2f}:")
        for idx, (line, score) in enumerate(zip(poem["lines"], scores), start=1):
            print(f"  Line {idx}: {score} — {line}")
    overall_average = sum(sum(scores) for _, _, scores in results) / (
        len(results) * 4
    )
    print("\n" + "-" * 50)
    print(f"Group average across all lines: {overall_average:.2f}")
    print("-" * 50)


def main() -> None:
    print("Welcome to the Poem Rank Game!")
    player_count = prompt_player_count()
    players = prompt_player_names(player_count)
    assigned_poems = select_poems_for_players(player_count)
    results = play_round(players, assigned_poems)
    summarize_results(results)


if __name__ == "__main__":
    main()
