#!/bin/bash

# Start Gunicorn processes
echo Starting Gunicorn.
cd src
exec gunicorn hs.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 3