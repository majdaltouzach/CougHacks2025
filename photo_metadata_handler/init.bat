@echo off

REM Backend setup
echo Setting up Python virtual environment...
cd backend
python -m venv venv
call venv\Scripts\activate
pip install -r requirements.txt

REM Start backend server
start cmd /k "uvicorn app.main:app --reload"
cd ..

REM Frontend setup
echo Installing frontend dependencies...
cd frontend
npm install

REM Start frontend server
start cmd /k "npm run dev"
