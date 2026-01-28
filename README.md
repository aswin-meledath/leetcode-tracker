# LeetCode Tracker - Setup & Run Guide

## Prerequisites
- Python 3.7+ installed on your machine
- pip (Python package manager)

## Step 1: Install Dependencies

Open PowerShell/Command Prompt and navigate to your project folder:

```powershell
cd "c:\Users\LENOVO\OneDrive\Desktop\leetcode_tracker"
```

Install the required packages:

```powershell
pip install -r requirements.txt
```

## Step 2: Run the Application

Execute the Flask app:

```powershell
python app.py
```

You should see output like:
```
 * Running on http://127.0.0.1:5000
 * Debug mode: on
```

## Step 3: Open in Browser

Go to your web browser and visit:
```
http://localhost:5000
```

## Features Available

- **Dashboard** (/) - Overview of your progress
- **Problems** (/problems) - View all problems with filters
- **Daily Plans** (/daily-plans) - 30-day schedule view
- **Calendar** (/calendar) - Visual calendar of progress

## Database

The app uses SQLite. Database file: `leetcode_tracker.db`

### Reset Database (if needed)

To clear all data and reseed:
```powershell
python
```

Then in Python:
```python
from app import app, db, seed_data

with app.app_context():
    db.drop_all()
    db.create_all()
    seed_data()
```

## Stop the Server

Press `Ctrl + C` in the terminal to stop the Flask development server.

## Deployment Options

### Option 1: Local Network Access
Edit app.py line 236 from:
```python
app.run(debug=True)
```
to:
```python
app.run(host='0.0.0.0', debug=True)
```

Then access from other machines on your network using your machine's IP address.

### Option 2: Production Deployment (Heroku/PythonAnywhere)
1. Install gunicorn: `pip install gunicorn`
2. Create Procfile: `echo "web: gunicorn app:app" > Procfile`
3. Deploy to your preferred platform

### Option 3: Create Windows Batch File

Create a file `run.bat` in the project folder:

```batch
@echo off
cd /d "%~dp0"
python app.py
pause
```

Double-click `run.bat` to start the server anytime.

## Troubleshooting

**Port Already in Use:**
```powershell
python app.py --port 5001
```

**Module Not Found Error:**
Make sure you're in the correct directory and have installed requirements:
```powershell
pip install -r requirements.txt
```

**Database Locked:**
Delete `instance/leetcode_tracker.db` and restart the app.
