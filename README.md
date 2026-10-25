# Recurrence Relation Solver — Working Model

A small Flask web application with an HTML/CSS/JavaScript interface connected to a Python recurrence solver.

## Requirements
- Python 3.9 or newer
- Internet is not required after Python and Flask are installed

## Run on Windows (VS Code / Command Prompt)

1. Extract `recurrence_relation_solver.zip`.
2. Open the extracted `recurrence_relation_solver` folder in VS Code.
3. Open the VS Code terminal (`Terminal` → `New Terminal`).
4. Create a virtual environment (recommended):

   ```bat
   py -m venv .venv
   .venv\Scripts\activate
   ```

5. Install Flask:

   ```bat
   py -m pip install -r requirements.txt
   ```

6. Start the web app:

   ```bat
   py app.py
   ```

7. Open the local address printed in the terminal, usually **http://127.0.0.1:5000**.

Keep the terminal open while using the app. Press `Ctrl+C` in the terminal to stop it.

## Run on macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
python3 app.py
```

Then open http://127.0.0.1:5000.

## Supported examples
- `T(n)=2T(n/2)+n` → `O(n log n)`
- `T(n)=T(n/2)+log(n)` → `O(log^2 n)`
- `T(n)=4T(n/2)+n^2` → `O(n^2 log n)`
- `T(n)=T(n-1)+n` → `O(n^2)`
- `T(n)=T(n-1)+n^2` → `O(n^3)`
- `T(n)=T(n-1)+2^n` → `O(2^n)`
- `T(n)=T(n-1)+T(n-2)+1` → `O(φ^n)`

## Important scope note
This is a working educational prototype for common recurrence patterns, not a general symbolic solver. It intentionally rejects unsupported forms instead of guessing. Big-O results depend on standard assumptions for the listed recurrence families. For a college presentation, describe it as a **pattern-based recurrence relation solver using the Master Theorem and summation for supported forms**.
