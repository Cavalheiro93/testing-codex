"""Application entry point.

This module exposes a minimal runner to start the Flask application
in development mode.
"""

from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
