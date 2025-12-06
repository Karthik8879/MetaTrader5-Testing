import React, { useState, useEffect, useRef } from 'react';
import './App.css';

const WS_URL = 'ws://localhost:8001';

function App() {
  const [prices, setPrices] = useState({
    XAUUSD: { bid: null, ask: null, spread: null, time: null },
    XAGUSD: { bid: null, ask: null, spread: null, time: null }
  });
  const [connectionStatus, setConnectionStatus] = useState('Disconnected');
  const [lastUpdate, setLastUpdate] = useState(null);
  const wsRef = useRef(null);
  const reconnectTimeoutRef = useRef(null);

  useEffect(() => {
    connectWebSocket();

    return () => {
      if (wsRef.current) {
        wsRef.current.close();
      }
      if (reconnectTimeoutRef.current) {
        clearTimeout(reconnectTimeoutRef.current);
      }
    };
  }, []);

  const connectWebSocket = () => {
    try {
      setConnectionStatus('Connecting...');
      const ws = new WebSocket(WS_URL);

      ws.onopen = () => {
        console.log('WebSocket connected');
        setConnectionStatus('Connected');
        if (reconnectTimeoutRef.current) {
          clearTimeout(reconnectTimeoutRef.current);
        }
      };

      ws.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);
          setPrices(data);
          setLastUpdate(new Date().toLocaleTimeString());
        } catch (error) {
          console.error('Error parsing WebSocket message:', error);
        }
      };

      ws.onerror = (error) => {
        console.error('WebSocket error:', error);
        setConnectionStatus('Error');
      };

      ws.onclose = () => {
        console.log('WebSocket disconnected');
        setConnectionStatus('Disconnected');
        // Attempt to reconnect after 3 seconds
        reconnectTimeoutRef.current = setTimeout(() => {
          connectWebSocket();
        }, 3000);
      };

      wsRef.current = ws;
    } catch (error) {
      console.error('Error connecting to WebSocket:', error);
      setConnectionStatus('Error');
      // Attempt to reconnect after 3 seconds
      reconnectTimeoutRef.current = setTimeout(() => {
        connectWebSocket();
      }, 3000);
    }
  };

  const formatPrice = (price) => {
    if (price === null || price === undefined) return 'N/A';
    return price.toFixed(2);
  };

  const formatSpread = (spread) => {
    if (spread === null || spread === undefined) return 'N/A';
    return spread.toFixed(3);
  };

  const getPriceColor = (symbol) => {
    const price = prices[symbol];
    if (!price || price.bid === null) return '#666';
    return '#fff';
  };

  return (
    <div className="App">
      <div className="container">
        <header className="header">
          <h1>MetaTrader5 Live Prices</h1>
          <div className="status-container">
            <div className={`status-indicator ${connectionStatus.toLowerCase()}`}>
              <span className="status-dot"></span>
              <span className="status-text">{connectionStatus}</span>
            </div>
            {lastUpdate && (
              <div className="last-update">
                Last Update: {lastUpdate}
              </div>
            )}
          </div>
        </header>

        <div className="prices-grid">
          {/* Gold (XAUUSD) */}
          <div className="price-card gold">
            <div className="card-header">
              <h2>Gold</h2>
              <span className="symbol">XAUUSD</span>
            </div>
            <div className="price-content">
              <div className="price-row">
                <span className="price-label">Bid:</span>
                <span className="price-value" style={{ color: getPriceColor('XAUUSD') }}>
                  {formatPrice(prices.XAUUSD?.bid)}
                </span>
              </div>
              <div className="price-row">
                <span className="price-label">Ask:</span>
                <span className="price-value" style={{ color: getPriceColor('XAUUSD') }}>
                  {formatPrice(prices.XAUUSD?.ask)}
                </span>
              </div>
              <div className="price-row">
                <span className="price-label">Spread:</span>
                <span className="price-value" style={{ color: getPriceColor('XAUUSD') }}>
                  {formatSpread(prices.XAUUSD?.spread)}
                </span>
              </div>
            </div>
          </div>

          {/* Silver (XAGUSD) */}
          <div className="price-card silver">
            <div className="card-header">
              <h2>Silver</h2>
              <span className="symbol">XAGUSD</span>
            </div>
            <div className="price-content">
              <div className="price-row">
                <span className="price-label">Bid:</span>
                <span className="price-value" style={{ color: getPriceColor('XAGUSD') }}>
                  {formatPrice(prices.XAGUSD?.bid)}
                </span>
              </div>
              <div className="price-row">
                <span className="price-label">Ask:</span>
                <span className="price-value" style={{ color: getPriceColor('XAGUSD') }}>
                  {formatPrice(prices.XAGUSD?.ask)}
                </span>
              </div>
              <div className="price-row">
                <span className="price-label">Spread:</span>
                <span className="price-value" style={{ color: getPriceColor('XAGUSD') }}>
                  {formatSpread(prices.XAGUSD?.spread)}
                </span>
              </div>
            </div>
          </div>
        </div>

        <footer className="footer">
          <p>Real-time price updates every 500ms</p>
        </footer>
      </div>
    </div>
  );
}

export default App;

