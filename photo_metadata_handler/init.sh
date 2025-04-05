#!/bin/bash

# Backend setup
echo "Setting up Python virtual environment..."
cd backend || exit
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Start backend server
echo "Starting backend server..."
uvicorn app.main:app --reload &
cd ..

# Frontend setup
echo "Installing frontend dependencies..."
cd frontend || exit
npm install

# Start frontend server
echo "Starting frontend development server..."
npm run dev
