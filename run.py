#!/usr/bin/env python3
"""Run the classroom management application."""
import os
from app import create_app

app = create_app(os.environ.get('FLASK_CONFIG') or 'default')

if __name__ == '__main__':
    debug_mode = os.environ.get('FLASK_DEBUG', 'false').lower() == 'true'
    app.run(host='0.0.0.0', port=5000, debug=debug_mode)
