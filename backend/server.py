import asyncio
import websockets
import json
import MetaTrader5 as mt5
import logging
import os
import platform
import subprocess
from datetime import datetime
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# MT5 Connection Details
MT5_LOGIN = 221490
MT5_PASSWORD = "Rg@12345"
MT5_SERVER = "Augmontspot"
SYMBOLS = ["XAUUSD", "XAGUSD"]

# WebSocket Configuration
WS_HOST = "0.0.0.0"
WS_PORT = 8001

# Initialize MT5
def find_mt5_path():
    """Try to find MT5 installation path using multiple methods"""
    if platform.system() != "Windows":
        return None
    
    # Method 1: Check common installation paths
    common_paths = [
        "C:\\Program Files\\MetaTrader 5\\terminal64.exe",
        "C:\\Program Files (x86)\\MetaTrader 5\\terminal64.exe",
        "D:\\Program Files\\MetaTrader 5\\terminal64.exe",
        "D:\\Program Files (x86)\\MetaTrader 5\\terminal64.exe",
        "E:\\Program Files\\MetaTrader 5\\terminal64.exe",
        "E:\\Program Files (x86)\\MetaTrader 5\\terminal64.exe",
    ]
    
    for path in common_paths:
        if os.path.exists(path):
            logger.info(f"Found MT5 at: {path}")
            return path
    
    # Method 2: Search in user AppData directory
    try:
        user_terminal_path = os.path.expanduser("~\\AppData\\Roaming\\MetaQuotes\\Terminal")
        if os.path.exists(user_terminal_path):
            for root, dirs, files in os.walk(user_terminal_path):
                if "terminal64.exe" in files:
                    found_path = os.path.join(root, "terminal64.exe")
                    logger.info(f"Found MT5 at: {found_path}")
                    return found_path
    except Exception as e:
        logger.debug(f"Error searching user directory: {e}")
    
    # Method 3: Search using Windows where command
    try:
        result = subprocess.run(
            ["where", "terminal64.exe"],
            capture_output=True,
            text=True,
            timeout=10,
            shell=True
        )
        if result.returncode == 0 and result.stdout.strip():
            found_path = result.stdout.strip().split('\n')[0]
            if os.path.exists(found_path):
                logger.info(f"Found MT5 using 'where' command: {found_path}")
                return found_path
    except Exception as e:
        logger.debug(f"Error using 'where' command: {e}")
    
    # Method 4: Search in all Program Files directories
    try:
        for drive in ['C:', 'D:', 'E:']:
            program_files_paths = [
                f"{drive}\\Program Files\\MetaTrader 5",
                f"{drive}\\Program Files (x86)\\MetaTrader 5",
            ]
            for base_path in program_files_paths:
                if os.path.exists(base_path):
                    mt5_exe = os.path.join(base_path, "terminal64.exe")
                    if os.path.exists(mt5_exe):
                        logger.info(f"Found MT5 at: {mt5_exe}")
                        return mt5_exe
    except Exception as e:
        logger.debug(f"Error searching Program Files: {e}")
    
    return None

def check_mt5_running():
    """Check if MT5 process is running"""
    try:
        if platform.system() == "Windows":
            result = subprocess.run(
                ["tasklist", "/FI", "IMAGENAME eq terminal64.exe"],
                capture_output=True,
                text=True,
                timeout=5
            )
            return "terminal64.exe" in result.stdout
    except Exception as e:
        logger.debug(f"Error checking MT5 process: {e}")
    return False

def initialize_mt5():
    """Initialize and login to MT5"""
    logger.info("Attempting to initialize MetaTrader5...")
    
    # First, try to find MT5 installation
    mt5_path = find_mt5_path()
    
    if not mt5_path:
        logger.error("=" * 60)
        logger.error("METATRADER5 INSTALLATION NOT FOUND!")
        logger.error("=" * 60)
        show_troubleshooting()
        return False
    
    # Check if MT5 is running
    if not check_mt5_running():
        logger.warning("=" * 60)
        logger.warning("MetaTrader5 Terminal does not appear to be running.")
        logger.warning("Please start MetaTrader5 Terminal before running this server.")
        logger.warning("=" * 60)
        logger.info(f"MT5 installation found at: {mt5_path}")
        logger.info("Please:")
        logger.info("1. Start MetaTrader5 Terminal (double-click the MT5 icon)")
        logger.info("2. Log in with your account credentials")
        logger.info("3. Then run this server again")
        return False
    
    # Try to initialize with found path
    logger.info(f"Attempting to initialize with path: {mt5_path}")
    if not mt5.initialize(path=mt5_path):
        error = mt5.last_error()
        logger.error(f"MT5 initialization failed with explicit path: {error}")
        # Try without path as fallback
        logger.info("Trying default initialization...")
        if not mt5.initialize():
            error = mt5.last_error()
            logger.error(f"MT5 initialization failed: {error}")
            show_troubleshooting()
            return False
        else:
            logger.info("MT5 initialized successfully with default method")
    else:
        logger.info("MT5 initialized successfully with explicit path")
    
    # Login to MT5
    authorized = mt5.login(MT5_LOGIN, password=MT5_PASSWORD, server=MT5_SERVER)
    if not authorized:
        logger.error(f"MT5 login failed: {mt5.last_error()}")
        mt5.shutdown()
        return False
    
    logger.info(f"MT5 login successful - Account: {MT5_LOGIN}, Server: {MT5_SERVER}")
    
    # Verify symbols are available
    for symbol in SYMBOLS:
        symbol_info = mt5.symbol_info(symbol)
        if symbol_info is None:
            logger.warning(f"Symbol {symbol} not found in market watch")
        else:
            logger.info(f"Symbol {symbol} is available")
    
    return True

