# Backend setup
Write-Host "Setting up Python virtual environment..."
Set-Location -Path "./backend"
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt

# Start backend server
Start-Process powershell -ArgumentList 'uvicorn app.main:app --reload'
Set-Location ..

# Frontend setup
Write-Host "Installing frontend dependencies..."
Set-Location -Path "./frontend"
npm install

# Start frontend server
Start-Process powershell -ArgumentList 'npm run dev'
