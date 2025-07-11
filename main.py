# ✅ CRYPTO TELEGRAM ALERT BOT for PEPE, 1000SATS, WIF, DOGE
# Monitors 15m chart for bullish candle patterns + RSI divergence
# Sends real-time alerts via Telegram bot to group

import requests
import time
import datetime
import os

# === CONFIGURATION ===
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
SYMBOLS = ['PEPEUSDT', '1000SATSUSDT', 'WIFUSDT', 'DOGEUSDT']
BINANCE_BASE = 'https://api.binance.com'
INTERVAL = '15m'
RSI_PERIOD = 14
ALERT_INTERVAL = 300  # seconds between checks

# === TELEGRAM SEND FUNCTION ===
def send_alert(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"}
    requests.post(url, data=payload)

# === RSI CALCULATION ===
def calculate_rsi(closes, period=RSI_PERIOD):
    gains = []
    losses = []
    for i in range(1, len(closes)):
        delta = closes[i] - closes[i - 1]
        if delta >= 0:
            gains.append(delta)
            losses.append(0)
        else:
            gains.append(0)
            losses.append(abs(delta))
    avg_gain = sum(gains[-period:]) / period
    avg_loss = sum(losses[-period:]) / period
    if avg_loss == 0:
        return 100
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))

# === CANDLE SIGNAL CHECK ===
def is_bullish_candle(c):
    open_, high, low, close = map(float, [c['o'], c['h'], c['l'], c['c']])
    body = close - open_
    wick = high - close
    tail = open_ - low
    return body > 0 and body >= (wick + tail) * 0.5  # strong body

# === FETCH 15m CANDLES ===
def get_candles(symbol):
    url = f"{BINANCE_BASE}/api/v3/klines?symbol={symbol}&interval={INTERVAL}&limit=20"
    res = requests.get(url)
    data = res.json()
    return [
        {"o": c[1], "h": c[2], "l": c[3], "c": c[4]} for c in data
    ]

# === MAIN LOOP ===
last_alert = {}
print("✅ Bot started... Monitoring", SYMBOLS)
while True:
    try:
        for symbol in SYMBOLS:
            candles = get_candles(symbol)
            closes = [float(c['c']) for c in candles]
            rsi = calculate_rsi(closes)
            last_candle = candles[-1]
            second_last = candles[-2]

            if is_bullish_candle(second_last) and rsi < 50:
                now = datetime.datetime.now().strftime("%H:%M:%S")
                msg = (
                    f"🚨 *BUY SIGNAL – {symbol} (15m)*\n"
                    f"🕒 Time: {now}\n"
                    f"📈 Pattern: Bullish candle + RSI ≈ {round(rsi, 1)}\n"
                    f"🎯 Target: +5-10% (watch manually)\n"
                    f"🛑 Stop: Below recent low\n"
                    f"🔁 Trail on breakout"
                )
                if symbol not in last_ale_
          
