#!/bin/bash

virtualenv venv
source venv/bin/activate

pip3 install -r requirements.txt

# Initialize database schemas
flask db init
flask db migrate -m "Initialize database"
flask db upgrade

# Start the application, config logfiles
gunicorn --workers=2 --bind 0.0.0.0:5000 --log-level=info --access-logfile=./logs/api.log --error-logfile=./logs/api.err.log --capture-output --enable-stdio-inheritance app:app