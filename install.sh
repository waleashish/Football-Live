#!/bin/bash

# Run the installation services
docker compose up populate-teams --build

# Stop the installation services
docker compose down

# Build streamlit app
docker compose up streamlit-app --build