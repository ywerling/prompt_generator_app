# Comprehensive AI Image Prompt Generator

A Flask application with prompt, landscape, character, and Adobe Stock description tools.

## Structure

- `app.py`: development entry point
- `prompt_app/routes/`: Flask blueprints and request handling
- `prompt_app/services/`: reusable prompt-building and scraping logic
- `prompt_app/db.py`: SQLite connection lifecycle and prompt persistence
- `templates/components/`: shared Jinja UI components
- `tests/`: route and service tests

## Run

```powershell
python -m pip install -r requirements.txt
$env:SECRET_KEY = "replace-with-a-random-secret"
python app.py
```

## Test

```powershell
python -m unittest discover -s tests
```
