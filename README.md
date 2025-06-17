# 📊 Momentum Strategy Using SPXL with Volatility Filter

[![Python](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/)
[![QuantConnect](https://img.shields.io/badge/platform-QuantConnect-black)](https://www.quantconnect.com/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

This project implements a simple momentum-based trading strategy on **SPXL**, a 3x leveraged ETF tracking the S&P 500. The strategy uses short- and long-term momentum indicators combined with a volatility filter to time entries and exits.

---

## 📌 Strategy Overview

- **Instrument**: `SPXL` (3x leveraged S&P 500 ETF)
- **Capital**: $1,000,000
- **Backtest Start**: Dec 23, 2009
- **Resolution**: Daily
- **Leverage**: 8x
- **Execution Platform**: QuantConnect Lean Framework

---

## ⚙️ How It Works

### 🧠 Core Logic

1. **Daily Rebalancing**
   - Rebalances near market close each day at 15:58.

2. **Momentum Signal**
   - Compares short-term (5-day) and long-term (27-day) rolling volatility-adjusted mean returns.
   - Enters a long position if the short-term mean is below the long-term mean.
   - Exits when the signal reverses.

3. **Volatility Filter**
   - If rolling volatility exceeds a dynamic threshold (22.5%), the strategy **exits all positions** and waits for calmer conditions.

4. **Charting**
   - Custom plots display price, signals, and volatility bands.

---

## 🧮 Indicators Used

- **Volatility-Adjusted Means**:
  $$ \mu = \bar{r} \cdot \sigma \cdot \sqrt{252 / N} $$

- **Volatility Bands**:  
  Uses rolling window of 27 days to compute:
  - Standard deviation of daily returns × 500
  - Adds/subtracts this value from a base level (100) for plotting

---

## 📁 Repository Structure

```
.
├── MomentumStrategy.py     # Core trading algorithm (Lean-compatible)
├── README.md               # Project documentation
├── LICENSE                 # MIT license
```

---

## 🚀 Getting Started

### Run in QuantConnect Cloud

1. Copy `MomentumStrategy.py` into a new QuantConnect project.
2. Run backtest and observe results + charts.

### Run Locally with Lean CLI

```bash
pip install lean
lean create "MomentumStrategy"
# Replace generated file with contents of MomentumStrategy.py
lean backtest "MomentumStrategy"
```

---

## 📈 Example Chart Output

- SPY Close price
- Long/Short term volatility-adjusted means
- Buy/Sell markers
- Volatility bounds

---

## 🧠 Potential Improvements

- Add **shorting logic** when signal reverses
- Test on other leveraged/non-leveraged ETFs
- Incorporate **regime detection** for risk-on/risk-off
- Add transaction cost modeling

---

## 🧑‍💻 Author

Built with 💡 by [Your Name]. Contributions welcome!

---

## 📜 License

This project is licensed under the [MIT License](LICENSE).
