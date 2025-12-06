# MetaTrader5 Installation Guide

## Quick Installation Steps

### Option 1: Direct Download (Recommended)

1. **Download MetaTrader5:**
   - Visit: https://www.metatrader5.com/en/download
   - Or direct download: https://download.mql5.com/cdn/web/metaquotes.software.corp/mt5/mt5setup.exe

2. **Run the Installer:**
   - Double-click `mt5setup.exe`
   - Follow the installation wizard
   - Choose installation location (default is usually fine)

3. **Launch MetaTrader5:**
   - After installation, MetaTrader5 Terminal will launch automatically
   - If not, find it in Start Menu → MetaTrader 5

4. **Login to Your Account:**
   - Enter your login credentials
   - Server: Your broker's server name (e.g., "Augmontspot")
   - Click "Login"

5. **Verify Installation:**
   - The terminal should open and show market data
   - You should see your account balance and trading interface

### Option 2: Install from MetaTrader5 Website

1. Go to https://www.metatrader5.com/en/download
2. Click "Download MetaTrader 5"
3. Run the downloaded installer
4. Follow the setup wizard

## Default Installation Locations

After installation, MetaTrader5 is typically located at:

- **64-bit Windows:**
  - `C:\Program Files\MetaTrader 5\terminal64.exe`
  
- **32-bit Windows:**
  - `C:\Program Files (x86)\MetaTrader 5\terminal64.exe`

## Verification

To verify MT5 is installed correctly:

1. **Check if file exists:**
   ```bash
   # Windows Command Prompt
   dir "C:\Program Files\MetaTrader 5\terminal64.exe"
   ```

2. **Check if process is running:**
   ```bash
   # Windows Command Prompt
   tasklist | findstr terminal64.exe
   ```

3. **Run the server:**
   ```bash
   cd MetaTrader5/MetaTraderAPI/backend
   python server.py
   ```

## Troubleshooting

### MT5 Not Found Error

If you get "MT5 not found" error:

1. **Verify Installation:**
   - Check if `terminal64.exe` exists in Program Files
   - If not, reinstall MetaTrader5

2. **Check Installation Path:**
   - The server will automatically search common locations
   - If installed in a custom location, you may need to specify the path

3. **Manual Path Specification:**
   - Edit `server.py` and modify the `find_mt5_path()` function
   - Add your custom installation path to the `common_paths` list

### MT5 Not Running Error

If you get "MT5 not running" error:

1. **Start MetaTrader5:**
   - Open Start Menu
   - Search for "MetaTrader 5"
   - Click to launch

2. **Login:**
   - Enter your account credentials
   - Make sure you're logged in successfully

3. **Verify Process:**
   - Open Task Manager (Ctrl+Shift+Esc)
   - Look for `terminal64.exe` in the Processes tab

### Login Failed Error

If login fails:

1. **Check Credentials:**
   - Verify login number, password, and server name in `server.py`
   - Make sure they match your MT5 account

2. **Test in MT5 Terminal:**
   - Try logging in manually through MT5 Terminal first
   - If that fails, check with your broker

3. **Server Name:**
   - Server name is case-sensitive
   - Make sure it matches exactly (e.g., "Augmontspot")

## System Requirements

- **Operating System:** Windows 7/8/10/11 (64-bit recommended)
- **RAM:** Minimum 1GB (2GB+ recommended)
- **Disk Space:** ~100MB for installation
- **Internet:** Required for trading and data updates

## Additional Resources

- **MetaTrader5 Official Site:** https://www.metatrader5.com/
- **Documentation:** https://www.metatrader5.com/en/automated-trading/mql5
- **Support:** Contact your broker for account-related issues

## Next Steps

After successful installation:

1. ✅ MT5 Terminal is installed
2. ✅ MT5 Terminal is running
3. ✅ You're logged into your account
4. ✅ Run `python server.py` in the backend directory
5. ✅ Start the frontend with `npm start` in the frontend directory

