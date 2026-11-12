"""Run the service locally: python -m app.main"""

import logging

from app import create_app

logging.basicConfig(level=logging.INFO)
app = create_app()

if __name__ == "__main__":
    app.run(port=5000, debug=True)