def show_troubleshooting():
    """Display troubleshooting information"""
    logger.error("=" * 60)
    logger.error("TROUBLESHOOTING STEPS:")
    logger.error("1. Make sure MetaTrader5 Terminal is INSTALLED on your system")
    logger.error("2. Make sure MetaTrader5 Terminal is RUNNING (open the MT5 application)")
    logger.error("3. Make sure you are logged into MT5 Terminal with your account")
    logger.error("4. Try specifying the MT5 path manually if installed in non-default location")
    logger.error("=" * 60)
    
    if platform.system() == "Windows":
        common_paths = [
            "C:\\Program Files\\MetaTrader 5\\terminal64.exe",
            "C:\\Program Files (x86)\\MetaTrader 5\\terminal64.exe",
        ]
        logger.info("Common MT5 installation paths on Windows:")
        mt5_found = False
        for path in common_paths:
            exists = "✓ EXISTS" if os.path.exists(path) else "✗ NOT FOUND"
            logger.info(f"  - {path} [{exists}]")
            if os.path.exists(path):
                mt5_found = True
        
        if not mt5_found:
            logger.error("=" * 60)
            logger.error("METATRADER5 NOT FOUND!")
            logger.error("=" * 60)
            logger.info("To install MetaTrader5:")
            logger.info("1. Download from: https://www.metatrader5.com/en/download")
            logger.info("2. Or visit: https://download.mql5.com/cdn/web/metaquotes.software.corp/mt5/mt5setup.exe")
            logger.info("3. Run the installer and follow the setup wizard")
            logger.info("4. After installation, start MetaTrader5 Terminal")
            logger.info("5. Log in with your trading account credentials")
            logger.info("6. Then run this server again")
            logger.error("=" * 60)
        else:
            logger.info("If MT5 is installed elsewhere, you can specify the path in initialize()")

def get_price_data():
    """Get current price data for all symbols"""
    data = {}
    timestamp = datetime.now().isoformat()
    
    for symbol in SYMBOLS:
        try:
            tick = mt5.symbol_info_tick(symbol)
            if tick is None:
                logger.warning(f"Failed to get tick for {symbol}")
                data[symbol] = {
                    "bid": None,
                    "ask": None,
                    "last": None,
                    "volume": None,
                    "time": timestamp,
                    "error": "No data available"
                }
            else:
                data[symbol] = {
                    "bid": tick.bid,
                    "ask": tick.ask,
                    "last": tick.last,
                    "volume": tick.volume,
                    "time": timestamp,
                    "spread": round(tick.ask - tick.bid, 5) if tick.ask and tick.bid else None
                }
        except Exception as e:
            logger.error(f"Error getting price for {symbol}: {str(e)}")
            data[symbol] = {
                "bid": None,
                "ask": None,
                "error": str(e),
                "time": timestamp
            }
    
    return data

async def price_stream(websocket, path):
    """Handle WebSocket connection and stream price data"""
    client_address = websocket.remote_address
    logger.info(f"New WebSocket connection from {client_address}")
    
    try:
        while True:
            price_data = get_price_data()
            await websocket.send(json.dumps(price_data))
            await asyncio.sleep(0.5)  # Send updates every 500ms
    except websockets.exceptions.ConnectionClosed:
        logger.info(f"WebSocket connection closed: {client_address}")
    except Exception as e:
        logger.error(f"Error in price_stream: {str(e)}")
    finally:
        logger.info(f"Client disconnected: {client_address}")

async def main():
    """Main function to start the WebSocket server"""
    logger.info("=" * 60)
    logger.info("MetaTrader5 WebSocket Server Starting...")
    logger.info("=" * 60)
    
    # Initialize MT5
    if not initialize_mt5():
        logger.error("=" * 60)
        logger.error("CRITICAL: Failed to initialize MT5. Server cannot start.")
        logger.error("Please ensure MetaTrader5 Terminal is running and try again.")
        logger.error("=" * 60)
        return
    
    # Start WebSocket server
    logger.info(f"Starting WebSocket server on ws://{WS_HOST}:{WS_PORT}")
    async with websockets.serve(price_stream, WS_HOST, WS_PORT):
        logger.info("WebSocket server is running. Press Ctrl+C to stop.")
        await asyncio.Future()  # Run forever

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Shutting down...")
    finally:
        mt5.shutdown()
        logger.info("MT5 connection closed")

