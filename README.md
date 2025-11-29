# Eileen's Classroom 🎨

A classroom management web application to help manage my daughter's classroom (4-year-olds).

## Features

- **Parent Accounts**: Registration and login for each parent in the class
- **Class Calendar**: View events, activities, and who is on snack duty
- **Snack Duty Schedule**: Track and manage snack duty assignments
- **Message Board**: Broadcast messages between parents

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/BNNJ/EileenClassRoom.git
   cd EileenClassRoom
   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the application:
   ```bash
   python run.py
   ```

5. Open your browser and navigate to `http://localhost:5000`

## Configuration

Set the following environment variables for production:

- `SECRET_KEY`: A secure random key for session management
- `DATABASE_URL`: Database connection string (defaults to SQLite)
- `FLASK_CONFIG`: Configuration mode (`development`, `production`, or `testing`)

## Running Tests

```bash
pip install pytest
pytest
```

## Project Structure

```
EileenClassRoom/
├── app/
│   ├── __init__.py          # Application factory
│   ├── models.py             # Database models
│   ├── forms.py              # WTForms definitions
│   ├── routes/               # Route blueprints
│   │   ├── auth.py           # Authentication routes
│   │   ├── main.py           # Main/dashboard routes
│   │   ├── calendar.py       # Calendar routes
│   │   └── messages.py       # Messaging routes
│   ├── templates/            # Jinja2 templates
│   └── static/               # CSS and static files
├── tests/                    # Test suite
├── config.py                 # Configuration classes
├── run.py                    # Application entry point
└── requirements.txt          # Python dependencies
```

## License

MIT License - see LICENSE file for details.
