# coding=utf-8
import os

import backtrader as bt
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import quantstats as qs

# qs.extend_pandas()
# 动态添加np.NINF
if not hasattr(np, 'NINF'):
    np.NINF = -np.inf

import pyfolio as pf

plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
import matplotlib.ticker as ticker  # 导入设置坐标轴的模块

from backtestsuite.core.btcore import CereBroBase, SignalGenerator
from backtestsuite.quote.akshare_quote import get_idx_quote_v2
# plt.style.use('seaborn')  # plt.style.use('dark_background')

from backtestsuite.config import Configs


class CereBroAnalyse(CereBroBase):
    def __init__(self, init_cash=100000.0, commission=0.001, position_percents=50, *kwargs):
        super().__init__(init_cash=init_cash, commission=commission,
                         position_percents=position_percents)

    def get_portfolio_info(self):
        daily_return, positions, transactions, gross_lev = self._result[0].analyzers.getbyname('pyfolio').get_pf_items()
        return daily_return, positions, transactions, gross_lev

    def _summary_cal_func_(self, cols_names=['date', 'AnnualReturn', 'CumulativeReturns', 'AnnualVvolatility',
                                             'SharpeRatio', 'CalmarRatio', 'Stability', 'MaxDrawdown',
                                             'OmegaRatio', 'SortinoRatio', 'Skew', 'Kurtosis', 'TailRatio',
                                             'DailyValueatRisk']):
        daily_return, positions, transactions, gross_lev = self.get_portfolio_info()

        nv = (daily_return + 1).cumprod()

        # 计算回撤序列
        max_return = nv.cummax()
        drawdown = (nv - max_return) / max_return

        # 计算收益评价指标

        ## 按年统计收益指标
        perf_stats_year = (daily_return).groupby(daily_return.index.to_period('y')).apply(
            lambda data: pf.timeseries.perf_stats(data)).unstack()

        # 统计所有时间段的收益指标
        perf_stats_all = pf.timeseries.perf_stats((daily_return)).to_frame(name='all')
        perf_stats = pd.concat([perf_stats_year, perf_stats_all.T], axis=0)
        perf_stats_ = round(perf_stats, 4).reset_index()

        perf_stats_.columns = cols_names

        return daily_return, positions, transactions, gross_lev, nv, drawdown, perf_stats_

    def sumamry(self, cols_names=['Date', 'AnnualReturn', 'CumulativeReturns', 'AnnualVvolatility',
                                  'SharpeRatio', 'CalmarRatio', 'Stability', 'MaxDrawdown',
                                  'OmegaRatio', 'SortinoRatio', 'Skew', 'Kurtosis', 'TailRatio',
                                  'DailyValueatRisk']):
        # 提取收益序列
        daily_return, positions, transactions, gross_lev, nv, drawdown, perf_stats_ = self._summary_cal_func_(
            cols_names=cols_names)

        # 绘制图形

        fig, (ax0, ax1) = plt.subplots(2, 1, gridspec_kw={'height_ratios': [1.5, 4]}, figsize=(20, 8))

        # 绘制表格
        ax0.set_axis_off()  # 除去坐标轴
        table = ax0.table(cellText=perf_stats_.values,
                          bbox=(0, 0, 1, 1),  # 设置表格位置， (x0, y0, width, height)
                          rowLoc='right',  # 行标题居中
                          cellLoc='right',
                          colLabels=cols_names,  # 设置列标题
                          colLoc='right',  # 列标题居中
                          edges='open'  # 不显示表格边框
                          )
        table.set_fontsize(130)
        table.auto_set_font_size(True)  # 确保自动调整字体大小

        # 绘制累计收益曲线
        ax2 = ax1.twinx()
        ax1.yaxis.set_ticks_position('right')  # 将回撤曲线的 y 轴移至右侧
        ax2.yaxis.set_ticks_position('left')  # 将累计收益曲线的 y 轴移至左侧
        # 绘制回撤曲线
        drawdown.plot.area(ax=ax1, label='Drawdown (right)', rot=0, alpha=0.3, fontsize=13, grid=False)
        # 绘制累计收益曲线
        (nv).plot(ax=ax2, color='#F1C40F', lw=3.0, label='nv (left)', rot=0, fontsize=13, grid=False)
        # 不然 x 轴留有空白
        ax2.set_xbound(lower=nv.index.min(), upper=nv.index.max())
        # 主轴定位器：每 5 个月显示一个日期：根据具体天数来做排版
        ax2.xaxis.set_major_locator(ticker.MultipleLocator(100))
        # 同时绘制双轴的图例
        h1, l1 = ax1.get_legend_handles_labels()
        h2, l2 = ax2.get_legend_handles_labels()
        plt.legend(h1 + h2, l1 + l2, fontsize=12, loc='upper left', ncol=1)

        fig.tight_layout()  # 规整排版
        plt.show()

    def qs_summary(self, daily_return, df_ohlc, benchmark_name: str = None, output='test.html'):
        daily_return.name = 'returns'
        daily_return.index = pd.to_datetime(daily_return.index.tz_localize(None))

        benchmark = df_ohlc['close'].pct_change().dropna()
        benchmark.name = benchmark_name if benchmark_name is not None else 'benchmark'

        metrics = qs.reports.metrics(returns=daily_return, benchmark=benchmark, mode='full',
                                     rf=0, display=False,
                                     prepare_returns=True)

        qs.reports.html(returns=daily_return, benchmark=benchmark, mode='full', rf=0, prepare_returns=True,
                        output=output)

        return metrics

    @staticmethod
    def _create_cls_obj_(df_ohlc_cols, cls_obj=None):
        if 'Signal' not in df_ohlc_cols and cls_obj is None:
            raise ValueError('cls_obj must be a class when Signal not in df_ohlc!')
        else:

            return SignalGenerator if cls_obj is None else cls_obj

    @classmethod
    def smart_run(cls, strategy_name: str, df_ohlc: pd.DataFrame, benchmark_name=None, cls_obj=None,
                  start_dt='2010-01-01', end_dt=None, init_cash=100000.0, commission=0.001, position_percents=50,
                  base_pth='./', signal_type=bt.SIGNAL_LONGSHORT):

        cls_obj = cls._create_cls_obj_(df_ohlc.columns, cls_obj=cls_obj)

        full_strategy_name = strategy_name if cls_obj is None else strategy_name + cls_obj.__name__

        Ch = CereBroAnalyse(init_cash=init_cash, commission=commission, position_percents=position_percents)

        Ch.setup_run_signal(df_ohlc, start_dt, end_dt, cls_obj, signal_type=signal_type)

        daily_return, positions, transactions, gross_lev = Ch.get_portfolio_info()

        # Ch.plot()

        # Ch.sumamry()

        stored_path = os.path.join(base_pth, f'{full_strategy_name}.html')

        metrics = Ch.qs_summary(daily_return, df_ohlc, benchmark_name=benchmark_name, output=stored_path)

        return full_strategy_name, metrics, stored_path


