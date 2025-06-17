# region imports
from AlgorithmImports import *
# endregion

class MomentumStrategy(QCAlgorithm):

    def initialize(self):
        self.set_start_date(2009, 12, 23)
        self.set_cash(1000000)
        self.spy = self.add_equity("SPXL", Resolution.DAILY).symbol
        self.portfolio.MarginCallModel = MarginCallModel.Null
        self.UniverseSettings.Leverage = 8

        # Schedule recalibration at the start of each week
        self.schedule.on(self.date_rules.every_day(), self.time_rules.at(15, 58), self.rebalance)

        self.state = 0

        chart = Chart("My Custom Chart")
        self.add_chart(chart)
        chart.AddSeries(Series("SPY Close", SeriesType.LINE, '$'))
        chart.AddSeries(Series("Long_term_mean", SeriesType.LINE, '$'))
        chart.AddSeries(Series("Short_term_mean", SeriesType.LINE, '$'))
        chart.AddSeries(Series(name="Buy Signal", type=SeriesType.SCATTER, unit='$', color=Color.DarkGreen, symbol=ScatterMarkerSymbol.TRIANGLE))
        chart.AddSeries(Series("Sell Signal", SeriesType.SCATTER, '$', Color.DarkRed, ScatterMarkerSymbol.TRIANGLE_DOWN))
        chart.AddSeries(Series("Volatility Upper", SeriesType.Line, '$'))
        chart.AddSeries(Series("Volatility Lower", SeriesType.Line, '$'))

        self.volatility_period = 27  # Period for volatility calculation
        self.rolling_window = RollingWindow[float](self.volatility_period)


            
    def rebalance(self):
        history = self.history(self.spy, self.volatility_period+1, Resolution.DAILY)
        if history.empty or history.isnull().values.any():
            raise ValueError("Empty History")

        #self.Debug(history)
        
        self.data = history['close'].unstack(level=0)
        for i in range(len(self.data)):
            self.rolling_window.add(self.data.iloc[i])

        long_term_mean = float(self.data.mean().values) * float(self.data.std().values) * np.sqrt( 252 / len(self.data))
        short_term_mean = float(self.data[:5].mean().values) * float(self.data[:5].std().values) * np.sqrt( 252 / 5)

        self.Plot("My Custom Chart", "SPY Close", self.data.iloc[-1])
        self.Plot("My Custom Chart", "Long_term_mean", long_term_mean)
        self.Plot("My Custom Chart", "Short_term_mean", short_term_mean)

        if self.rolling_window.IsReady:
            returns = [self.rolling_window[i] / self.rolling_window[i+1] - 1 for i in range(self.volatility_period - 1)]
            volatility = np.std(returns)*500
            upper_bar = 100 + volatility / 2
            lower_bar = 100 - volatility / 2

            self.Plot("My Custom Chart", "Volatility Upper", upper_bar)
            self.Plot("My Custom Chart", "Volatility Lower", lower_bar)


        self.previous_state = self.state 

        if (float(self.data.std().values) * np.sqrt( 252 / len(self.data))) > 22.5:
            self.debug(f"HIGH VOL {(float(self.data.std().values) * np.sqrt( 252 / len(self.data)))}")
            self.liquidate()
            return

        if  short_term_mean < long_term_mean and self.state != 1:
            self.state = 1
        elif short_term_mean > long_term_mean and self.state != -1:
            self.state = -1

        if self.previous_state != self.state:
            self.trade()
        
    

    def trade(self):
        if self.state == 1:
            self.plot("My Custom Chart", "Buy Signal", self.data.iloc[-1])
            self.liquidate()
            self.set_holdings("SPXL", 1.9)

        if self.state == -1:
            self.plot("My Custom Chart", "Sell Signal", self.data.iloc[-1])
            self.liquidate()
            # self.set_holdings("SPXL", -1.9)

   
        