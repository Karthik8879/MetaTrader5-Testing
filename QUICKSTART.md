# Quick Start Guide

## Step-by-Step Setup

### 1. Prerequisites Check
- ✅ MetaTrader5 Terminal installed and running
- ✅ Python 3.7+ installed
- ✅ Node.js 14+ installed

### 2. Backend Setup (First Time Only)

```bash
cd MetaTrader5/MetaTraderAPI/backend

# Create virtual environment (optional but recommended)
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Frontend Setup (First Time Only)

```bash
cd MetaTrader5/MetaTraderAPI/frontend

# Install dependencies
npm install
```

### 4. Running the Application

**IMPORTANT:** Make sure MetaTrader5 Terminal is running and you're logged in!

#### Option A: Using Scripts (Windows)

1. **Start Backend:**
   - Double-click `backend/start-server.bat`
   - Or run: `cd backend && start-server.bat`

2. **Start Frontend:**
   - Double-click `frontend/start-frontend.bat`
   - Or run: `cd frontend && start-frontend.bat`

#### Option B: Using Command Line

1. **Terminal 1 - Start Backend:**
   ```bash
   cd MetaTrader5/MetaTraderAPI/backend
   python server.py
   ```

2. **Terminal 2 - Start Frontend:**
   ```bash
   cd MetaTrader5/MetaTraderAPI/frontend
   npm start
   ```

### 5. Access the Application

- Open your browser to: `http://localhost:3000`
- You should see live prices for Gold and Silver updating every 500ms

## Troubleshooting

### Backend won't start
- Check if MetaTrader5 is running
- Verify login credentials in `server.py`
- Make sure port 8001 is not in use

### Frontend shows "Disconnected"
- Ensure backend is running
- Check browser console for errors
- Verify WebSocket URL matches backend port

### No prices showing
- Check if XAUUSD and XAGUSD are in MT5 market watch
- Verify MT5 connection in backend logs
- Check backend terminal for error messages

## Default Configuration

- **Backend Port:** 8001
- **Frontend Port:** 3000
- **Update Frequency:** 500ms (0.5 seconds)
- **Symbols:** XAUUSD (Gold), XAGUSD (Silver)
- **MT5 Account:** 221490
- **MT5 Server:** Augmontspot

## Need Help?

Check the main `README.md` for detailed documentation and troubleshooting tips.

