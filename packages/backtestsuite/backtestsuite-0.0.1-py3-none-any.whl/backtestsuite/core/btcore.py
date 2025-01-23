# coding=utf-8
import backtrader as bt

import pandas as pd


class SignalPandasOHLCData(bt.feeds.PandasData):
    lines = ('Signal',)
    params = (('Signal', -1),

              )

    datafields = bt.feeds.PandasData.datafields + ['Signal']


class SignalGenerator(bt.Indicator):
    lines = ('Signal',)

    def __init__(self):
        self.lines.Signal = self.data.Signal


class DefaultStrategy(bt.Strategy):

    def __init__(self):
        # 用于保存订单
        self.order = None
        # 订单价格
        self.buyprice = None
        # 订单佣金
        self.buycomm = None

    def log(self, txt, dt=None):
        dt = dt or self.data.datetime.date(0)
        print('%s, %s' % (dt, txt))

    def notify_order(self, order):
        # 等待订单提交、订单被cerebro接受
        if order.status in [order.Submitted, order.Accepted]:
            return

        # 等待订单完成
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(
                    'BUY EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                    (order.executed.price,
                     order.executed.value,
                     order.executed.comm))

            else:
                self.log(
                    'SELL EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                    (order.executed.price,
                     order.executed.value,
                     order.executed.comm))

        # 如果订单保证金不足，将不会完成，而是执行以下拒绝程序
        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        self.order = None

    def notify_trade(self, trade):
        if not trade.isclosed:
            return

        self.log('OPERATION PROFIT, GROSS %.2f, NET %.2f' %
                 (trade.pnl, trade.pnlcomm))  # pnl：盈利  pnlcomm：手续费


class TestStrategy(DefaultStrategy):
    # 定义策略参数
    params = (
        ('period_sma10', 10),  # 短期均线周期
        ('period_sma30', 30)  # 长期均线周期
    )

    def __init__(self):
        super(TestStrategy, self).__init__()

        # 定义变量保存所有收盘价
        self.dataclose = self.data.close

        # 计算10日均线
        self.sma10 = bt.indicators.MovingAverageSimple(self.dataclose, period=self.params.period_sma10)
        # 计算30日均线
        self.sma30 = bt.indicators.MovingAverageSimple(self.dataclose, period=self.params.period_sma30)

        self.Signal = self.data.Signal

        self.Signal_line = self.data.Signal

    # 策略逻辑实现
    def next(self):
        print(self.Signal)

        buy_condition = self.sma10[0] > self.sma30[0] and self.sma10[-1] < self.sma30[-1]  # self.Signal > 0  #
        sell_condition = self.sma10[0] < self.sma30[0] and self.sma10[-1] > self.sma30[-1]  # self.Signal < 0  #

        # 当今天的10日均线大于30日均线并且昨天的10日均线小于30日均线，则进入市场（买）
        if buy_condition:
            # 判断订单是否完成，完成则为None，否则为订单信息
            if self.order:
                return

            # 若上一个订单处理完成，可继续执行买入操作
            self.order = self.buy()

        # 当今天的10日均线小于30日均线并且昨天的10日均线大于30日均线，则退出市场（卖）
        elif sell_condition:
            # 卖出
            self.order = self.sell()


