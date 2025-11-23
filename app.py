import random
from dataclasses import dataclass
from typing import Dict, List, Tuple

from flask import Flask, redirect, render_template, request, url_for


app = Flask(__name__)


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


@dataclass
class PlayerAssignment:
    name: str
    poem_title: str
    poem_lines: List[str]
    existing_scores: List[int] | None = None


PlayerResults = Tuple[str, str, List[str], List[int]]


def normalize_names(raw_names: List[str], count: int) -> List[str]:
    names: List[str] = []
    for idx in range(count):
        candidate = raw_names[idx].strip() or f"Player {idx + 1}"
        if candidate in names:
            raise ValueError("Names must be unique")
        names.append(candidate)
    return names


def assign_poems(count: int) -> List[Poem]:
    shuffled = random.sample(POEMS, k=len(POEMS))
    return shuffled[:count]


def parse_player_count(raw_value: str) -> int:
    if not raw_value.isdigit():
        raise ValueError("Player count must be a number between 2 and 5")
    count = int(raw_value)
    if not 2 <= count <= 5:
        raise ValueError("Player count must be between 2 and 5")
    return count


def build_assignments_from_form(form: dict) -> List[PlayerAssignment]:
    try:
        count = int(form.get("player_count", 0))
    except ValueError:
        count = 0
    assignments: List[PlayerAssignment] = []
    for idx in range(count):
        name = form.get(f"player_{idx}_name", "").strip() or f"Player {idx + 1}"
        poem_title = form.get(f"player_{idx}_title", "Unknown Poem")
        poem_lines = [
            form.get(f"player_{idx}_line_{line_idx}", "")
            for line_idx in range(4)
        ]
        scores: List[int] = []
        for line_idx in range(4):
            raw_score = form.get(f"player_{idx}_score_{line_idx}", "0")
            try:
                score = int(raw_score)
            except ValueError:
                score = 0
            scores.append(score)
        assignments.append(
            PlayerAssignment(
                name=name,
                poem_title=poem_title,
                poem_lines=poem_lines,
                existing_scores=scores,
            )
        )
    return assignments


def validate_scores(scores: List[int]) -> bool:
    return all(1 <= value <= 5 for value in scores)


def calculate_results(assignments: List[PlayerAssignment]) -> List[PlayerResults]:
    results: List[PlayerResults] = []
    for assignment in assignments:
        if assignment.existing_scores is None:
            raise ValueError("Missing scores for player")
        results.append(
            (
                assignment.name,
                assignment.poem_title,
                assignment.poem_lines,
                assignment.existing_scores,
            )
        )
    return results


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html", error_message=None)


@app.route("/rate", methods=["POST"])
def rate():
    raw_count = request.form.get("player_count", "")
    raw_names = [request.form.get(f"player_{idx}_name", "") for idx in range(1, 6)]

    try:
        player_count = parse_player_count(raw_count)
        names = normalize_names(raw_names, player_count)
    except ValueError as exc:
        return render_template(
            "index.html",
            error_message=str(exc),
            previous_count=raw_count,
            previous_names=raw_names,
        )

    assigned_poems = assign_poems(player_count)
    assignments = [
        PlayerAssignment(
            name=name,
            poem_title=poem["title"],
            poem_lines=poem["lines"],
        )
        for name, poem in zip(names, assigned_poems)
    ]

    return render_template("rate.html", assignments=assignments, player_count=player_count)


@app.route("/results", methods=["POST"])
def results():
    assignments = build_assignments_from_form(request.form)

    for assignment in assignments:
        if assignment.existing_scores is None:
            return redirect(url_for("index"))
        if not validate_scores(assignment.existing_scores):
            error = "All scores must be whole numbers between 1 and 5."
            return render_template(
                "rate.html",
                assignments=assignments,
                player_count=len(assignments),
                error_message=error,
            )

    results_data = calculate_results(assignments)
    per_player = []
    total_scores = 0
    total_lines = 0

    for name, title, lines, scores in results_data:
        average = sum(scores) / len(scores)
        total_scores += sum(scores)
        total_lines += len(scores)
        per_player.append({
            "name": name,
            "title": title,
            "lines": list(zip(lines, scores)),
            "average": average,
        })

    group_average = total_scores / total_lines if total_lines else 0

    return render_template(
        "results.html",
        per_player=per_player,
        group_average=group_average,
    )


if __name__ == "__main__":
    app.run(debug=True)
