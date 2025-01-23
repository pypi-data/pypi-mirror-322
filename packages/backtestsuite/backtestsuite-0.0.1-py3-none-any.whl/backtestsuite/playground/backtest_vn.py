# # coding=utf-8
# from datetime import datetime
#
# import akshare as ak
# import pandas as pd
# import numpy as np
# from CodersWheel.QuickTool.file_cache import file_cache
# # from vnpy.app.cta_strategy.base import EVENT_CTA_LOG
# from vnpy.event import EventEngine
# from vnpy.trader.constant import Interval
# from vnpy.trader.engine import MainEngine
# from vnpy.trader.object import BarData
# from vnpy_ctastrategy import CtaStrategyApp
# from vnpy_ctastrategy.backtesting import BacktestingEngine
#
#
# @file_cache(enable_cache=True, granularity='d')
# def get_idx_quote(code):
#     stock_zh_index_daily_df = ak.stock_zh_index_daily(symbol=code).set_index('date')
#     stock_zh_index_daily_df.index = pd.to_datetime(stock_zh_index_daily_df.index)
#     return stock_zh_index_daily_df
#
#
# class MyBacktestingEngine(BacktestingEngine):
#     def __init__(self, event_engine, main_engine):
#         super().__init__(event_engine, main_engine)
#         self.dataframe = None
#         self.history_data = []
#
#     def load_data_from_dataframe(self, dataframe):
#         self.dataframe = dataframe
#
#         for index, row in dataframe.iterrows():
#             bar = BarData(
#                 symbol=self.symbol,
#                 exchange=self.exchange,
#                 datetime=row['datetime'],
#                 interval=self.interval,
#                 volume=row['volume'],
#                 open_price=row['open'],
#                 high_price=row['high'],
#                 low_price=row['low'],
#                 close_price=row['close'],
#                 gateway_name="BACKTESTING"
#             )
#             self.history_data.append(bar)
#         self.output(f"载入历史数据，数据量 {len(self.history_data)}")
#
#     def new_bar(self):
#         bar = self.history_data[self.history_index]
#         self.history_index += 1
#         self.bar = bar
#         self.datetime = bar.datetime
#         self.cross_limit_order()
#         self.cross_stop_order()
#         self.strategy.on_bar(bar)
#         self.strategy.update_bar(bar)
#         self.update_daily_close(bar.close_price)
#         self.calculate_daily_result()
#         self.calculate_daily_statistics()
#
#
# # 示例策略
# class MyStrategy(CtaStrategyApp):
#     def __init__(self, cta_engine, strategy_name, vt_symbol, setting):
#         super().__init__(cta_engine, strategy_name, vt_symbol, setting)
#         self.ma = 0
#
#     def on_init(self):
#         self.write_log("策略初始化")
#         self.load_bar(10)
#
#     def on_start(self):
#         self.write_log("策略启动")
#         self.put_event()
#
#     def on_stop(self):
#         self.write_log("策略停止")
#         self.put_event()
#
#     def on_tick(self, tick):
#         pass
#
#     def on_bar(self, bar):
#         am = self.get_array_manager()
#         if not am.inited:
#             return
#         self.ma = am.sma(20)
#         if self.pos == 0:
#             if bar.close_price > self.ma:
#                 self.buy(bar.close_price, 1)
#         elif self.pos > 0:
#             if bar.close_price < self.ma:
#                 self.sell(bar.close_price, 1)
#
#     def on_order(self, order):
#         pass
#
#     def on_trade(self, trade):
#         self.put_event()
#
#     def on_stop_order(self, stop_order):
#         pass
#
#
# if __name__ == "__main__":
#     event_engine = EventEngine()
#     main_engine = MainEngine(event_engine)
#     cta_engine = CtaStrategyApp(main_engine, event_engine)
#
#     # 创建回测引擎实例
#     backtesting_engine = MyBacktestingEngine(event_engine, main_engine)
#
#     # 设置回测参数
#     backtesting_engine.set_parameters(
#         vt_symbol="000852.SH",
#         interval=Interval.DAILY,
#         start=datetime(2019, 1, 1),
#         end=datetime(2024, 12, 31),
#         rate=0.3 / 10000,
#         slippage=0.2,
#         size=300,
#         pricetick=0.2,
#         capital=1_000_000,
#     )
#
#     # 加载数据
#     # 添加行情数据
#     df_ohlc = get_idx_quote(code="sh000852")
#     backtesting_engine.load_data_from_dataframe(df_ohlc)
#
#     # 初始化策略
#     backtesting_engine.add_strategy(MyStrategy, {})
#
#     # 开始回测
#     backtesting_engine.load_data()
#     backtesting_engine.run_backtesting()
#     df = backtesting_engine.calculate_result()
#     backtesting_engine.calculate_statistics()
#     backtesting_engine.show_chart()