class CereBroBase(object):
    __slots__ = ('_setup_broker', '_setup_state', '_cerebro', '_result')

    def __init__(self,  init_cash=100000.0, commission=0.001, position_percents=50):
        self._setup_broker = {}
        self._setup_state = False
        self._result = None

        self._cerebro = bt.Cerebro()  # 在 Backtrader 中，默认情况下，订单的执行逻辑是“当日下单，次日以开盘价成交”。
        # 在 Backtrader 中，使用 SignalStrategy 时，默认的买入价格是下一个时间点的开盘价。这是因为 Backtrader 的默认行为是“当日收盘后下单，次日以开盘价成交”
        self.add_observer()
        self.add_analyzer()
        self.setup_broker(init_cash=init_cash, commission=commission, position_percents=position_percents)

    def add_observer(self, ):
        # self._cerebro.addobserver(bt.observers.Broker)
        # self._cerebro.addobserver(bt.observers.Trades)
        self._cerebro.addobserver(bt.observers.BuySell)
        self._cerebro.addobserver(bt.observers.DrawDown)
        self._cerebro.addobserver(bt.observers.TimeReturn)

        # self._cerebro.addobserver(bt.observers.Benchmark, data=banchdata)

    def add_analyzer(self):
        self._cerebro.addanalyzer(bt.analyzers.TimeReturn, _name='_TimeReturn')
        self._cerebro.addanalyzer(bt.analyzers.PyFolio, _name='pyfolio')

    def setup_run_signal(self, df_ohlc, start_dt=None, end_dt=None, DefaultSignal=None, signal_type='SIGNAL_LONGSHORT',
                         **kwargs):
        self.setup_data(df_ohlc, start_dt=start_dt, end_dt=end_dt)

        if isinstance(signal_type, str):
            signal_type = getattr(bt, signal_type.upper())

        return self.run_signal(DefaultSignal=DefaultSignal, signal_type=signal_type, **kwargs)

    def setup_data(self, df_ohlc: pd.DataFrame, start_dt=None, end_dt=None):

        start_dt = pd.to_datetime(df_ohlc.index.min()) if start_dt is None else pd.to_datetime(start_dt)
        end_dt = pd.to_datetime(df_ohlc.index.max()) if end_dt is None else pd.to_datetime(end_dt)

        create_data_cls = SignalPandasOHLCData if 'Signal' in df_ohlc.columns else bt.feeds.PandasData

        data = create_data_cls(dataname=df_ohlc, fromdate=start_dt, todate=end_dt)

        # 加载交易数据
        self._cerebro.adddata(data, name='quote')
        self._setup_state = True

    def setup_broker(self, init_cash=100000.0, commission=0.001, position_percents=50):

        if init_cash is not None and isinstance(init_cash, (int, float)):
            self._setup_broker['init_cash'] = init_cash
        if commission is not None and isinstance(commission, (int, float)):
            self._setup_broker['commission'] = commission
        if position_percents is not None and isinstance(position_percents, (int, float)):
            self._setup_broker['position_percents'] = position_percents

        self._cerebro.broker.setcash(self._setup_broker['init_cash'])  # 设置投资金额100000.0
        # 设置佣金为0.001,
        self._cerebro.broker.setcommission(commission=self._setup_broker['commission'])
        # 设置交易模式
        self._cerebro.addsizer(bt.sizers.PercentSizer, percents=self._setup_broker['position_percents'])

    def run_strategy(self, TradingStrategy=None, **kwargs):
        if not self._setup_state:
            raise ValueError('setup is not completed!')

        # 为Cerebro引擎添加策略
        self._cerebro.addstrategy(TradingStrategy)

        # 引擎运行前打印期出资金
        print('组合期初资金: %.2f' % self._cerebro.broker.getvalue())

        result = self._cerebro.run(**kwargs)

        # 引擎运行后打期末资金
        print('组合期末资金: %.2f' % self._cerebro.broker.getvalue())

        self._result = result

        return result

    def run_signal(self, DefaultSignal=None, signal_type=bt.SIGNAL_LONG, **kwargs):

        if not self._setup_state:
            raise ValueError('setup is not completed!')

        # 为Cerebro引擎添加策略
        self._cerebro.add_signal(signal_type, DefaultSignal)

        # 引擎运行前打印期出资金
        print('组合期初资金: %.2f' % self._cerebro.broker.getvalue())

        result = self._cerebro.run(**kwargs)

        # 引擎运行后打期末资金
        print('组合期末资金: %.2f' % self._cerebro.broker.getvalue())

        self._result = result

        return result

    def plot(self, **kwargs):
        return self._cerebro.plot(**kwargs)


if __name__ == '__main__':
    pass
