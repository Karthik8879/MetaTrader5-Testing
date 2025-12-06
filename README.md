# MetaTrader5 Live Price Streaming

A real-time price streaming application for Gold (XAUUSD) and Silver (XAGUSD) using MetaTrader5 API with WebSocket backend and React frontend.

## Project Structure

```
MetaTraderAPI/
├── backend/          # Python WebSocket server
│   ├── server.py     # Main server file
│   └── requirements.txt
└── frontend/         # React application
    ├── src/
    ├── public/
    └── package.json
```

## Prerequisites

1. **MetaTrader5 Terminal** - Must be installed and running
2. **Python 3.7+** - For backend server
3. **Node.js 14+** - For React frontend
4. **MetaTrader5 Python Package** - Will be installed via requirements.txt

## Setup Instructions

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd MetaTrader5/MetaTraderAPI/backend
   ```

2. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   ```

3. Activate the virtual environment:
   - **Windows:**
     ```bash
     venv\Scripts\activate
     ```
   - **Linux/Mac:**
     ```bash
     source venv/bin/activate
     ```

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Make sure MetaTrader5 terminal is running and logged in with your account.

6. Start the backend server:
   ```bash
   python server.py
   ```

   You should see:
   ```
   MT5 initialized successfully
   MT5 login successful - Account: 221490, Server: Augmontspot
   Starting WebSocket server on ws://0.0.0.0:8001
   WebSocket server is running. Press Ctrl+C to stop.
   ```

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd MetaTrader5/MetaTraderAPI/frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the React development server:
   ```bash
   npm start
   ```

   The app will open automatically at `http://localhost:3000`

## Usage

1. **Start MetaTrader5 Terminal** - Ensure it's running and logged in
2. **Start Backend Server** - Run `python server.py` in the backend directory
3. **Start Frontend** - Run `npm start` in the frontend directory
4. **View Live Prices** - Open your browser to `http://localhost:3000`

The application will display:
- **Gold (XAUUSD)**: Bid, Ask, and Spread prices
- **Silver (XAGUSD)**: Bid, Ask, and Spread prices
- **Connection Status**: Real-time WebSocket connection indicator
- **Last Update Time**: Timestamp of the last price update

Prices update every 500ms (0.5 seconds) automatically.

## Configuration

### Backend Configuration

Edit `server.py` to modify:
- **Symbols**: Change the `SYMBOLS` list to add/remove trading pairs
- **Update Frequency**: Modify `await asyncio.sleep(0.5)` to change update interval
- **WebSocket Port**: Change `WS_PORT` (default: 8001)

### Frontend Configuration

Edit `src/App.js` to modify:
- **WebSocket URL**: Change `WS_URL` if backend runs on different host/port
- **UI Styling**: Modify `src/App.css` for custom styling

## Troubleshooting

### Backend Issues

1. **MT5 Initialization Failed**
   - Ensure MetaTrader5 terminal is installed and running
   - Check if MT5 is properly installed in your system

2. **Login Failed**
   - Verify your login credentials in `server.py`
   - Ensure you're logged into MetaTrader5 terminal
   - Check if the server name is correct

3. **Symbol Not Found**
   - Make sure XAUUSD and XAGUSD are available in your MT5 market watch
   - Add symbols to market watch if not visible

4. **WebSocket Connection Error**
   - Check if port 8001 is available
   - Ensure firewall allows connections on port 8001

### Frontend Issues

1. **Cannot Connect to WebSocket**
   - Verify backend server is running
   - Check if WebSocket URL in `App.js` matches backend configuration
   - Ensure CORS is not blocking the connection

2. **No Price Updates**
   - Check browser console for errors
   - Verify WebSocket connection status indicator
   - Ensure backend is receiving data from MT5

## Features

- ✅ Real-time price streaming via WebSocket
- ✅ Automatic reconnection on disconnect
- ✅ Beautiful, modern UI with gradient cards
- ✅ Connection status indicator
- ✅ Responsive design for mobile and desktop
- ✅ Error handling and logging
- ✅ Support for multiple symbols

## License

This project is for personal/educational use.

