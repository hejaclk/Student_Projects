# Adding New Games

Whenever you add a new game to this repository, follow this structure.

## Directory and file

- **One directory per game**, named clearly (e.g. `Game_1`, `Game_2`, or `Game_<name>`).
- Put **all code for that game** inside that directory.
- Use a **descriptive Python filename** (e.g. `fast_clicker.py`, `snake.py`).

## What to document

In the game folder, add a short **README.md** that includes:

| Item | Example |
|------|--------|
| **Game name** | Fast Clicker |
| **Short description** | One line: what the game does. |
| **How to run** | `python fast_clicker.py` (or the actual script name). |
| **Requirements** | e.g. `pygame` (and how to install: `pip install pygame`). |
| **Source** (optional) | e.g. "From ENG M6L5 – Part 3" if it came from a lesson/doc. |

Keep it concise: a few lines are enough.

## Example layout

```
Student_Projects/
├── README.md              ← Main repo description
├── ADDING_GAMES.md        ← This file
├── Game_1/
│   ├── README.md          ← Describes this game only
│   └── fast_clicker.py
└── Game_2/
    ├── README.md
    └── ...
```

## Checklist for a new game

1. Create a new folder (e.g. `Game_2`).
2. Add the game’s Python file(s) inside it.
3. Add a `README.md` in that folder with name, description, how to run, and requirements.