class BackTestCore(CereBroAnalyse):
    def __init__(self, config_file: str):
        self._config = Configs(config_file)

        super(BackTestCore, self).__init__(**self._config.items())

    def auto_run(self, strategy_name: str = None, df_ohlc: pd.DataFrame = None, benchmark_name=None, base_path='./',
                 signal_type=None,cls_obj=None,
                 start_dt='2010-01-01', end_dt=None, ):

        if strategy_name is None:
            strategy_name = self._config['strategy']['name']
        if benchmark_name is None:
            benchmark_name = self._config['benchmark']
        if df_ohlc is None:
            df_ohlc = get_idx_quote_v2(benchmark_name)

        if base_path is None:
            base_path = self._config['base_path']

        if start_dt is None:
            start_dt = self._config['start_dt']
        if end_dt is None:
            end_dt = self._config['end_dt']

        if signal_type is None:
            signal_type = self._config['strategy']['signal_type']

        cls_obj = self._create_cls_obj_(df_ohlc.columns, cls_obj=cls_obj)

        full_strategy_name = strategy_name if cls_obj is None else strategy_name + cls_obj.__name__

        self.setup_run_signal(df_ohlc, start_dt, end_dt, cls_obj, signal_type=signal_type)

        daily_return, positions, transactions, gross_lev = self.get_portfolio_info()

        # Ch.plot()

        # Ch.sumamry()

        stored_path = os.path.join(base_path, f'{full_strategy_name}.html')

        metrics = self.qs_summary(daily_return, df_ohlc, benchmark_name=benchmark_name, output=stored_path)

        return full_strategy_name, metrics, stored_path


if __name__ == '__main__':
    from backtestsuite.strategy_cls.bt_strategy import ADXCloseSignal



    # 添加行情数据
    df_ohlc = get_idx_quote_v2(code="000852.SH")

    # 假设你有一个包含信号的DataFrame
    signal_data = pd.DataFrame({
        'Date': ['2024-01-04', '2024-01-02', '2024-01-03'],
        'Signal': [1, 0, -1]  # 1代表买入，-1代表卖出，0代表无信号
    }).set_index('Date')

    signal_data.index = pd.to_datetime(signal_data.index)
    signal_data = signal_data.reindex(index=df_ohlc.index).fillna(0)
    df_ohlc_merged = pd.merge(df_ohlc, signal_data, left_index=True, right_index=True)

    # Ch.plot()
    #
    # Ch.sumamry()
    #

    full_strategy_name, metrics, stored_path = CereBroAnalyse.smart_run('test', df_ohlc_merged, cls_obj=ADXCloseSignal,
                                                                        start_dt='2017-01-01', end_dt=None,
                                                                        init_cash=1000000.0,
                                                                        commission=0.001,
                                                                        position_percents=90,
                                                                        base_pth='./')
