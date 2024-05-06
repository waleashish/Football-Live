#!/bin/bash

# Run the installation services
docker compose up populate-tables --build

# Stop the installation services
docker compose down

# Build streamlit app
docker compose build streamlit-app