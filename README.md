# FastAPI ChatBot API

## Project Structure

```
ChatBot/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── api/
│   │   ├── __init__.py
│   │   └── endpoints.py
│   ├── core/
│   │   ├── __init__.py
│   │   └── config.py
│   └── models/
│       ├── __init__.py
│       └── user.py
│
├── requirements.txt
├── README.md
└── venv/
```

- `app/`: Main application package
- `api/`: API route definitions
- `core/`: Core settings/configuration
- `models/`: Pydantic models
- `main.py`: Entry point (can be moved to `app/main.py`) 